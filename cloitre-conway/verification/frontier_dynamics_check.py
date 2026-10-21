"""Independent checks of contact-frontier entrance and exact clock amplification."""

from fractions import Fraction
import json

from conway_explore import generate, literal_generate


def main():
    limit = 131072
    values, preperiods, periods, selected = generate(limit)
    literal, _ = literal_generate(2584)
    assert literal == values[:2585]
    fibonacci = [0, 1]
    while fibonacci[-1] <= limit:
        fibonacci.append(sum(fibonacci[-2:]))
    last_complete = max(level for level in range(2, len(fibonacci) - 1)
                        if fibonacci[level + 1] <= limit)

    def defect(level, offset):
        return fibonacci[level - 1] + offset - values[fibonacci[level] + offset]

    frontiers = {level: max(offset for offset in range(fibonacci[level - 2] + 1)
                            if defect(level, offset) == 0)
                 for level in range(6, last_complete + 1)}
    lower_bound_checks = 0
    left_bound_checks = 0
    capture_checks = 0
    cycle_position_checks = 0
    for base in (8, 9, 10):
        cap = max(Fraction(frontiers[base], fibonacci[base - 1]),
                  Fraction(frontiers[base + 1], fibonacci[base]))
        slope = 1 / (fibonacci[base] * (1 - cap))
        for level in range(base, last_complete + 1):
            for offset in range(fibonacci[level - 1] + 1):
                assert defect(level, offset) >= slope * max(0, offset - cap * fibonacci[level - 1])
                lower_bound_checks += 1
        margin = (1 - cap) / 4
        eta = min(slope * margin, Fraction(1, 3))
        pairs = 0
        while Fraction(2, 3) ** pairs > eta / 2:
            pairs += 1
        for level in range(max(base + 1, 10), last_complete + 1):
            first_child, second_child = fibonacci[level - 1], fibonacci[level - 2]
            if second_child < 6 / eta:
                continue
            first_offset = ((cap + margin) * second_child).__ceil__()
            offsets = sorted({first_offset + (second_child - first_offset) * part // 16
                              for part in range(17)})
            for offset in offsets:
                parent = fibonacci[level] + offset
                point = parent - 1
                trajectory = []
                positions = {}
                while point not in positions:
                    positions[point] = len(trajectory)
                    trajectory.append(point)
                    point = parent - values[point]
                first_capture = next(rank for rank, point in enumerate(trajectory)
                                     if first_child <= point <= first_child + offset)
                assert first_capture <= 2 * pairs + 1
                cycle = trajectory[positions[point]:]
                for point in cycle:
                    displacement = point - first_child
                    assert displacement >= eta * second_child
                    quotient = Fraction(offset + 1 - displacement, eta * second_child)
                    assert quotient > 0 and quotient * quotient + quotient > 1
                    cycle_position_checks += 1
                capture_checks += 1
    for base in (9, 10, 11):
        widths = {level: 2 * level // 3 - 3 for level in (base, base + 1)}
        cap = max(Fraction(widths[base], fibonacci[base - 2]),
                  Fraction(widths[base + 1], fibonacci[base - 1]))
        slope = 1 / (fibonacci[base - 1] * (1 - cap))
        for level in range(base, last_complete + 1):
            for gap in range(fibonacci[level - 2] + 1):
                left_defect = fibonacci[level - 1] - values[fibonacci[level] - gap]
                assert left_defect >= slope * max(0, gap - cap * fibonacci[level - 2])
                left_bound_checks += 1
    frontier_rows = []
    gated_rows = []
    ungated_rows = []
    for level in range(10, last_complete + 1):
        offset = frontiers[level]
        parent = fibonacci[level] + offset
        point = parent - 1
        rank = 0
        while not fibonacci[level - 1] <= point <= fibonacci[level - 1] + offset:
            point = parent - values[point]
            rank += 1
        frontier_rows.append(dict(level=level, frontier=offset, first_capture=rank,
                                  cycle_entry=preperiods[parent], period=periods[parent]))
        if fibonacci[level + 1] + offset + 4 > limit:
            continue
        if not (offset > max(4, frontiers[level - 1])
                and offset + 4 <= fibonacci[level - 1]
                and all(defect(level, small) == defect(level - 1, small) == 0
                        for small in range(5))):
            continue
        gate = all(values[fibonacci[level] + later] - fibonacci[level - 1] >= offset
                   for later in range(offset, fibonacci[level - 1] + 1))
        if not gate:
            ungated_rows.append(level)
            continue
        lower_defect = defect(level - 1, offset)
        assert lower_defect > 0
        rows = []
        for small in range(5):
            parent = fibonacci[level + 1] + offset + small
            depth = values[parent - 1]
            expected = fibonacci[level] + (small if depth % 2 else offset)
            assert selected[parent] == expected
            assert periods[parent] == 2
            assert defect(level + 1, offset + small) == (lower_defect if depth % 2 else 0)
            rows.append(dict(n=parent, depth=depth, selected_offset=selected[parent] - fibonacci[level],
                             defect=defect(level + 1, offset + small), value=values[parent]))
        drops = [small for small in range(4)
                 if values[rows[small]['n']] - values[rows[small + 1]['n']] == lower_defect - 1]
        assert drops
        gated_rows.append(dict(level=level, frontier=offset, lower_defect=lower_defect,
                               transition_offsets=drops, rows=rows))
    assert next(row for row in gated_rows if row['level'] == 16)['lower_defect'] == 3
    assert frontiers[9] == 8 and values[42] == 29 and values[43] == 28
    print(json.dumps(dict(limit=limit, evaluator='full visited-state orbits',
                          literal_values_checked_through=2584,
                          right_minorant_positions=lower_bound_checks,
                          left_minorant_positions=left_bound_checks,
                          capture_inputs=capture_checks,
                          cycle_positions=cycle_position_checks,
                          frontiers=frontier_rows, gated_frontiers=gated_rows,
                          ungated_frontiers_with_other_hypotheses=ungated_rows,
                          ungated_example=dict(level=9, frontier=8, at_contact=29, next_value=28)), indent=2))


if __name__ == '__main__':
    main()

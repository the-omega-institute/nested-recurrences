"""Check an earlier-row clock certificate without reading the current row."""

import json

from conway_explore import generate, literal_generate


def coupled_selector(prefix, parent, seed, steps, invariant_lower, source_end):
    orbit = []
    positions = {}
    point = seed
    while point not in positions:
        assert invariant_lower <= point < source_end
        positions[point] = len(orbit)
        orbit.append(point)
        point = parent - prefix[point]
    entry = positions[point]
    period = len(orbit) - entry
    selected = orbit[steps if steps < len(orbit) else entry + (steps - entry) % period]
    literal = seed
    for iteration in range(steps):
        assert invariant_lower <= literal < source_end
        literal = parent - prefix[literal]
    assert selected == literal
    return selected


def main():
    fibonacci = [0, 1]
    for level in range(2, 22):
        fibonacci.append(fibonacci[-1] + fibonacci[-2])
    level = 20
    source_end = fibonacci[level]
    anchor = fibonacci[level - 1]
    lower_anchor = fibonacci[level - 2]
    source, _, _, _ = generate(source_end - 1)
    literal, updates = literal_generate(source_end + 154)
    assert source == literal[:source_end]

    def defect(source_level, offset):
        return fibonacci[source_level - 1] + offset - source[fibonacci[source_level] + offset]

    frontiers = {
        source_level: max(offset for offset in range(fibonacci[source_level - 2] + 1)
                          if defect(source_level, offset) == 0)
        for source_level in [9, 10, 18, 19]
    }
    assert frontiers == {9: 8, 10: 7, 18: 67, 19: 87}
    upper = frontiers[19] + frontiers[18]
    assert upper == 154
    expected_images = {149: [4], 150: [4], 151: [1, 4, 8], 152: [1], 153: [1, 3, 6], 154: [4]}
    expected_feedback = [4, 4, 4, 1, 1, 4]
    states = set(range(149))
    rows = []
    evaluations = 0
    for offset in range(149, 155):
        parent = source_end + offset
        transitions = {}
        for previous_defect in range(offset):
            seed = lower_anchor + 1 + previous_defect
            depth = anchor + offset - 1 - previous_defect
            selected = coupled_selector(source, parent, seed, depth - 1, lower_anchor + 1, source_end)
            selected_offset = selected - anchor
            assert 0 <= selected_offset <= offset
            result = defect(19, selected_offset) + defect(18, offset - selected_offset)
            assert 0 <= result <= offset
            transitions[previous_defect] = result
            evaluations += 1
        image = sorted(set(transitions.values()))
        assert image == expected_images[offset]
        states = {transitions[previous] for previous in states}
        assert states == {expected_feedback[offset - 149]}
        actual_defect = anchor + offset - literal[parent]
        assert states == {actual_defect}
        rows.append({'offset': offset, 'full_image': image, 'feedback_image': sorted(states)})
    assert evaluations == 909

    offset = 154
    parent = source_end + offset
    interval_lower = lower_anchor + 1 - anchor
    interval_upper = lower_anchor + offset - anchor
    interval_rows = []
    for rank in range(1, 10):
        values = [source[anchor + argument] for argument in range(interval_lower, interval_upper + 1)]
        minimum = min(values)
        maximum = max(values)
        interval_rows.append({'absolute_rank': rank, 'offset_interval': [interval_lower, interval_upper],
                              'minimum_C': minimum, 'maximum_C': maximum})
        interval_lower, interval_upper = lower_anchor + offset - maximum, lower_anchor + offset - minimum
    assert (interval_lower, interval_upper) == (151, 154)

    def next_offset(argument):
        return parent - source[anchor + argument] - anchor

    synchronized = []
    for start in range(151, 155):
        point = start
        for iteration in range(25):
            point = next_offset(point)
        synchronized.append(point)
    assert synchronized == [45, 45, 45, 45]
    assert next_offset(45) == 112 and next_offset(112) == 45
    assert next_offset(87) == 67 and next_offset(67) == 87
    assert defect(19, 87) + defect(18, 67) == 0
    reached_phase_defects = [defect(19, argument) + defect(18, offset - argument) for argument in [45, 112]]
    assert reached_phase_defects == [4, 4]
    for previous_defect in range(offset):
        selected = coupled_selector(source, parent, lower_anchor + 1 + previous_defect,
                                    anchor + offset - 2 - previous_defect, lower_anchor + 1, source_end)
        assert selected - anchor == (112 if previous_defect % 2 == 0 else 45)
    assert anchor + 148 - literal[source_end + 148] == 0
    print(json.dumps({
        'source_prefix_inclusive': source_end - 1,
        'independent_literal_prefix': len(literal) - 1,
        'literal_updates': updates,
        'coupled_seed_clock_cases': evaluations,
        'every_coupled_case_checked_by_literal_residual_iteration': True,
        'frontiers': frontiers,
        'excluded_terminal_interval': [149, 154],
        'transition_images': rows,
        'certified_erosion_lower_bound': 6,
        'actual_contact_at_148_verified': True,
        'basin_certificate': {'parent': parent, 'first_image_interval': [2585, 2738],
                              'interval_enclosures': interval_rows, 'rank10_interval': [151, 154],
                              'synchronization_rank': 35, 'synchronization_offset': 45,
                              'reached_cycle': [45, 112], 'reached_phase_defects': reached_phase_defects,
                              'valid_but_unreached_cycle': [87, 67],
                              'even_predecessor_defect_selects': 112, 'odd_predecessor_defect_selects': 45},
        'scope': 'Finite earlier-row certificate and exact feedback; no uniform cross-level erosion or convergence claim.'
    }, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()

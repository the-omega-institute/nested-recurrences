import itertools
import json

from conway_explore import brent_generate, generate, literal_generate


def abstract_check():
    profiles = cycles = phases = 0
    for width in range(1, 4):
        for offset in range(width + 1, 2 * width + 1):
            arguments = list(range(-2, 0)) + list(range(width + 1, offset + 3))
            options = [range(-2, 1) for argument in range(-2, 0)]
            options += [range(width, argument + 1) for argument in range(width + 1, offset + 3)]
            for assignment in itertools.product(*options):
                profile = dict(zip(arguments, assignment))
                profile.update({argument: argument for argument in range(width + 1)})
                orbit = []
                point = offset + 1
                while point not in orbit:
                    assert -2 <= point <= offset + 2
                    orbit.append(point)
                    point = offset - profile[point]
                entry = orbit.index(point)
                cycle = orbit[entry:]
                profiles += 1
                if not all(0 <= argument <= offset for argument in cycle):
                    continue
                cycles += 1
                assert len(cycle) <= 2
                assert all(profile[argument] == argument for argument in cycle)
                for depth in range(entry, entry + 2 * len(cycle)):
                    selected = orbit[entry + (depth - entry) % len(cycle)]
                    phases += 1
                    if depth % 2 == 0:
                        assert offset - selected <= width
                    if offset - selected > width:
                        assert depth % 2 == 1
                        assert 0 <= selected < offset - width
                        assert profile[offset - selected] == offset - selected
    return dict(profiles=profiles, captured_reached_cycles=cycles, terminal_clock_phases=phases)


def main():
    limit = 832302
    values, _, _, _ = generate(limit)
    assert values == brent_generate(limit)
    literal, literal_updates = literal_generate(4096)
    assert values[:4097] == literal
    fibonacci = [0, 1]
    for order in range(2, 32):
        fibonacci.append(sum(fibonacci[-2:]))
    rows = []
    inner_witnesses = []
    cases = updates = cycles = 0
    for order, width in ((25, 32), (26, 32), (29, 131), (30, 131)):
        anchor = fibonacci[order - 1]
        lower = fibonacci[order - 2]
        assert all(min(argument, width) <= values[anchor + argument] - lower <= argument
                   for argument in range(lower + 1))
        positive = inner_positive = 0
        for offset in range(width + 1, 2 * width + 1):
            parent = fibonacci[order] + offset
            profile = [values[anchor + argument] - lower for argument in range(offset + 1)]
            assert all(profile[argument] == argument for argument in range(width + 1))
            assert all(min(argument, width) <= profile[argument] <= argument
                       for argument in range(offset + 1))
            assert all(values[lower + argument] == fibonacci[order - 3] + argument
                       for argument in range(width + 1))
            for initial in range(offset + 1):
                orbit = []
                point = initial
                while point not in orbit:
                    orbit.append(point)
                    point = offset - profile[point]
                cycle = orbit[orbit.index(point):]
                assert len(cycle) <= 2
                assert all(profile[argument] == argument for argument in cycle)
                cycles += 1
            depth = values[parent - 1]
            selected = parent - 1
            for iteration in range(depth):
                selected = parent - values[selected]
            updates += depth
            selected_offset = selected - anchor
            defect = anchor + offset - values[parent]
            assert defect == (selected_offset - profile[selected_offset]
                              + offset - selected_offset - values[lower + offset - selected_offset]
                              + fibonacci[order - 3])
            assert profile[selected_offset] == selected_offset
            if depth % 2 == 0:
                assert defect == 0
            if defect:
                other = offset - selected_offset
                assert depth % 2 == 1
                assert width < other <= offset
                assert profile[other] == other
                assert defect == fibonacci[order - 3] + other - values[lower + other]
                positive += 1
                inner_positive += selected_offset > 0
                if selected_offset > 0:
                    inner_witnesses.append(dict(order=order, offset=offset, parent=parent,
                                                depth=depth, selected_offset=selected_offset,
                                                copied_offset=other, defect=defect))
            cases += 1
        rows.append(dict(order=order, offsets=[width + 1, 2 * width],
                         positive_defects=positive, positive_inner_pair=inner_positive))
    assert inner_witnesses == [
        dict(order=29, offset=257, parent=514486, depth=318067,
             selected_offset=2, copied_offset=255, defect=2),
        dict(order=30, offset=257, parent=832297, depth=514485,
             selected_offset=1, copied_offset=256, defect=3),
        dict(order=30, offset=258, parent=832298, depth=514483,
             selected_offset=2, copied_offset=256, defect=3),
        dict(order=30, offset=261, parent=832301, depth=514489,
             selected_offset=3, copied_offset=258, defect=3),
    ]
    print(json.dumps(dict(status='PASS', canonical_prefix=limit,
                          independent_full_orbit_and_Brent_values_agree=True,
                          literal_prefix=4096, literal_prefix_updates=literal_updates,
                          literal_selected_clock_updates=updates, cases=cases,
                          all_captured_seed_cycles=cycles, rows=rows,
                          inner_witnesses=inner_witnesses,
                          abstract=abstract_check(),
                          scope='Finite corroboration of the written doubled-band theorem. '
                                'The unconditional infinite domain uses already proved saturated barriers.'), indent=2))


if __name__ == '__main__':
    main()

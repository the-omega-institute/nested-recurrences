"""Check an earlier-row clock certificate without reading the current row."""

import argparse
import json
import mmap

from conway_explore import brent_generate, g_closed, generate, literal_generate


class BoundedPrefix:
    def __init__(self, prefix, limit):
        self.prefix = prefix
        self.limit = limit
        self.maximum_query = 0

    def __getitem__(self, index):
        assert 1 <= index <= self.limit
        self.maximum_query = max(self.maximum_query, index)
        return self.prefix[index]


def coupled_selector(prefix, parent, seed, steps, invariant_lower, source_end, literal=True):
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
    if literal:
        literal_point = seed
        for iteration in range(steps):
            assert invariant_lower <= literal_point < source_end
            literal_point = parent - prefix[literal_point]
        assert selected == literal_point
    return selected


def brent_selector(prefix, parent, seed, steps):
    power = period = 1
    slow = seed
    fast = parent - prefix[seed]
    while slow != fast:
        if power == period:
            slow = fast
            power *= 2
            period = 0
        fast = parent - prefix[fast]
        period += 1
    slow = fast = seed
    for iteration in range(period):
        fast = parent - prefix[fast]
    entry = 0
    while slow != fast:
        slow = parent - prefix[slow]
        fast = parent - prefix[fast]
        entry += 1
    residual = steps if steps < entry else entry + (steps - entry) % period
    selected = seed
    for iteration in range(residual):
        selected = parent - prefix[selected]
    return selected


def sparse_certificate(prefix, order, endpoint):
    fibonacci = [0, 1]
    for level in range(2, order + 1):
        fibonacci.append(sum(fibonacci[-2:]))
    anchor, lower = fibonacci[order - 1], fibonacci[order - 2]
    source_end = fibonacci[order]
    source_limit = 2 * lower + endpoint - 1
    assert order >= 11 and 1 <= endpoint <= fibonacci[order - 3]
    assert len(prefix) > source_limit
    preceding = 0
    maximum_query = 0
    first_positive = None
    amplitudes = {}
    for offset in range(1, endpoint + 1):
        bounded = BoundedPrefix(prefix, 2 * lower + offset - 1)
        depth = anchor + offset - 1 - preceding
        seed = lower + 1 + preceding
        assert 0 <= preceding < offset
        selected = coupled_selector(bounded, source_end + offset, seed, depth - 1,
                                    lower + 1, source_end, literal=False)
        assert selected == brent_selector(bounded, source_end + offset, seed, depth - 1)
        value = bounded[selected] + bounded[source_end + offset - selected]
        preceding = anchor + offset - value
        assert 0 <= preceding <= offset
        maximum_query = max(maximum_query, bounded.maximum_query)
        amplitudes[preceding] = amplitudes.get(preceding, 0) + 1
        if preceding and first_positive is None:
            first_positive = dict(offset=offset, defect=preceding, value=value,
                                  selected_point=selected, depth=depth)
    return dict(status='PASS', order=order, offsets=endpoint,
                parent_anchor=source_end, source_limit=source_limit,
                unread_earlier_interval=[source_limit + 1, source_end - 1],
                maximum_query=maximum_query, paired_values_and_selected_points=endpoint,
                first_positive_defect=first_positive,
                defect_histogram=dict(sorted(amplitudes.items())),
                scope='Sparse continuation from the exact Fibonacci anchor and an earlier '
                      'prefix, with every residual query bounded separately at each offset. '
                      'Visited-orbit and Brent selectors agree. No intervening-gap or '
                      'current-row table is read; no convergence claim.')


def ternary_feedback(prefix, fibonacci, order, offset, preceding, contacts):
    anchor = fibonacci[order - 1]
    lower_anchor = fibonacci[order - 2]
    third_anchor = fibonacci[order - 3]
    parent = fibonacci[order] + offset
    distance = third_anchor - 1 - preceding
    terminal_limit = 3 * (order - 1) + (order - 2) // 3 - 24
    returns = 0
    while distance > terminal_limit:
        upper = parent - prefix[anchor - distance]
        next_distance = prefix[upper] - lower_anchor - offset
        assert 0 < next_distance <= 2 * distance // 3
        distance = next_distance
        returns += 1
    negative_level = lower_anchor - prefix[anchor - distance]
    assert negative_level in (0, 1, 2, 3)
    deviation = 0
    if negative_level in (1, 2):
        neighbor = offset + negative_level
        if lower_anchor + neighbor - prefix[anchor + neighbor] == 3:
            deviation = 3 - negative_level
    contact = contacts[offset - deviation]
    depth = anchor + offset - 1 - preceding
    selected = anchor + (offset - contact if depth % 2 else contact)
    defect = (third_anchor + contact - prefix[lower_anchor + contact]) if depth % 2 else 0
    return dict(selected=selected, defect=defect, contact=contact,
                deviation=deviation, terminal_gap=distance,
                terminal_negative_level=negative_level, exterior_returns=returns)


def ternary_certificate(prefix):
    fibonacci = [0, 1]
    for order in range(2, 35):
        fibonacci.append(sum(fibonacci[-2:]))
    order, width, endpoint, offset = 33, 225, 450, 260
    anchor, lower_anchor, third_anchor = fibonacci[32], fibonacci[31], fibonacci[30]
    source_end = fibonacci[33]
    source_limit = 2 * lower_anchor + offset - 1
    assert len(prefix) > source_limit
    prefix = BoundedPrefix(prefix, source_limit)
    assert 2 <= width < offset <= g_closed(endpoint - 1)
    assert endpoint <= min(2 * width, third_anchor) and offset + 3 <= endpoint
    source = [lower_anchor + position - prefix[anchor + position]
              for position in range(endpoint + 1)]
    assert set(source) == {0, 3}
    assert all(position - source[position] >= min(position, width)
               for position in range(endpoint + 1))
    assert g_closed(anchor + endpoint + 1) - lower_anchor >= width
    assert all(third_anchor + position == prefix[lower_anchor + position]
               for position in range(width + 1))
    contacts = list(range(endpoint + 1))
    for position in range(width + 1, endpoint + 1):
        if source[position]:
            contacts[position] = contacts[position - 3]

    expected = [(831780, 832039, 513970, 514228),
                (424025, 424891, 190842, 191963),
                (176000, 177784, 58636, 59583),
                (56804, 57996, 13776, 14365),
                (13498, 14358, 2351, 2540),
                (2310, 2538, 287, 323),
                (287, 323, 24, 26),
                (24, 26, 1, 1)]
    lower, upper = third_anchor - offset, third_anchor - 1
    rows = []
    lookups = 0
    for step, expected_row in enumerate(expected):
        assert (lower, upper) == expected_row[:2]
        outputs = [lower_anchor - prefix[anchor - distance]
                   for distance in range(lower, upper + 1)]
        minimum, maximum = min(outputs), max(outputs)
        assert (minimum, maximum) == expected_row[2:]
        rows.append(dict(step=step, distance_interval=[lower, upper],
                         negative_defect_interval=[minimum, maximum]))
        lookups += upper - lower + 1
        if step + 1 < len(expected):
            returns = [prefix[anchor + offset + distance] - lower_anchor - offset
                       for distance in range(minimum, maximum + 1)]
            lower, upper = min(returns), max(returns)
            assert lower > 0
            lookups += maximum - minimum + 1

    parent = source_end + offset
    images, reached_contacts, selected_points = set(), set(), set()
    for preceding in range(offset):
        result = ternary_feedback(prefix, fibonacci, order, offset, preceding, contacts)
        depth = anchor + offset - 1 - preceding
        selected = coupled_selector(prefix, parent, lower_anchor + 1 + preceding,
                                    depth - 1, lower_anchor + 1, source_end, literal=False)
        assert result['selected'] == selected
        direct_defect = anchor + offset - prefix[selected] - prefix[parent - selected]
        assert direct_defect == result['defect'] == 0
        assert result['terminal_negative_level'] == 1
        images.add(result['defect'])
        reached_contacts.add(result['contact'])
        selected_points.add(selected)
    assert images == {0} and reached_contacts == {255}
    assert source[261] == source[258] == 3 and source[255] == source[260] == 0
    assert third_anchor + 255 - prefix[lower_anchor + 255] == 0
    assert third_anchor + 260 - prefix[lower_anchor + 260] == 2
    return dict(status='PASS', source_limit=source_limit, order=order,
                unread_earlier_interval=[source_limit + 1, source_end - 1],
                maximum_query=prefix.maximum_query,
                width=width, source_band=endpoint, offset=offset, parent=parent,
                paired_seed_clock_comparisons=offset, interval_extrema_lookups=lookups,
                rows=rows, forced_contact=255, feedback_image=sorted(images),
                selected_points=sorted(selected_points),
                locally_permitted_default_odd_depth_defect=2,
                scope='Finite corroboration of the exact seeded decoder. The interval '
                      'certificate excludes a locally permitted positive branch for every '
                      'capped preceding state. No uniform reset estimate or extinction claim.')


def main():
    parser = argparse.ArgumentParser()
    modes = parser.add_mutually_exclusive_group()
    modes.add_argument('--ternary', action='store_true',
                       help='Check the amplitude-three seeded branch exclusion.')
    modes.add_argument('--sparse', action='store_true',
                       help='Continue a Fibonacci block using a shorter earlier prefix.')
    parser.add_argument('--order', type=int)
    parser.add_argument('--offsets', type=int)
    parser.add_argument('--values-u32',
                        help='Reuse an independently verified native unsigned-32-bit prefix.')
    arguments = parser.parse_args()
    if not __debug__:
        raise SystemExit('Run without -O; assertions perform the mathematical checks.')
    if (arguments.order is not None or arguments.offsets is not None) and not arguments.sparse:
        parser.error('--order and --offsets require --sparse')
    if arguments.values_u32 and not (arguments.ternary or arguments.sparse):
        parser.error('--values-u32 requires --ternary or --sparse')
    if arguments.ternary or arguments.sparse:
        if arguments.ternary:
            source_limit = 2692797
            evaluator = ternary_certificate
        else:
            order = 33 if arguments.order is None else arguments.order
            endpoint = 512 if arguments.offsets is None else arguments.offsets
            if order < 11 or endpoint < 1:
                parser.error('Use order >= 11 and at least one offset.')
            fibonacci = [0, 1]
            for level in range(2, order + 1):
                fibonacci.append(sum(fibonacci[-2:]))
            if endpoint > fibonacci[order - 3]:
                parser.error('The offset range must be at most F_(order-3).')
            source_limit = 2 * fibonacci[order - 2] + endpoint - 1
            evaluator = lambda prefix: sparse_certificate(prefix, order, endpoint)
        if arguments.values_u32:
            with open(arguments.values_u32, 'rb') as handle:
                with mmap.mmap(handle.fileno(), 0, access=mmap.ACCESS_READ) as mapped:
                    prefix = memoryview(mapped).cast('I')
                    report = evaluator(prefix)
                    prefix.release()
        else:
            prefix, _, _, _ = generate(source_limit)
            assert prefix == brent_generate(source_limit)
            report = evaluator(prefix)
        print(json.dumps(report, indent=2))
        return
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
        bounded_source = BoundedPrefix(source, 2 * lower_anchor + offset - 1)
        for previous_defect in range(offset):
            seed = lower_anchor + 1 + previous_defect
            depth = anchor + offset - 1 - previous_defect
            selected = coupled_selector(bounded_source, parent, seed, depth - 1,
                                        lower_anchor + 1, source_end)
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
        selected = coupled_selector(bounded_source, parent, lower_anchor + 1 + previous_defect,
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

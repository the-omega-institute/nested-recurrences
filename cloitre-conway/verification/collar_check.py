"""Corroborate the proved Fibonacci collar consequences by exact computation."""

import bisect
import hashlib
from itertools import product
import json
from pathlib import Path

from conway_explore import brent_generate, full_orbit, generate, g_closed, literal_generate
from golden_check import candidate_zeros, fibonacci_values


def interval_distance(point, lower, upper):
    return max(lower - point, point - upper, 0)


def capture_pair_budget(distance):
    pairs = 0
    while distance:
        distance = 2 * distance // 3
        pairs += 1
    return pairs


def defect_plateau_bounds(profile):
    lower = [0] * len(profile)
    upper = [0] * len(profile)
    first = 0
    for following in range(1, len(profile) + 1):
        if (following < len(profile)
                and following - profile[following] == first - profile[first]):
            continue
        for point in range(first, following):
            lower[point], upper[point] = first, following - 1
        first = following
    return lower, upper


def plateau_return_cell(scale, point, profile, bounds, domain):
    lower, upper = bounds
    domain_lower, domain_upper = domain
    following = scale - profile[point]
    assert domain_lower <= following <= domain_upper
    first_defect = point - profile[point]
    second_defect = following - profile[following]
    first_lower = max(lower[point], domain_lower)
    first_upper = min(upper[point], domain_upper)
    second_lower = max(lower[following], domain_lower)
    second_upper = min(upper[following], domain_upper)
    cell_lower = max(first_lower, scale + first_defect - second_upper)
    cell_upper = min(first_upper, scale + first_defect - second_lower)
    assert cell_lower <= point <= cell_upper
    drift = second_defect - first_defect
    exit_pairs = None
    if drift > 0:
        exit_pairs = (cell_upper - point) // drift + 1
    elif drift < 0:
        exit_pairs = (point - cell_lower) // -drift + 1
    return following, cell_lower, cell_upper, drift, exit_pairs


def plateau_iterate(scale, start, depth, profile, bounds, domain):
    point = start
    remaining = depth
    visited = {}
    blocks = []
    while remaining:
        if point in visited:
            period = visited[point] - remaining
            assert period > 0
            skipped = remaining // period * period
            if skipped:
                blocks.append(dict(kind='cycle', start=point, steps=skipped, period=period))
                remaining -= skipped
                if not remaining:
                    break
        else:
            visited[point] = remaining
        if remaining == 1:
            following = scale - profile[point]
            blocks.append(dict(kind='step', start=point, end=following, steps=1))
            point = following
            break
        following, cell_lower, cell_upper, drift, exit_pairs = plateau_return_cell(
            scale, point, profile, bounds, domain)
        if not drift:
            endpoint = following if remaining % 2 else point
            blocks.append(dict(kind='reflection', start=point, partner=following,
                               end=endpoint, steps=remaining))
            point = endpoint
            break
        pairs = min(exit_pairs, remaining // 2)
        endpoint = point + pairs * drift
        blocks.append(dict(kind='translation', start=point, end=endpoint,
                           cell=[cell_lower, cell_upper], drift=drift, pairs=pairs,
                           steps=2 * pairs))
        point = endpoint
        remaining -= 2 * pairs
        assert domain[0] <= point <= domain[1]
    assert sum(block['steps'] for block in blocks) == depth
    return point, blocks


def plateau_return_audit(sequence, splits):
    abstract_profiles = 0
    literal_iterations = 0
    for scale in range(6):
        for profile in product(*(range(point + 1) for point in range(scale + 1))):
            bounds = defect_plateau_bounds(profile)
            for start in range(scale + 1):
                point = start
                for depth in range(2 * scale + 8):
                    endpoint, _ = plateau_iterate(scale, start, depth, profile, bounds, (0, scale))
                    assert endpoint == point
                    point = scale - profile[point]
                    literal_iterations += 1
            abstract_profiles += 1
    bounds = defect_plateau_bounds(sequence)
    translation_runs = 0
    translated_pairs = 0
    indices_with_jump = 0
    longest_jump = None
    witness = None
    for index in range(3, len(sequence)):
        depth = sequence[index - 1]
        endpoint, blocks = plateau_iterate(index, index - 1, depth, sequence,
                                           bounds, (1, index - 1))
        assert endpoint == splits[index]
        jumps = [block for block in blocks
                 if block['kind'] == 'translation' and block['pairs'] > 1]
        translation_runs += len(jumps)
        translated_pairs += sum(block['pairs'] for block in jumps)
        indices_with_jump += bool(jumps)
        for block in jumps:
            if longest_jump is None or block['pairs'] > longest_jump['block']['pairs']:
                longest_jump = dict(index=index, depth=depth, block=block)
        if index == 248:
            witness = dict(index=index, depth=depth, selected_split=endpoint, blocks=blocks)
            assert endpoint == 156 and depth == 158
            assert any(block['start'] == 160 and block['end'] == 156
                       and block['pairs'] == 4 for block in jumps)
    return dict(abstract_capped_profiles=abstract_profiles,
                all_start_literal_depth_checks=literal_iterations,
                abstract_scales=[0, 5], abstract_depths='0 through 2*scale+7',
                conway_indices=[3, len(sequence) - 1],
                conway_selected_splits_checked=len(sequence) - 3,
                indices_with_nontrivial_translation=indices_with_jump,
                nontrivial_translation_runs=translation_runs,
                pairs_in_those_runs=translated_pairs, longest_observed_jump=longest_jump,
                conway_certificate=witness,
                scope='Exact-depth evaluation by paired defect plateaus and witnessed returns, independently compared with full-orbit selected splits; bounds are clipped to the prior prefix. This does not prove a uniform short certificate or a complete multiscale profile description.')


def interior_tail_examples():
    contexts = 0
    for zero_width in (0, 32):
        for centre in range(zero_width + 1, zero_width + 13):
            width = 2 * centre
            profile = [point - (zero_width < point <= centre)
                       for point in range(width + 1)]
            assert all(0 <= value <= point for point, value in enumerate(profile))
            assert all(first <= second for first, second in zip(profile, profile[1:]))
            assert profile[:zero_width + 1] == list(range(zero_width + 1))
            positions = {}
            trajectory = []
            point = centre
            while point not in positions:
                positions[point] = len(trajectory)
                trajectory.append(point)
                point = width - profile[point]
            transient = positions[point]
            assert transient == 2 * (centre - zero_width) - 1
            assert trajectory[transient:] == [width - zero_width, zero_width]
            assert len(trajectory) - transient == 2
            if zero_width == 0:
                assert len(trajectory) == width + 1
            contexts += 1
    compressed_examples = []
    for zero_width in (0, 32):
        for centre in (10 ** 12, 10 ** 18 + 7):
            width = 2 * centre
            profile = {centre: centre - 1, centre + 1: centre + 1,
                       zero_width: zero_width, width - zero_width: width - zero_width}
            lower = {centre: zero_width + 1, centre + 1: centre + 1,
                     zero_width: 0, width - zero_width: centre + 1}
            upper = {centre: centre, centre + 1: width,
                     zero_width: zero_width, width - zero_width: width}
            for depth in (10 * centre + 2, 10 * centre + 3):
                endpoint, blocks = plateau_iterate(width, centre, depth, profile,
                                                   (lower, upper), (0, width))
                assert endpoint == (width - zero_width if depth % 2 else zero_width)
                assert len(blocks) == 2
                assert blocks[0]['pairs'] == centre - zero_width
                assert blocks[0]['cell'] == [zero_width + 1, centre]
                assert blocks[0]['drift'] == -1 and blocks[0]['end'] == zero_width
                assert blocks[1]['kind'] == 'reflection'
                compressed_examples.append(dict(collar_width=zero_width, centre=centre,
                                                depth=depth, endpoint=endpoint, blocks=blocks))
    return dict(contexts_checked=contexts,
                profile_rule='H(u)=u-1 for W<u<=m; H(u)=u otherwise, on 0<=u<=2m, m>W',
                zero_defect_collar_widths=[0, 32], start='u=m',
                transient_formula='2*(m-W)-1', terminal_cycle='(2m-W,W)', period=2,
                paired_translation_cell='[W+1,m]', drift=-1,
                run_length_pairs='m-W',
                compressed_large_integer_examples=compressed_examples,
                scope='Abstract shared profile, not a C example. Nondecreasing capped profiles, defects in {0,1}, a fixed identity collar and period two do not imply short interior transients. W=0 attains mu+period=interval cardinality.')


def all_cycles(sequence, index, capture_interval=None):
    completed = bytearray(index)
    cycles = []
    for start in range(1, index):
        if completed[start]:
            continue
        positions = {}
        path = []
        point = start
        while not completed[point] and point not in positions:
            if capture_interval is not None:
                lower, upper = capture_interval
                first = index - sequence[point]
                second = index - sequence[first]
                radius = interval_distance(point, lower, upper)
                assert interval_distance(second, lower, upper) <= 2 * radius // 3
            positions[point] = len(path)
            path.append(point)
            point = index - sequence[point]
            assert 1 <= point < index
        if point in positions:
            cycles.append(tuple(sorted(path[positions[point]:])))
        for point in path:
            completed[point] = 1
    assert all(completed[1:])
    return sorted(cycles)


def selected_collar_phase_audit(sequence, splits, fibonacci, zeros):
    arithmetic_fibonacci = fibonacci_values(10 ** 100)
    floor_rows = []
    for order in range(24, len(arithmetic_fibonacci) - 1):
        anchor = arithmetic_fibonacci[order - 1]
        lower_anchor = arithmetic_fibonacci[order - 2]
        assert [g_closed(anchor + offset) - lower_anchor for offset in (33, 34, 35)] == [21, 21, 22]
        assert anchor + 33 not in candidate_zeros(arithmetic_fibonacci)
        assert anchor + 34 not in candidate_zeros(arithmetic_fibonacci)
        assert anchor % 2 == (order % 3 != 1)
        floor_rows.append(order)
    rows = []
    literal_updates = 0
    for order in range(24, len(fibonacci)):
        if fibonacci[order] + 21 >= len(sequence):
            break
        anchor = fibonacci[order - 1]
        lower_anchor = fibonacci[order - 2]
        assert all(value <= lower_anchor for value in sequence[1:anchor])
        assert anchor + 33 not in zeros and anchor + 34 not in zeros
        assert all(sequence[point] >= lower_anchor + 22
                   for point in range(anchor + 33, fibonacci[order] + 21))
        for offset in range(1, 22):
            index = fibonacci[order] + offset
            depth = sequence[index - 1]
            assert depth == anchor + offset - 1
            trajectory, transient, period = full_orbit(sequence, index)
            assert transient % 2 == 0 and trajectory[transient] == anchor + offset
            assert period == 2 and set(trajectory[transient:]) == {anchor, anchor + offset}
            for position, point in enumerate(trajectory[:transient]):
                assert (point > anchor + offset) if position % 2 == 0 else (point < anchor)
            expected = anchor + offset if (anchor + offset) % 2 else anchor
            assert splits[index] == expected
            argument = index - 1
            for iteration in range(depth):
                argument = index - sequence[argument]
            assert argument == expected
            literal_updates += depth
            rows.append(dict(order=order, offset=offset, transient=transient,
                             entry_offset=offset, selected_offset=expected - anchor))
    window_edges = 0
    for order in range(25, len(fibonacci)):
        if fibonacci[order] + 21 >= len(sequence):
            break
        for offset, following_offset in product(range(22), repeat=2):
            index = fibonacci[order] + offset
            following_index = fibonacci[order] + following_offset
            first = splits[index]
            following_first = splits[following_index]
            second = index - first
            following_second = following_index - following_first
            first_offset = first - fibonacci[order - 1]
            following_first_offset = following_first - fibonacci[order - 1]
            second_offset = second - fibonacci[order - 2]
            following_second_offset = following_second - fibonacci[order - 2]
            assert first_offset == (offset if (fibonacci[order - 1] + offset) % 2 else 0)
            assert second_offset == offset - first_offset
            first_parameter = following_first + sequence[first] - fibonacci[order]
            second_parameter = following_second + sequence[second] - fibonacci[order - 1]
            assert first_parameter == first_offset + following_first_offset
            assert second_parameter == second_offset + following_second_offset
            assert first_parameter + second_parameter == offset + following_offset
            window_edges += 1
    boundary = []
    for order in (22, 23):
        anchor = fibonacci[order - 1]
        for offset in range(22):
            index = fibonacci[order] + offset
            argument = index - 1
            for iteration in range(sequence[index - 1]):
                argument = index - sequence[argument]
            assert argument == splits[index]
            literal_updates += sequence[index - 1]
            boundary.append(dict(order=order, offset=offset, value=sequence[index],
                                 selected_split=argument))
    return dict(universal_orders='k >= 24', offsets_inclusive=[1, 21],
                selected_endpoint_rule='A+t if A+t is odd; A otherwise, A=F_(k-1)',
                prescribed_basin='Outermost two-cycle {A,A+t}; first entry is A+t at an even time',
                exact_floor_offsets=[33, 34, 35], exact_floor_values_relative_to_lower_anchor=[21, 21, 22],
                arithmetic_only_floor_orders_inclusive=[floor_rows[0], floor_rows[-1]],
                checked_orbits=len(rows), orbit_rows=rows, literal_selected_updates=literal_updates,
                all_offset_pair_window_edges_checked=window_edges,
                finite_boundary_orders=[22, 23], boundary_records=boundary,
                scope='The uniform basin and phase rule follows from the proved cap, exact equality set and linear collar, not these finite checks. Floor checks beyond the sequence prefix use integer square roots only. Boundary records are finite actual iterations, not a uniform phase rule at orders22/23. No global five-cycle phase theorem or minimum complete proof size is claimed.')


def main():
    if not __debug__:
        raise SystemExit('Run without -O; assertions perform the checks.')
    limit = 131071
    sequence, preperiods, periods, splits = generate(limit)
    assert sequence == brent_generate(limit)
    literal, updates = literal_generate(4096)
    assert sequence[:len(literal)] == literal
    fibonacci = fibonacci_values(limit + 2)
    zeros = candidate_zeros(fibonacci)
    sharp_trajectory, sharp_preperiod, sharp_period = full_orbit(sequence, 8)
    assert sharp_trajectory == [7, 3, 6, 4, 5] and sharp_preperiod == 4 and sharp_period == 1
    assert 8 - sequence[8 - sequence[2]] == 3
    anchor_drop_pairs = 0
    anchor_drop_base = []
    for order, anchor in enumerate(fibonacci):
        if order < 5:
            continue
        if anchor > limit:
            break
        lower_anchor = fibonacci[order - 1]
        for point in range(1, anchor):
            assert lower_anchor - sequence[point] <= 2 * (anchor - point) // 3
            if order <= 10:
                arithmetic_lower = g_closed(point) + (point not in zeros)
                assert lower_anchor - arithmetic_lower <= 2 * (anchor - point) // 3
            anchor_drop_pairs += 1
        if order <= 10:
            anchor_drop_base.append(dict(order=order, anchor=anchor,
                                         lower_anchor=lower_anchor, arguments_checked=anchor - 1))
    selected_cycle_points = 0
    selected_two_step_checks = 0
    maximum_capture_time = 0
    capture_time_witness = None
    maximum_core_capture_time = 0
    core_capture_time_witness = None
    core_two_step_checks = 0
    for index in range(8, limit + 1):
        block_order = bisect.bisect_right(fibonacci, index) - 1
        order = block_order
        if fibonacci[order + 1] - index < index - fibonacci[order]:
            order += 1
        offset = index - fibonacci[order]
        anchor = fibonacci[order - 1]
        lower = anchor + min(0, offset)
        upper = anchor + max(0, offset)
        trajectory, preperiod, period = full_orbit(sequence, index)
        assert preperiod == preperiods[index] and period == periods[index]
        assert period <= abs(offset) + 1
        assert lower <= splits[index] <= upper
        capture_time = next(position for position, point in enumerate(trajectory)
                            if lower <= point <= upper)
        initial_distance = interval_distance(index - 1, lower, upper)
        pair_budget = capture_pair_budget(initial_distance)
        assert capture_time <= 2 * pair_budget
        assert preperiod <= 2 * pair_budget + abs(offset) + 1 - period
        assert (abs(offset) + 2 * index - 1) ** 2 < 5 * index ** 2
        global_comparison = preperiod + period - 2 * pair_budget - 2 + 2 * index
        assert 0 <= global_comparison and global_comparison ** 2 < 5 * index ** 2
        block_anchor = fibonacci[block_order]
        block_lower = fibonacci[block_order - 1]
        block_child = fibonacci[block_order - 2]
        block_offset = index - block_anchor
        core_lower = max(block_lower, index - block_lower)
        core_upper = min(index - block_child, block_anchor)
        core_width = core_upper - core_lower
        assert core_width == min(block_offset, fibonacci[block_order - 3],
                                 block_lower - block_offset)
        core_distance = interval_distance(index - 1, core_lower, core_upper)
        assert core_distance == max(block_child, block_offset) - 1
        core_pair_budget = capture_pair_budget(core_distance)
        core_capture_time = next(position for position, point in enumerate(trajectory)
                                 if core_lower <= point <= core_upper)
        assert core_capture_time <= 2 * core_pair_budget
        assert preperiod + period <= 2 * core_pair_budget + core_width + 1
        width_comparison = 3 * index - 4 * core_width + 4
        assert width_comparison > 0 and width_comparison ** 2 > 5 * index ** 2
        core_global_comparison = 3 * index - 4 * (preperiod + period - 2 * core_pair_budget - 2)
        assert core_global_comparison > 0 and core_global_comparison ** 2 > 5 * index ** 2
        for point in trajectory:
            first = index - sequence[point]
            second = index - sequence[first]
            radius = interval_distance(point, lower, upper)
            assert interval_distance(second, lower, upper) <= 2 * radius // 3
            selected_two_step_checks += 1
            core_radius = interval_distance(point, core_lower, core_upper)
            assert interval_distance(second, core_lower, core_upper) <= 2 * core_radius // 3
            core_two_step_checks += 1
        if capture_time > maximum_capture_time:
            maximum_capture_time = capture_time
            capture_time_witness = dict(index=index, order=order, offset=offset,
                                        initial_distance=initial_distance, capture_time=capture_time,
                                        pair_budget=pair_budget, preperiod=preperiod, period=period)
        if core_capture_time > maximum_core_capture_time:
            maximum_core_capture_time = core_capture_time
            core_capture_time_witness = dict(index=index, block_order=block_order,
                                             block_offset=block_offset,
                                             core_interval=[core_lower, core_upper],
                                             initial_distance=core_distance,
                                             capture_time=core_capture_time,
                                             pair_budget=core_pair_budget,
                                             preperiod=preperiod, period=period)
        for point in trajectory[preperiod:]:
            assert lower <= point <= upper
            selected_cycle_points += 1
    positive_identities = []
    negative_identities = []
    graph_count = 0
    graph_vertices = 0
    classified_graph_count = 0
    witnesses = []
    for order, index in enumerate(fibonacci):
        if index + 2 > limit:
            break
        if order >= 5:
            assert sequence[index + 2] == fibonacci[order - 1] + 2
            positive_identities.append(order)
        if order >= 8:
            assert sequence[index - 2] == fibonacci[order - 1]
            negative_identities.append(order)
        if order < 6:
            continue
        anchor = fibonacci[order - 1]
        for offset in range(-2, 3):
            lower = anchor + min(0, offset)
            upper = anchor + max(0, offset)
            actual_cycles = all_cycles(sequence, index + offset, (lower, upper))
            assert all(lower <= point <= upper for cycle in actual_cycles for point in cycle)
            assert all(len(cycle) <= abs(offset) + 1 for cycle in actual_cycles)
            expected = {
                -2: [(anchor - 2,)],
                -1: [(anchor - 1,)],
                0: [(anchor,)],
                1: [(anchor, anchor + 1)],
                2: [(anchor, anchor + 2), (anchor + 1,)],
            }[offset]
            if offset != -2 or order >= 9:
                assert actual_cycles == sorted(expected)
                classified_graph_count += 1
            graph_count += 1
            graph_vertices += index + offset - 1
            if order in (6, 9, 26):
                witnesses.append(dict(order=order, offset=offset, index=index + offset,
                                      cycles=actual_cycles))
    left_width = 12
    right_width = 32
    seed_orders = [23, 24]
    seed_values = []
    stable_identity_orders = []
    for order in range(seed_orders[0], len(fibonacci)):
        index = fibonacci[order]
        if index + right_width > limit:
            break
        actual = [sequence[index + offset] - fibonacci[order - 1]
                  for offset in range(-left_width, right_width + 1)]
        assert actual == [max(0, offset) for offset in range(-left_width, right_width + 1)]
        stable_identity_orders.append(order)
        if order in seed_orders:
            seed_values.append(dict(order=order, index=index, relative_values=actual))
    assert len(seed_values) == 2
    stable_graph_order = 24
    stable_graph_index = fibonacci[stable_graph_order]
    stable_anchor = fibonacci[stable_graph_order - 1]
    stable_graph_witnesses = []
    stable_graph_count = 0
    stable_graph_vertices = 0
    for offset in range(-left_width, right_width + 1):
        lower = stable_anchor + min(0, offset)
        upper = stable_anchor + max(0, offset)
        actual_cycles = all_cycles(sequence, stable_graph_index + offset, (lower, upper))
        trajectory, transient, period = full_orbit(sequence, stable_graph_index + offset)
        capture_time = next(position for position, point in enumerate(trajectory)
                            if lower <= point <= upper)
        assert transient <= capture_time + (offset < 0)
        if offset <= 0:
            expected_cycles = [(stable_anchor + offset,)]
        else:
            expected_cycles = [(stable_anchor + point, stable_anchor + offset - point)
                               for point in range((offset + 1) // 2)]
            if offset % 2 == 0:
                expected_cycles.append((stable_anchor + offset // 2,))
        assert actual_cycles == sorted(expected_cycles)
        stable_graph_count += 1
        stable_graph_vertices += stable_graph_index + offset - 1
        if offset in (-left_width, 0, 1, 2, right_width):
            stable_graph_witnesses.append(dict(offset=offset, cycles=actual_cycles))
    report = dict(
        status='Exact two-collar seeds and finite corroboration; fibonacci-collars.md Sections 1-4 use golden-proof.md, and Section 6 adds the recorded seed premises; no Lean formalization.',
        source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        evaluator_source_sha256=hashlib.sha256(Path(__file__).with_name('conway_explore.py').read_bytes()).hexdigest(),
        limit=limit,
        sequence_sha256=hashlib.sha256(','.join(map(str, sequence[1:])).encode('ascii')).hexdigest(),
        independent_brent_agrees_through=limit,
        literal_agrees_through=4096,
        literal_updates=updates,
        selected_orbit_localization_inclusive=[8, limit],
        selected_cycle_points_checked=selected_cycle_points,
        positive_two_identity_orders=positive_identities,
        negative_two_identity_orders=negative_identities,
        all_start_graphs_checked=graph_count,
        all_start_vertices_checked=graph_vertices,
        exact_classified_graphs_checked=classified_graph_count,
        graph_order_range_inclusive=[6, 26],
        graph_offsets_inclusive=[-2, 2],
        classification_witnesses=witnesses,
        exact_collar_propagation=dict(
            offsets_inclusive=[-left_width, right_width],
            seeds=seed_values, seed_value_count=len(seed_values) * (left_width + right_width + 1),
            identities_checked_orders=stable_identity_orders,
            universal_identity_orders='all k >= 23, by the two-collar induction',
            universal_cycle_classification_orders='all k >= 24, by capture and reflection',
            all_start_graph_order=stable_graph_order,
            all_start_graphs_checked=stable_graph_count,
            all_start_vertices_checked=stable_graph_vertices,
            classification_witnesses=stable_graph_witnesses,
        ),
        selected_positive_collar_phase=selected_collar_phase_audit(sequence, splits, fibonacci, zeros),
        quantitative_capture=dict(
            anchor_drop_formula='F_(j-1)-C(F_j-d) <= floor(2*d/3), j>=5, 1<=d<F_j',
            anchor_drop_base=anchor_drop_base,
            anchor_drop_base_pairs=sum(row['arguments_checked'] for row in anchor_drop_base),
            anchor_drop_base_scope='Exact G-floor and equality-set arithmetic; no new sequence-prefix premise',
            anchor_drop_pairs_checked=anchor_drop_pairs,
            two_step_formula='dist(T_n^2(x), I) <= floor(2*dist(x,I)/3)',
            selected_trajectory_two_step_checks=selected_two_step_checks,
            all_start_two_step_checks=graph_vertices + stable_graph_vertices,
            selected_capture_bound_indices=[8, limit],
            maximum_capture_time=maximum_capture_time,
            capture_time_witness=capture_time_witness,
            pair_budget_rule='repeat d <- floor(2*d/3) until zero; capture time <= 2 * number of repetitions',
            full_preperiod_bound='mu <= 2*q(d_initial) + abs(t)+1-period',
            global_joint_orbit_bound='mu+period < (sqrt(5)-2)*n + 2*q(d_initial)+2, using the closest Fibonacci index',
            two_anchor_core=dict(
                interval_formula='[max(F_(k-1),n-F_(k-1)), min(n-F_(k-2),F_k)] for F_k<=n<F_(k+1)',
                width_formula='min(t,F_(k-3),F_(k-1)-t), t=n-F_k',
                initial_distance_formula='max(F_(k-2),t)-1 for start n-1',
                selected_two_step_checks=core_two_step_checks,
                maximum_capture_time=maximum_core_capture_time,
                capture_time_witness=core_capture_time_witness,
                joint_orbit_bound='mu+period <= 2*q(d_core)+core_width+1',
                global_joint_orbit_bound='mu+period < ((3-sqrt(5))/4)*n+2*q(d_core)+2',
                scope='The two adjacent anchor intervals intersect to the full intersection of every eligible Fibonacci capture interval. Actual cycle widths or periods need not attain this geometric bound.',
            ),
            certified_collar_preperiod='mu <= capture_time for 0<=t<=32; mu <= capture_time+1 for -12<=t<0, k>=24',
            sharp_two_step_example=dict(anchor=5, lower_anchor=3, index=8, start=2,
                                        second_iterate=3, initial_distance=3, second_distance=2),
            sharp_prescribed_start_example=dict(index=8, initial_distance=2, pair_budget=2,
                                               trajectory=sharp_trajectory, preperiod=sharp_preperiod),
            scope='General argument uses the proved G bound, equality set and cap; the 130 small-anchor cases are exact G-floor/equality-set arithmetic, not new sequence premises. Larger orbit checks are corroboration. Logarithmic capture is not logarithmic full landing in arbitrary wide arches.',
            interior_tail_counterexample=interior_tail_examples(),
            plateau_return_certificates=plateau_return_audit(sequence, splits),
        ),
        full_ratio_convergence='open; sublinear-neighborhood convergence is proved separately',
    )
    print(json.dumps(report, indent=2) + '\n', end='')


if __name__ == '__main__':
    main()

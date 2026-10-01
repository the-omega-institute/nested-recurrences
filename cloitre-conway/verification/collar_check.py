"""Corroborate the proved Fibonacci collar consequences by exact computation."""

import bisect
from fractions import Fraction
from functools import lru_cache
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


def capped_profile_cycles(profile, scale):
    completed = set()
    cycles = []
    for start in range(scale + 1):
        if start in completed:
            continue
        positions = {}
        path = []
        point = start
        while point not in completed and point not in positions:
            positions[point] = len(path)
            path.append(point)
            point = scale - profile[point]
            assert 0 <= point <= scale
        if point in positions:
            cycles.append(tuple(path[positions[point]:]))
        completed.update(path)
    return cycles


def saturated_profile_abstract_audit():
    contexts = 0
    proper_cycles = 0
    for width in range(5):
        for scale in range(width + 6):
            for profile in product(*(range(min(point, width), point + 1)
                                     for point in range(scale + 1))):
                for cycle in capped_profile_cycles(profile, scale):
                    if len(cycle) >= 3:
                        assert min(cycle) > width and max(cycle) <= scale - width
                        assert len(cycle) <= scale - 2 * width
                        proper_cycles += 1
                contexts += 1
    sharp = []
    for width in (0, 1, 32):
        for period in range(3, 13):
            if period % 2:
                centred = tuple(value for amplitude in range(1, period, 2)
                                for value in (amplitude, -amplitude)) + (period,)
            else:
                centred = tuple(value for amplitude in range(period - 2, 0, -2)
                                for value in (-amplitude, amplitude)) + (0, period)
            cycle = tuple(width + (period + value) // 2 for value in centred)
            scale = 2 * width + period
            profile = list(range(scale + 1))
            for position, point in enumerate(cycle):
                profile[point] = scale - cycle[(position + 1) % period]
            assert all(min(point, width) <= value <= point for point, value in enumerate(profile))
            assert len(set(cycle)) == period and min(cycle) == width + 1
            assert max(cycle) == scale - width and len(cycle) == scale - 2 * width
            assert all(scale - profile[point] == cycle[(position + 1) % period]
                       for position, point in enumerate(cycle))
            cost = sum(point - profile[point] for point in cycle)
            assert cost == period
            sharp.append(dict(width=width, scale=scale, cycle=list(cycle), defect_cost=cost))
    return dict(exhaustive_capped_saturated_profiles=contexts, proper_cycles_checked=proper_cycles,
                saturation_widths=[0, 4], maximum_scale_rule='width+5',
                sharp_spatial_and_defect_examples=sharp,
                scope='Complete small capped/saturated profile enumeration and abstract sharp constructions. These profiles are not claimed to be C or to satisfy its recurrence.')


def saturated_profile_audit(sequence, periods, splits, fibonacci):
    width = 32
    seeds = []
    for order in (23, 24):
        values = [sequence[fibonacci[order] + offset] - fibonacci[order - 1]
                  for offset in range(33, 51)]
        assert min(values) >= width
        seeds.append(dict(order=order, offsets_inclusive=[33, 50], relative_values=values))
    arithmetic_fibonacci = fibonacci_values(10 ** 100)
    arithmetic_orders = []
    for order in range(23, len(arithmetic_fibonacci) - 1):
        assert g_closed(arithmetic_fibonacci[order] + 51) >= arithmetic_fibonacci[order - 1] + width
        arithmetic_orders.append(order)
    profile_rows = []
    for order in range(23, len(fibonacci)):
        anchor = fibonacci[order]
        if anchor >= len(sequence):
            break
        stop = min(fibonacci[order + 1], len(sequence) - 1)
        assert all(sequence[point] - fibonacci[order - 1] >= min(point - anchor, width)
                   for point in range(anchor, stop + 1))
        profile_rows.append(dict(order=order, offsets_inclusive=[0, stop - anchor],
                                 whole_closed_block=stop == fibonacci[order + 1]))
    extra_phases = []
    literal_updates = 0
    all_start_graphs = 0
    all_start_vertices = 0
    for order in range(24, len(fibonacci)):
        if fibonacci[order] + 66 >= len(sequence):
            break
        anchor = fibonacci[order - 1]
        for offset in range(33, 67):
            index = fibonacci[order] + offset
            cycles = all_cycles(sequence, index, (anchor, anchor + offset))
            assert all(len(cycle) <= 2 for cycle in cycles)
            all_start_graphs += 1
            all_start_vertices += index - 1
        for offset in range(22, 33):
            index = fibonacci[order] + offset
            trajectory, transient, period = full_orbit(sequence, index)
            entry = trajectory[transient] - anchor
            assert period == 2 and set(trajectory[transient:]) == {anchor, anchor + offset}
            assert (entry == offset and transient % 2 == 0) or (entry == 0 and transient % 2 == 1)
            if offset < width:
                assert entry == offset and transient % 2 == 0
            expected = anchor + offset if (anchor + offset) % 2 else anchor
            argument = index - 1
            depth = sequence[index - 1]
            for iteration in range(depth):
                argument = index - sequence[argument]
            assert argument == expected == splits[index]
            literal_updates += depth
            extra_phases.append(dict(order=order, offset=offset, transient=transient,
                                     entry_offset=entry, selected_offset=expected - anchor))
    selected_proper_cycles = 0
    selected_five_cycles = 0
    first_five_per_order = {}
    for index in range(fibonacci[24], len(sequence)):
        if periods[index] < 3:
            continue
        order = bisect.bisect_right(fibonacci, index) - 1
        offset = index - fibonacci[order]
        trajectory, transient, period = full_orbit(sequence, index)
        cycle = tuple(point - fibonacci[order - 1] for point in trajectory[transient:])
        assert min(cycle) > width and max(cycle) <= offset - width
        assert period <= offset - 2 * width
        lower = max(width + 1, offset - fibonacci[order - 3])
        upper = min(offset - width, fibonacci[order - 2])
        assert lower <= min(cycle) <= max(cycle) <= upper
        assert period <= upper - lower + 1
        if period == 5:
            selected_five_cycles += 1
            first_five_per_order.setdefault(order, dict(order=order, index=index, offset=offset,
                                                        cycle_offsets=list(cycle)))
        selected_proper_cycles += 1
    extra_boundary = []
    for order in (22, 23):
        for offset in range(22, 33):
            index = fibonacci[order] + offset
            argument = index - 1
            for iteration in range(sequence[index - 1]):
                argument = index - sequence[argument]
            assert argument == splits[index]
            literal_updates += sequence[index - 1]
            extra_boundary.append(dict(order=order, offset=offset, value=sequence[index],
                                       selected_split=argument))
    boundary_failures = []
    for order, offset, expected_index in ((24, 33, 46401), (25, 42, 75067), (25, 43, 75068)):
        index = fibonacci[order] + offset
        assert index == expected_index
        anchor = fibonacci[order - 1]
        trajectory, transient, period = full_orbit(sequence, index)
        cycle = trajectory[transient:]
        depth = sequence[index - 1]
        argument = index - 1
        for iteration in range(depth):
            argument = index - sequence[argument]
        assert argument == splits[index] and period == 2
        literal_updates += depth
        outputs = [sequence[point] + sequence[index - point] for point in cycle]
        predicted = anchor + offset if (anchor + offset) % 2 else anchor
        boundary_failures.append(dict(order=order, offset=offset, index=index,
                                      cycle_offsets=[point - anchor for point in cycle],
                                      transient=transient, actual_depth=depth,
                                      linear_depth_prediction=anchor + offset - 1,
                                      actual_selected_offset=argument - anchor,
                                      collar_selected_offset_prediction=predicted - anchor,
                                      root_value=sequence[index], cycle_value_outputs=outputs))
    assert boundary_failures[0]['cycle_offsets'] == [1, 32]
    assert boundary_failures[0]['actual_selected_offset'] == 1
    assert len(set(boundary_failures[0]['cycle_value_outputs'])) == 1
    assert boundary_failures[1]['cycle_offsets'] == [42, 0]
    assert boundary_failures[1]['cycle_value_outputs'] == [46410, 46407]
    assert boundary_failures[2]['actual_depth'] == 46407
    assert boundary_failures[2]['linear_depth_prediction'] == 46410
    assert boundary_failures[2]['actual_selected_offset'] == 0
    assert boundary_failures[2]['collar_selected_offset_prediction'] == 43
    return dict(width=width, universal_profile_orders='j >= 23',
                profile_lower_bound='P_j(u) >= min(u,32) on the entire closed natural block',
                additional_seed_value_count=36, seeds=seeds,
                arithmetic_floor_orders_inclusive=[arithmetic_orders[0], arithmetic_orders[-1]],
                arithmetic_floor_offset=51, profile_rows=profile_rows,
                abstract_cycle_bound=saturated_profile_abstract_audit(),
                proper_cycle_offset_domain='33 <= u <= t-32',
                intersected_proper_cycle_domain='max(33,t-F_(k-3)) <= u <= min(t-32,F_(k-2))',
                proper_period_bound='p <= t-64 for every p>=3, k>=24',
                five_cycle_requires_offset_at_least=69,
                all_start_extra_graph_offsets=[33, 66], all_start_extra_graphs=all_start_graphs,
                all_start_extra_vertices=all_start_vertices,
                selected_proper_cycles_checked=selected_proper_cycles,
                selected_five_cycles_checked=selected_five_cycles,
                first_selected_five_per_order=list(first_five_per_order.values()),
                extended_selected_phase_offsets=[1, 32], additional_phase_orbits=extra_phases,
                additional_literal_selected_updates=literal_updates, additional_boundary_records=extra_boundary,
                wider_collar_failure_witnesses=boundary_failures,
                scope='General two-scale saturation induction plus a minimum/maximum cycle argument. The36 extra seeds and earlier exact collar seeds are finite premises; all-start and selected-cycle checks are corroboration. The extended endpoint rule proves actual basin and phase on offsets1..32, with possible odd entry at the lower endpoint when t=32. Recursive nonautonomous windows in0..32 have arithmetic splits, but the spatial period bound applies only to autonomous constant-parameter cycles. No wider-arch phase classification or full minimum closure theorem is claimed.')


def negative_plateau_width(order):
    return 2 * order // 3 - 3


def moving_negative_plateau_audit(sequence, splits, fibonacci):
    base_order = 10
    base_anchor = fibonacci[base_order]
    base_cap = fibonacci[base_order - 1]
    base_profile = [base_cap - sequence[base_anchor - gap]
                    for gap in range(fibonacci[base_order - 2] + 1)]
    expected_base = [0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 3, 4, 6, 5, 6, 8, 9, 9, 10, 11, 12, 13]
    assert base_profile == expected_base
    seed_order = 9
    seed_values = [sequence[fibonacci[seed_order] - gap] for gap in range(4)]
    assert seed_values == [fibonacci[seed_order - 1]] * 4
    literal, updates = literal_generate(base_anchor)
    assert literal == sequence[:base_anchor + 1] == brent_generate(base_anchor)
    abstract_profiles = 0
    periodic_readouts = 0
    for collar_width in range(3, 13):
        for extra in range(2, 9):
            gap = collar_width + extra
            ranges = [range(1, max(1, point - collar_width - 1) + 1)
                      for point in range(collar_width + 1, gap + 1)]
            for tail in product(*ranges):
                profile = [0] * (collar_width + 1) + list(tail)
                cycles = capped_profile_cycles(profile, gap)
                for cycle in cycles:
                    for selected in cycle:
                        assert collar_width < selected < gap
                        lower_gap = gap - selected
                        lower_cap = 0 if lower_gap <= 3 else 2 * lower_gap // 3
                        maximum_defect = profile[selected] + lower_cap
                        assert maximum_defect > 0
                        assert maximum_defect <= (1 if extra == 2 else extra - 2)
                        periodic_readouts += 1
                abstract_profiles += 1
    block_vertices = 0
    selected_rows = 0
    recursive_rows = 0
    five_window_rows = 0
    five_window_witness = None
    new_endpoint_rows = []
    for order in range(6, 31):
        anchor = fibonacci[order]
        cap = fibonacci[order - 1]
        collar_width = negative_plateau_width(order)
        for gap in range(fibonacci[order - 2] + 1):
            defect = cap - sequence[anchor - gap]
            assert (defect == 0) == (gap <= collar_width)
            if order >= 7 and gap > collar_width:
                assert 1 <= defect <= max(1, gap - collar_width - 1)
            block_vertices += 1
        if order < 11:
            continue
        previous_width = negative_plateau_width(order - 1)
        assert collar_width == previous_width + int(order % 3 != 1)
        assert previous_width + 2 < fibonacci[order - 3]
        for gap in range(previous_width + 2):
            index = anchor - gap
            boundary = gap == previous_width + 1
            shift = int(boundary and order % 3 != 1)
            expected_split = cap - gap + shift
            trajectory, transient, period = full_orbit(sequence, index)
            expected_cycle = {cap - gap, cap - gap + 1} if boundary else {cap - gap}
            assert set(trajectory[transient:]) == expected_cycle
            assert period == 1 + int(boundary)
            assert splits[index] == expected_split
            assert sequence[index] == cap - int(boundary and not shift)
            if boundary:
                capture = next(position for position, point in enumerate(trajectory)
                               if cap - gap <= point <= cap)
                assert capture % 2 == 0 and trajectory[capture] > cap - gap
                assert sequence[index - 1] == cap - 1
                assert fibonacci[order - 2] - sequence[cap - gap] == 1
                assert fibonacci[order - 2] - sequence[cap - gap - 1] == 1
            if gap <= collar_width:
                first_gap = gap - shift
                second_gap = shift
                assert first_gap <= negative_plateau_width(order - 1)
                assert second_gap <= negative_plateau_width(order - 2)
                assert sequence[expected_split] == fibonacci[order - 2]
                assert sequence[index - expected_split] == fibonacci[order - 3]
                recursive_rows += 1
                if boundary and order in (24, 26, 30):
                    new_endpoint_rows.append(dict(order=order, gap=gap, index=index,
                                                  selected_split=expected_split, period=period,
                                                  first_child_gap=first_gap, second_child_gap=second_gap))
            selected_rows += 1
        gaps = [0, 1, collar_width // 2, collar_width - 1, collar_width]
        shifts = [int(gap == previous_width + 1) for gap in gaps]
        profile_order = order - 1
        parent_offsets = [fibonacci[profile_order - 1] - gap for gap in gaps]
        first_offsets = [fibonacci[profile_order - 2] - gap + shift
                         for gap, shift in zip(gaps, shifts)]
        second_offsets = [fibonacci[profile_order - 3] - shift for shift in shifts]
        parent_parameters = []
        first_parameters = []
        second_parameters = []
        for row, gap in enumerate(gaps):
            following = (row + 1) % 5
            index = anchor - gap
            split = splits[index]
            assert split - fibonacci[profile_order - 1] == first_offsets[row]
            assert index - split - fibonacci[profile_order - 2] == second_offsets[row]
            parent_parameter = parent_offsets[following] + sequence[index] - fibonacci[profile_order - 1]
            first_parameter = first_offsets[following] + sequence[split] - fibonacci[profile_order - 2]
            second_parameter = second_offsets[following] + sequence[index - split] - fibonacci[profile_order - 3]
            assert parent_parameter == fibonacci[profile_order] - gaps[following]
            assert first_parameter == fibonacci[profile_order - 1] - gaps[following] + shifts[following]
            assert second_parameter == fibonacci[profile_order - 2] - shifts[following]
            assert first_parameter + second_parameter == parent_parameter
            parent_parameters.append(parent_parameter)
            first_parameters.append(first_parameter)
            second_parameters.append(second_parameter)
            five_window_rows += 1
        if order == 30:
            defects = [fibonacci[profile_order - 3] - gap for gap in gaps]
            five_window_witness = dict(anchor_order=order, gaps=gaps, shifts=shifts,
                                       parent_parameters=parent_parameters, first_parameters=first_parameters,
                                       second_parameters=second_parameters, total_natural_defect=sum(defects),
                                       residual_selector_labels=0)
    threshold_rows = []
    for gap in (17, 18, 32, 100, 1000):
        threshold = max(6, (3 * (gap + 3) + 1) // 2)
        assert negative_plateau_width(threshold) >= gap
        assert threshold == 6 or negative_plateau_width(threshold - 1) < gap
        threshold_rows.append(dict(gap=gap, first_exact_order_at_least_six=threshold))
    return dict(base_order=base_order, base_gaps_inclusive=[0, fibonacci[base_order - 2]],
                base_defect_profile=base_profile, width_three_seed_order=seed_order,
                width_three_seed_values=seed_values, unique_scalar_seed_indices_inclusive=[31, 55],
                independently_literal_checked_through=base_anchor, base_literal_updates=updates,
                abstract_widths_inclusive=[3, 12], abstract_extra_gaps_inclusive=[2, 8],
                abstract_shelf_profiles=abstract_profiles, abstract_periodic_readouts=periodic_readouts,
                actual_complete_block_orders_inclusive=[6, 30], actual_block_vertices=block_vertices,
                actual_selected_fixed_or_boundary_rows=selected_rows,
                actual_closed_arithmetic_rows=recursive_rows, new_two_cycle_endpoints=new_endpoint_rows,
                actual_moving_five_window_rows=five_window_rows, arithmetic_five_window=five_window_witness,
                width_formula='L_k=floor(2*k/3)-3, k>=6',
                exact_tail_threshold_formula='max(6,ceil(3*(v+3)/2))', threshold_examples=threshold_rows,
                scope='Simultaneous top-suffix/shelf-barrier induction and boundary depth parity prove the exact moving negative plateau for actual C. Small seeds are literal/full-orbit/Brent premises; larger blocks and abstract graphs corroborate the written proof. A freshly added zero endpoint has a proper two-cycle, so scalar exactness does not imply a fixed inner cycle. Arithmetic child gaps close the moving plateau with supplied order/gap, excluding finite base-table and scale/context costs. No complete actual-C interface, wide-arch dispersion, global limit or Lean claim.')


def unit_defect_width(order):
    return order + (order - 1) // 3 - 6


def unit_defect_shift(order, gap):
    previous_zero = negative_plateau_width(order - 1)
    previous_unit = unit_defect_width(order - 1)
    if gap <= previous_zero:
        return 0
    if gap == previous_zero + 1:
        return int(order % 3 != 1)
    if gap <= previous_unit + 1:
        return 1
    assert gap == previous_unit + 2 and order % 3 == 1
    return 2


def unit_defect_closure_audit(sequence, splits, fibonacci):
    base_order = 19
    base_anchor = fibonacci[base_order]
    base_cap = fibonacci[base_order - 1]
    base_profile = [base_cap - sequence[base_anchor - gap]
                    for gap in range(fibonacci[base_order - 2] + 1)]
    literal, updates = literal_generate(base_anchor)
    assert literal == sequence[:base_anchor + 1] == brent_generate(base_anchor)
    assert unit_defect_width(base_order) == 19
    for gap, defect in enumerate(base_profile):
        assert (defect <= 1) == (gap <= unit_defect_width(base_order))
        assert (defect == 0) == (gap <= negative_plateau_width(base_order))
        if gap > unit_defect_width(base_order):
            assert 2 <= defect <= max(2, gap - unit_defect_width(base_order) - 1)
    abstract_profiles = 0
    abstract_readouts = 0
    lower_gap_bounds = 0
    for lower_gap in range(2, 4097):
        lower_cap = 0 if lower_gap <= 9 else 2 * lower_gap // 3
        assert lower_cap <= lower_gap - 2
        if lower_gap >= 3:
            assert lower_cap <= lower_gap - 3
        if lower_gap >= 4:
            assert lower_cap <= lower_gap - 4
        lower_gap_bounds += 1
    for zero_width in range(3, 9):
        for unit_width in range(zero_width + 2, zero_width + 7):
            for extra in range(1, 10):
                gap = unit_width + extra
                ranges = [range(2, max(2, point - unit_width - 1) + 1)
                          for point in range(unit_width + 1, gap + 1)]
                for tail in product(*ranges):
                    profile = [0] * (zero_width + 1) + [1] * (unit_width - zero_width) + list(tail)
                    cycles = capped_profile_cycles(profile, gap)
                    if extra == 1:
                        assert cycles == [(unit_width,)]
                    elif extra == 2:
                        assert len(cycles) == 1 and set(cycles[0]) == {unit_width, unit_width + 1}
                    else:
                        for cycle in cycles:
                            for selected in cycle:
                                assert unit_width < selected <= gap - 2
                                lower_gap = gap - selected
                                lower_cap = 0 if lower_gap <= 9 else 2 * lower_gap // 3
                                upper_readout = profile[selected] + lower_cap
                                assert 2 <= upper_readout <= max(2, gap - unit_width - 3)
                                abstract_readouts += 1
                    abstract_profiles += 1
    block_vertices = 0
    selected_rows = 0
    unit_rows = 0
    phase_rows = 0
    first_spine_steps = 0
    boundary_records = []
    dispersion_minimum = None
    dispersion_witness = None
    five_window_witness = None
    for order in range(base_order, 31):
        anchor = fibonacci[order]
        cap = fibonacci[order - 1]
        zero_width = negative_plateau_width(order)
        unit_width = unit_defect_width(order)
        for gap in range(fibonacci[order - 2] + 1):
            defect = cap - sequence[anchor - gap]
            assert (defect <= 1) == (gap <= unit_width)
            if gap > unit_width:
                assert 2 <= defect <= max(2, gap - unit_width - 1)
            block_vertices += 1
        if order == base_order:
            continue
        previous_zero = negative_plateau_width(order - 1)
        previous_unit = unit_defect_width(order - 1)
        assert unit_width == previous_unit + 1 + int(order % 3 == 1)
        assert previous_unit + 3 < fibonacci[order - 3]
        boundary_gap = previous_unit + 2
        boundary_index = anchor - boundary_gap
        trajectory, transient, period = full_orbit(sequence, boundary_index)
        lower = cap - previous_unit - 1
        upper = lower + 1
        assert period == 2 and set(trajectory[transient:]) == {lower, upper}
        assert all(point > upper if position % 2 == 0 else point < lower
                   for position, point in enumerate(trajectory[:transient]))
        assert all(point >= upper if position % 2 == 0 else point <= lower
                   for position, point in enumerate(trajectory))
        assert sequence[boundary_index - 1] == cap - 2
        expected_boundary = upper if order % 3 == 1 else lower
        assert splits[boundary_index] == expected_boundary
        assert cap - sequence[boundary_index] == (1 if order % 3 == 1 else 2)
        boundary_records.append(dict(order=order, gap=boundary_gap, index=boundary_index,
                                     cycle=[lower, upper], transient=transient,
                                     depth=sequence[boundary_index - 1], selected_split=expected_boundary,
                                     cap_defect=cap - sequence[boundary_index]))
        for gap in range(unit_width + 1):
            index = anchor - gap
            defect = int(gap > zero_width)
            shift = unit_defect_shift(order, gap)
            split = cap - gap + shift
            assert splits[index] == split and sequence[index] == cap - defect
            first_gap = gap - shift
            assert first_gap <= previous_unit and shift <= negative_plateau_width(order - 2)
            assert sequence[split] == fibonacci[order - 2] - defect
            assert sequence[index - split] == fibonacci[order - 3]
            trajectory, transient, period = full_orbit(sequence, index)
            cycle = trajectory[transient:]
            if gap == previous_zero + 1:
                expected_cycle = {cap - gap, cap - gap + 1}
            elif gap == previous_unit + 2:
                expected_cycle = {cap - gap + 1, cap - gap + 2}
            else:
                expected_cycle = {split}
            assert set(cycle) == expected_cycle
            selected_rows += 1
            unit_rows += defect
            spine_order, spine_gap = order, gap
            while spine_order >= 20:
                spine_shift = unit_defect_shift(spine_order, spine_gap)
                spine_gap -= spine_shift
                spine_order -= 1
                assert spine_gap <= unit_defect_width(spine_order)
                assert int(spine_gap > negative_plateau_width(spine_order)) == defect
                first_spine_steps += 1
            golden_defect = sequence[index] - g_closed(index)
            assert 0 <= golden_defect <= gap
            for point in cycle:
                complement = index - point
                phase_shift = point - (cap - gap)
                numerator = fibonacci[order - 2] * complement - fibonacci[order - 3] * point
                expected_numerator = (-1) ** (order - 1) + fibonacci[order - 3] * gap - cap * phase_shift
                assert numerator == expected_numerator
                if gap:
                    assert 2 * numerator >= fibonacci[order - 3] * gap
                assert 25 * numerator ** 2 >= gap ** 2 * point * complement
                assert 25 * numerator ** 2 >= golden_defect ** 2 * point * complement
                if golden_defect:
                    ratio = Fraction(numerator ** 2, point * complement * golden_defect ** 2)
                    if dispersion_minimum is None or ratio < dispersion_minimum:
                        dispersion_minimum = ratio
                        dispersion_witness = dict(order=order, gap=gap, index=index,
                                                  phase_split=point, golden_defect=golden_defect)
                phase_rows += 1
        if order == 28:
            gaps = [0, 16, 17, 30, 31]
            shifts = [unit_defect_shift(order, gap) for gap in gaps]
            defects = [int(gap > zero_width) for gap in gaps]
            assert shifts == [0, 0, 1, 1, 2] and defects == [0, 1, 1, 1, 1]
            profile_order = order - 1
            parent_parameters = []
            first_parameters = []
            second_parameters = []
            for row, gap in enumerate(gaps):
                following = (row + 1) % 5
                index = anchor - gap
                split = splits[index]
                first_offset = fibonacci[profile_order - 2] - gap + shifts[row]
                second_offset = fibonacci[profile_order - 3] - shifts[row]
                assert split - fibonacci[profile_order - 1] == first_offset
                assert index - split - fibonacci[profile_order - 2] == second_offset
                parent_parameter = fibonacci[profile_order] - gaps[following] - defects[row]
                first_parameter = (fibonacci[profile_order - 1] - gaps[following]
                                   + shifts[following] - defects[row])
                second_parameter = fibonacci[profile_order - 2] - shifts[following]
                assert first_parameter + second_parameter == parent_parameter
                first_profile = sequence[split] - fibonacci[profile_order - 2]
                second_profile = sequence[index - split] - fibonacci[profile_order - 3]
                assert first_profile == fibonacci[profile_order - 3] - defects[row]
                assert second_profile == fibonacci[profile_order - 4]
                next_first_offset = fibonacci[profile_order - 2] - gaps[following] + shifts[following]
                next_second_offset = fibonacci[profile_order - 3] - shifts[following]
                assert next_first_offset + first_profile == first_parameter
                assert next_second_offset + second_profile == second_parameter
                parent_parameters.append(parent_parameter)
                first_parameters.append(first_parameter)
                second_parameters.append(second_parameter)
            five_window_witness = dict(anchor_order=order, gaps=gaps, shifts=shifts, cap_defects=defects,
                                       parent_parameters=parent_parameters, first_parameters=first_parameters,
                                       second_parameters=second_parameters, residual_selector_labels=0)
    return dict(base_order=base_order, base_scalar_indices_inclusive=[fibonacci[18], base_anchor],
                base_full_gap_positions=len(base_profile), base_zero_width=negative_plateau_width(base_order),
                base_unit_width=unit_defect_width(base_order),
                base_profile_sha256=hashlib.sha256(','.join(map(str, base_profile)).encode('ascii')).hexdigest(),
                independently_literal_checked_through=base_anchor, base_literal_updates=updates,
                unit_width_formula='R_k=k+floor((k-1)/3)-6, k>=19',
                shelf_formula='2<=Q_k(v)<=max(2,v-R_k-1) for v>R_k, k>=19',
                abstract_profiles=abstract_profiles, abstract_periodic_upper_readouts=abstract_readouts,
                lower_gap_arithmetic_bounds_checked=lower_gap_bounds,
                actual_complete_block_orders_inclusive=[19, 30], actual_block_vertices=block_vertices,
                actual_closed_selector_rows=selected_rows, actual_unit_defect_rows=unit_rows,
                first_child_spine_steps=first_spine_steps, boundary_records=boundary_records,
                arithmetic_five_window=five_window_witness, all_basin_phase_variance_checks=phase_rows,
                basin_quadratic_constant='1/25', basin_ratio_minimum=str(dispersion_minimum),
                basin_ratio_witness=dispersion_witness,
                scope='Finite base and abstract graph checks for the unit-sublevel/shelf induction; actual selector and single-defective-spine checks through order30. All basin phases satisfy the scoped one-step quadratic dispersion inequality in the proved Q<=1 family. No wide-block or global dispersion bound, full minimum interface or Lean claim.')


def negative_adjacent_transitions(amplitude, adjacent):
    if amplitude == 1:
        return {1} if adjacent == 1 else {adjacent, 0, 1}
    return {0, 1, amplitude} if adjacent == 1 else {0, adjacent}


def parity_envelope_partition(transitions):
    classes = {adjacent: adjacent % 2 for adjacent in transitions}
    while True:
        signatures = {adjacent: (adjacent % 2, tuple(sorted({classes[following]
                                                            for following in successors})))
                      for adjacent, successors in transitions.items()}
        labels = {signature: label for label, signature in enumerate(sorted(set(signatures.values())))}
        refined = {adjacent: labels[signature] for adjacent, signature in signatures.items()}
        if all((classes[first] == classes[second]) == (refined[first] == refined[second])
               for first in transitions for second in transitions):
            return refined
        classes = refined


def parity_clock_longest_path(transitions, positive_only=False):
    @lru_cache(None)
    def continuation(phase, adjacent):
        following_phase = (phase + 1) % 3
        paths = [continuation(following_phase, following)
                 for following in sorted(transitions[adjacent])
                 if following % 2 == int(following_phase == 1)
                 and (not positive_only or following > 0)]
        longest = max(paths, key=len, default=())
        return ((phase, adjacent),) + longest
    paths = [continuation(phase, adjacent) for phase in range(3) for adjacent in transitions
             if adjacent % 2 == int(phase == 1) and (not positive_only or adjacent > 0)]
    return max(paths, key=len)


def negative_adjacent_gap_audit(sequence, fibonacci):
    amplitude_contexts = 0
    profile_contexts = 0
    partition_counts = set()
    maximum_survival = {1: 0, 2: 0}
    maximum_positive_survival = 0
    for gap in range(3, 65):
        width = gap + 1
        cap = 2 * width // 3
        assert cap < gap
        for amplitude in range(1, 2 * gap // 3 + 1):
            transitions = {}
            for adjacent in range(cap + 1):
                profile = [0] * gap + [amplitude, adjacent]
                cycles = capped_profile_cycles(profile, width)
                assert all(width - point < gap for cycle in cycles for point in cycle)
                actual_readouts = {profile[point] for cycle in cycles for point in cycle}
                expected = negative_adjacent_transitions(amplitude, adjacent)
                assert actual_readouts == expected
                transitions[adjacent] = actual_readouts
                profile_contexts += 1
            classes = parity_envelope_partition(transitions)
            expected_classes = {adjacent: (0 if adjacent % 2 == 0 else 1 if adjacent == 1 else 2)
                                if amplitude == 1 else adjacent % 2 for adjacent in transitions}
            assert all((classes[first] == classes[second])
                       == (expected_classes[first] == expected_classes[second])
                       for first in transitions for second in transitions)
            count = len(set(classes.values()))
            assert count == (3 if amplitude == 1 and cap >= 3 else 2)
            partition_counts.add((amplitude == 1, count))
            trace = parity_clock_longest_path(transitions)
            positive_trace = parity_clock_longest_path(transitions, positive_only=True)
            bound = 4 if amplitude == 1 else 3
            assert len(trace) <= bound and len(positive_trace) <= 3
            maximum_survival[1 if amplitude == 1 else 2] = max(
                maximum_survival[1 if amplitude == 1 else 2], len(trace))
            maximum_positive_survival = max(maximum_positive_survival, len(positive_trace))
            amplitude_contexts += 1
    assert maximum_survival == {1: 4, 2: 3} and maximum_positive_survival == 3
    sharp_unit_trace = parity_clock_longest_path({adjacent: negative_adjacent_transitions(1, adjacent)
                                                for adjacent in range(4)})
    sharp_larger_trace = parity_clock_longest_path({adjacent: negative_adjacent_transitions(2, adjacent)
                                                  for adjacent in range(4)})
    assert len(sharp_unit_trace) == 4 and len(sharp_larger_trace) == 3
    actual_rows = []
    for order in range(7, 31):
        for gap in range(3, min(129, fibonacci[order - 3])):
            if not all(sequence[fibonacci[order - 1] - smaller] == fibonacci[order - 2]
                       for smaller in range(gap)):
                continue
            amplitude = fibonacci[order - 2] - sequence[fibonacci[order - 1] - gap]
            if not amplitude:
                continue
            adjacent = fibonacci[order - 2] - sequence[fibonacci[order - 1] - gap - 1]
            assert 0 <= adjacent < gap and 0 < amplitude < gap
            if not all(sequence[fibonacci[order - 2] - smaller] == fibonacci[order - 3]
                       for smaller in {1, amplitude, adjacent}):
                continue
            index = fibonacci[order] - gap - 1
            next_adjacent = fibonacci[order - 1] - sequence[index]
            assert next_adjacent in negative_adjacent_transitions(amplitude, adjacent)
            trajectory, transient, period = full_orbit(sequence, index)
            profile = [0] * gap + [amplitude, adjacent]
            expected_cycles = {frozenset(cycle) for cycle in capped_profile_cycles(profile, gap + 1)}
            actual_cycle = frozenset(fibonacci[order - 1] - point for point in trajectory[transient:])
            assert actual_cycle in expected_cycles
            actual_rows.append(dict(order=order, gap=gap, adjacent_index=index, amplitude=amplitude,
                                    preceding_adjacent_defect=adjacent, next_adjacent_defect=next_adjacent,
                                    selected_adjacent_period=period))
    suffix_rows = []
    suffix_vertices = 0
    for order in range(5, 31):
        top = fibonacci[order - 1]
        stop = fibonacci[order]
        first = next(index for index in range(top, stop + 1) if sequence[index] == top)
        assert all(sequence[index] == top for index in range(first, stop + 1))
        assert all(sequence[index] != top for index in range(top, first))
        suffix_vertices += stop - top + 1
        if order >= 6:
            assert stop - first == 2 * order // 3 - 3
        suffix_rows.append(dict(order=order, first_top_index=first, top_value=top, negative_width=stop - first))
    return dict(abstract_gaps_inclusive=[3, 64], amplitude_contexts=amplitude_contexts,
                capped_profile_contexts=profile_contexts,
                parity_partition_types=[list(row) for row in sorted(partition_counts)],
                unit_amplitude_maximum_clock_survival=maximum_survival[1],
                larger_amplitude_maximum_clock_survival=maximum_survival[2],
                positive_adjacent_only_maximum_clock_survival=maximum_positive_survival,
                sharp_unit_amplitude_trace=[list(row) for row in sharp_unit_trace],
                sharp_larger_amplitude_trace=[list(row) for row in sharp_larger_trace],
                actual_adjacent_contexts=actual_rows,
                complete_top_suffix_orders_inclusive=[5, 30], top_suffix_vertices=suffix_vertices,
                top_suffix_rows=suffix_rows,
                scope='Complete adjacent-gap cycle/readout envelope, exact parity-trace quotient and clock obstruction are general proofs with supplied flat lower profiles and amplitude. Three/two states count envelope parity continuations, not actual-C graph memory or numeric adjacent defects. Zero adjacent defects are allowed in the envelope. The separate moving-plateau induction establishes actual top contiguity and resolves its entrance premise; the qualified actual first boundary has unit amplitude and adjacent defect one. No global limit/dispersion or Lean claim.')


def negative_collar_boundary_audit(sequence, splits, fibonacci):
    abstract_contexts = 0
    abstract_start_depth_checks = 0
    for gap in range(2, 33):
        for previous_defect in range(2 * gap // 3 + 1):
            for transfer_defect in range(2 * previous_defect // 3 + 1):
                expected_cycle = {gap} if not previous_defect else {gap, gap - previous_defect}
                readouts = set()
                for start in range(gap + 1):
                    point = start
                    positions = {}
                    trajectory = []
                    while point not in positions:
                        positions[point] = len(trajectory)
                        trajectory.append(point)
                        point = gap - (previous_defect if point == gap else 0)
                    assert set(trajectory[positions[point]:]) == expected_cycle
                    point = start
                    entrance_flag = int(start < gap)
                    for depth in range(2 * gap + 5):
                        if point in expected_cycle:
                            defect = ((previous_defect if point == gap else 0)
                                      + (transfer_defect if gap - point == previous_defect else 0))
                            expected = (previous_defect if depth % 2 == entrance_flag else transfer_defect)
                            assert defect == expected
                            readouts.add(defect)
                            abstract_start_depth_checks += 1
                        point = gap - (previous_defect if point == gap else 0)
                assert len(readouts) == (2 if previous_defect else 1)
                abstract_contexts += 1
    seed_rows = []
    arithmetic_window_rows = 0
    arithmetic_window_witness = None
    for width, order in ((13, 24), (14, 26), (15, 27), (16, 29), (17, 30)):
        index = fibonacci[order] - width
        anchor = fibonacci[order - 1]
        values = [sequence[fibonacci[order] - gap] - anchor for gap in range(width + 1)]
        assert values == [0] * (width + 1)
        assert width < fibonacci[order - 2]
        corroborating_orders = []
        for height in range(order, 31):
            assert all(sequence[fibonacci[height] - gap] == fibonacci[height - 1]
                       for gap in range(width + 1))
            if height > order:
                for gap in range(width + 1):
                    parent = fibonacci[height] - gap
                    parent_anchor = fibonacci[height - 1]
                    assert all(parent - sequence[parent_anchor - point] == parent_anchor - gap
                               for point in range(gap + 1))
                    assert splits[parent] == parent_anchor - gap
                for length in (1, 2, 3, 5):
                    gaps = [0, 1, width // 2, width - 1, width][:length]
                    profile_order = height - 1
                    parents = [fibonacci[height] - gap for gap in gaps]
                    offsets = [parent - fibonacci[profile_order] for parent in parents]
                    first_offsets = [splits[parent] - fibonacci[profile_order - 1] for parent in parents]
                    second_offsets = [parent - splits[parent] - fibonacci[profile_order - 2] for parent in parents]
                    profiles = [sequence[parent] - fibonacci[profile_order - 1] for parent in parents]
                    assert profiles == [fibonacci[profile_order - 2]] * length
                    assert first_offsets == [fibonacci[profile_order - 2] - gap for gap in gaps]
                    assert second_offsets == [fibonacci[profile_order - 3]] * length
                    parameters = []
                    first_parameters = []
                    second_parameters = []
                    for row, parent in enumerate(parents):
                        following = (row + 1) % length
                        parameter = offsets[following] + profiles[row]
                        first_parameter = (first_offsets[following] + sequence[splits[parent]]
                                           - fibonacci[profile_order - 2])
                        second_parameter = (second_offsets[following] + sequence[parent - splits[parent]]
                                            - fibonacci[profile_order - 3])
                        assert parameter == fibonacci[profile_order] - gaps[following]
                        assert first_parameter == fibonacci[profile_order - 1] - gaps[following]
                        assert second_parameter == fibonacci[profile_order - 2]
                        assert first_parameter + second_parameter == parameter
                        parameters.append(parameter)
                        first_parameters.append(first_parameter)
                        second_parameters.append(second_parameter)
                    defects = [offset - profile for offset, profile in zip(offsets, profiles)]
                    assert defects == [fibonacci[profile_order - 3] - gap for gap in gaps]
                    arithmetic_window_rows += length
                    if height == 30 and width == 16 and length == 5:
                        arithmetic_window_witness = dict(anchor_order=height, profile_order=profile_order,
                                                         gaps=gaps, indices=parents, offsets=offsets,
                                                         defects=defects, total_defect=sum(defects),
                                                         first_offsets=first_offsets, second_offsets=second_offsets,
                                                         parent_parameters=parameters,
                                                         first_parameters=first_parameters,
                                                         second_parameters=second_parameters,
                                                         selected_splits=[splits[parent] for parent in parents])
            corroborating_orders.append(height)
        seed_rows.append(dict(width=width, order=order, index=index, value=sequence[index],
                              relative_seed_values=values, corroborating_orders=corroborating_orders,
                              universal_value_orders=f'all k >= {order}, by single-seed propagation',
                              universal_unique_fixed_cycle_orders=f'all k >= {order + 1}'))
    conditional_contexts = 0
    positive_rows = []
    absorbing_tail_contexts = 0
    for order in range(7, 31):
        for gap in range(2, min(129, fibonacci[order - 3])):
            if not all(sequence[fibonacci[order - 1] - smaller] == fibonacci[order - 2]
                       for smaller in range(gap)):
                continue
            index = fibonacci[order] - gap
            anchor = fibonacci[order - 1]
            previous_defect = fibonacci[order - 2] - sequence[fibonacci[order - 1] - gap]
            transfer_defect = fibonacci[order - 3] - sequence[fibonacci[order - 2] - previous_defect]
            assert 0 <= previous_defect <= 2 * gap // 3 < gap
            assert 0 <= transfer_defect <= 2 * previous_defect // 3
            trajectory, transient, period = full_orbit(sequence, index)
            capture = next(position for position, point in enumerate(trajectory)
                           if anchor - gap <= point <= anchor)
            assert capture % 2 == 0
            assert all((point > anchor and index - sequence[point] < anchor - gap)
                       or (point < anchor - gap and index - sequence[point] >= anchor - gap)
                       for point in trajectory[:capture])
            if not previous_defect:
                assert period == 1 and trajectory[transient:] == [anchor - gap]
                assert sequence[index] == anchor and splits[index] == anchor - gap
            else:
                assert period == 2
                assert set(trajectory[transient:]) == {anchor - gap, anchor - gap + previous_defect}
                entrance_flag = int(trajectory[capture] > anchor - gap)
                depth = sequence[index - 1]
                expected_defect = (previous_defect if depth % 2 == entrance_flag else transfer_defect)
                assert sequence[index] == anchor - expected_defect
                positive_rows.append(dict(order=order, gap=gap, index=index,
                                          previous_defect=previous_defect, transfer_defect=transfer_defect,
                                          capture_time=capture, entrance_flag=entrance_flag, depth=depth,
                                          selected_gap=anchor - splits[index],
                                          parent_defect=anchor - sequence[index]))
            conditional_contexts += 1
            initial_height = order - 1
            previous = fibonacci[initial_height - 1] - sequence[fibonacci[initial_height] - gap]
            for height in range(order, 31):
                current = fibonacci[height - 1] - sequence[fibonacci[height] - gap]
                if height == order:
                    assert current in (previous, transfer_defect)
                else:
                    assert current in (previous, 0)
                previous = current
            absorbing_tail_contexts += 1
    literal_witnesses = []
    literal_updates = 0
    for order, gap in ((24, 13), (25, 14), (26, 14)):
        index = fibonacci[order] - gap
        anchor = fibonacci[order - 1]
        trajectory, transient, period = full_orbit(sequence, index)
        depth = sequence[index - 1]
        point = index - 1
        for iteration in range(depth):
            point = index - sequence[point]
        literal_updates += depth
        assert point == splits[index] and period == 2
        other = next(vertex for vertex in trajectory[transient:] if vertex != point)
        other_value = sequence[other] + sequence[index - other]
        assert sequence[index] != other_value
        literal_witnesses.append(dict(order=order, gap=gap, index=index, depth=depth,
                                      transient=transient, cycle=list(trajectory[transient:]),
                                      selected_split=point, value=sequence[index],
                                      other_split=other, other_value=other_value))
    return dict(abstract_gaps_inclusive=[2, 32], abstract_contexts=abstract_contexts,
                abstract_start_depth_readout_checks=abstract_start_depth_checks,
                new_scalar_seed_premises=5, whole_seed_values_corroborated=sum(row['width'] + 1 for row in seed_rows),
                seed_rows=seed_rows, conditional_actual_contexts=conditional_contexts,
                absorbing_tail_contexts=absorbing_tail_contexts,
                arithmetic_selected_window_rows=arithmetic_window_rows,
                arithmetic_selected_five_window=arithmetic_window_witness,
                nonzero_actual_boundary_rows=positive_rows,
                literal_witnesses=literal_witnesses, literal_endpoint_updates=literal_updates,
                adjacent_gap_parity=negative_adjacent_gap_audit(sequence, fibonacci),
                moving_negative_plateau=moving_negative_plateau_audit(sequence, splits, fibonacci),
                unit_defect_closure=unit_defect_closure_audit(sequence, splits, fibonacci),
                scope='Single-negative-seed propagation and first-boundary copy-or-contract/readout-phase proofs are general. Earlier scalar seeds reuse the independently agreeing F30+34 full-orbit/Brent prefix. The separate small-seed moving-plateau induction now proves all fixed negative widths, top contiguity and the unit-amplitude actual boundary rule. Full recursive minimum, dispersion and global convergence remain open. Conditional phase-state minima exclude supplied context and its certification cost.')


def positive_collar_extinction_audit(sequence, fibonacci):
    local_contexts = 0
    periodic_splits = 0
    for offset in range(1, 13):
        for first_top, second_top in product(range(1, offset + 1), repeat=2):
            first = tuple(range(offset)) + (first_top,)
            second = tuple(range(offset)) + (second_top,)
            for cycle in capped_profile_cycles(first, offset):
                for split in cycle:
                    value = first[split] + second[offset - split]
                    if value < offset:
                        assert split == 0 and first_top == offset and second_top < offset
                        assert value == second_top
                    periodic_splits += 1
            local_contexts += 1
    extinction_rows = []
    for offset_parity in (0, 1):
        for base_mod in range(3):
            states = set(product((0, 1), repeat=2))
            last_positive = 1
            transitions = []
            for step in range(2, 10):
                phase_allows = ((base_mod + step) % 3 != 1) if offset_parity else ((base_mod + step) % 3 == 1)
                following = set()
                for earlier, previous in states:
                    following.add((previous, 0))
                    if earlier and not previous and phase_allows:
                        following.add((previous, 1))
                states = following
                if any(previous for earlier, previous in states):
                    last_positive = step
                transitions.append(dict(step=step, states=[list(state) for state in sorted(states)]))
            expected = ((2, 4, 3), (6, 5, 4))[offset_parity][base_mod]
            assert last_positive + 1 == expected and states == {(0, 0)}
            extinction_rows.append(dict(offset_parity=offset_parity, base_order_mod3=base_mod,
                                         first_uniform_linear_step=expected, state_trace=transitions))
    conditional_rows = 0
    conditional_nonzero_rows = []
    for order in range(6, len(fibonacci) - 1):
        for offset in range(1, 129):
            if fibonacci[order] + offset >= len(sequence):
                break
            if not all(sequence[fibonacci[height] + point] == fibonacci[height - 1] + point
                       for height in (order - 2, order - 1, order) for point in range(offset)):
                continue
            defects = [fibonacci[height - 1] + offset - sequence[fibonacci[height] + offset]
                       for height in (order - 2, order - 1, order)]
            assert all(defect >= 0 for defect in defects)
            if defects[-1]:
                assert defects[-1] == defects[0] and defects[1] == 0
                assert (fibonacci[order - 1] + offset) % 2 == 0
                conditional_nonzero_rows.append(dict(order=order, offset=offset, defect=defects[-1]))
            conditional_rows += 1
    threshold_rows = []
    threshold = 23
    for offset in range(33, 1001):
        increment = ((2, 4, 3), (6, 5, 4))[offset % 2][threshold % 3]
        threshold += increment
        expected = 23 + 3 * (offset - 32) + (offset - 32) % 2
        assert threshold == expected
        threshold_rows.append((offset, threshold))
    higher_limit = fibonacci[30] + 34
    higher_sequence, _, _, higher_splits = generate(higher_limit)
    assert higher_sequence == brent_generate(higher_limit)
    higher_cases = []
    literal_updates = 0
    for offset, orders in ((33, range(27, 31)), (34, range(29, 31))):
        for order in orders:
            index = fibonacci[order] + offset
            assert higher_sequence[index] == fibonacci[order - 1] + offset
            point = index - 1
            depth = higher_sequence[index - 1]
            for iteration in range(depth):
                point = index - higher_sequence[point]
            assert point == higher_splits[index]
            literal_updates += depth
            higher_cases.append(dict(order=order, offset=offset, index=index,
                                     value=higher_sequence[index], selected_offset=point - fibonacci[order - 1]))
    width_rows = []
    arithmetic_fibonacci = fibonacci_values(10 ** 100)
    for order in range(23, len(arithmetic_fibonacci) - 1):
        quotient, remainder = divmod(order - 23, 6)
        linear_width = 32 + 2 * quotient + (remainder >= 4)
        barrier_width = max(32, g_closed(linear_width))
        assert barrier_width <= linear_width <= arithmetic_fibonacci[order - 2]
        if order >= 25:
            previous_quotient, previous_remainder = divmod(order - 24, 6)
            previous_linear_width = 32 + 2 * previous_quotient + (previous_remainder >= 4)
            lower_quotient, lower_remainder = divmod(order - 25, 6)
            lower_linear_width = 32 + 2 * lower_quotient + (lower_remainder >= 4)
            assert max(32, g_closed(previous_linear_width)) <= lower_linear_width
        assert g_closed(arithmetic_fibonacci[order] + linear_width + 1) >= (
            arithmetic_fibonacci[order - 1] + g_closed(linear_width))
        if order in (23, 27, 29, 87, 100, 479):
            width_rows.append(dict(order=order, linear_width=linear_width,
                                   saturated_width=barrier_width))
    positive_report = dict(local_capped_split_contexts=local_contexts, periodic_split_witnesses=periodic_splits,
                extinction_table=extinction_rows, finite_conditional_C_rows=conditional_rows,
                finite_nonzero_persistence_rows=conditional_nonzero_rows,
                threshold_formula='K(u)=23+3*(u-32)+(u-32 mod2), u>=33',
                threshold_offsets_checked=[33, 1000], threshold_last=list(threshold_rows[-1]),
                higher_prefix_limit=higher_limit,
                higher_prefix_sha256=hashlib.sha256(','.join(map(str, higher_sequence[1:])).encode('ascii')).hexdigest(),
                higher_full_orbit_and_brent_agree=True, higher_literal_endpoint_updates=literal_updates,
                higher_threshold_cases=higher_cases, arithmetic_width_examples=width_rows,
                growing_linear_width='L_j=32+2*floor((j-23)/6)+indicator((j-23 mod6)>=4)',
                growing_saturated_width='W_j=max(32,G(L_j))',
                scope='General offset induction from the already certified0..32 collar and a necessary defect-persistence/phase rule. Finite Boolean paths are exhaustive for the rule envelope, not reverse-complete actual C histories. Every fixed positive width eventually has a proved exact collar; the separate moving-negative-plateau theorem supplies all fixed negative widths. Global ratio convergence remains open. Additional independent numerical checks stay within the previously published2^20 range, while the infinite conclusion comes from the extinction proof.')
    return positive_report, negative_collar_boundary_audit(higher_sequence, higher_splits, fibonacci)


def canonical_fibonacci_indices(value, fibonacci):
    remainder = value
    indices = []
    for order in range(len(fibonacci) - 1, 1, -1):
        if fibonacci[order] <= remainder:
            indices.append(order)
            remainder -= fibonacci[order]
    assert remainder == 0
    assert all(first - second >= 2 for first, second in zip(indices, indices[1:]))
    return tuple(indices)


def persistent_canonical_interaction_audit():
    patterns = ((0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 0, 1), (1, 0, 1))
    offsets = (0, 2, 3, 5, 7)
    fibonacci = fibonacci_values(1000)
    context_orders = range(8, 15)
    anchor_orders = [(3 * (fibonacci[order] - 3) + 1) // 2 for order in context_orders]
    while len(fibonacci) <= max(anchor_orders):
        fibonacci.append(fibonacci[-1] + fibonacci[-2])
    arithmetic_rows = []
    canonical_words = 0
    for context_order, anchor_order in zip(context_orders, anchor_orders):
        gap = fibonacci[context_order]
        anchor = fibonacci[anchor_order]
        context = anchor - gap
        zero_width = negative_plateau_width(anchor_order)
        unit_width = unit_defect_width(anchor_order)
        assert anchor_order >= context_order + 2 and anchor_order >= 27
        assert anchor_order % 3 != 1
        assert zero_width == gap - 6 and unit_width >= gap
        assert negative_plateau_width(anchor_order - 1) == gap - 7
        expected_high = (tuple(range(anchor_order - 1, context_order, -2))
                         if (anchor_order - context_order) % 2 == 0
                         else tuple(range(anchor_order - 1, context_order + 1, -2)) + (context_order - 1,))
        assert sum(fibonacci[order] for order in expected_high) == context
        assert min(expected_high) >= 7
        for pattern, offset in zip(patterns, offsets):
            indices = canonical_fibonacci_indices(context + offset, fibonacci)
            low = tuple(order for order in (5, 4, 3) if pattern[order - 3])
            assert indices == expected_high + low
            defect = int(gap - offset > zero_width)
            assert defect == 1 - pattern[0] * pattern[2]
            assert unit_defect_shift(anchor_order, gap - offset) == defect
            canonical_words += 1
        arithmetic_rows.append(dict(context_order=context_order, anchor_order=anchor_order,
                                    anchor_gap=gap, zero_width=zero_width, unit_width=unit_width,
                                    high_digit_count=len(expected_high), lowest_high_digit=min(expected_high),
                                    context_bit_length=context.bit_length(),
                                    predicted_interaction=1))
    witness_order = anchor_orders[0]
    witness_context_order = 8
    prefix_limit = fibonacci[witness_order]
    sequence, _, _, splits = generate(prefix_limit)
    assert sequence == brent_generate(prefix_limit)
    context = prefix_limit - fibonacci[witness_context_order]
    root_indices = [context + offset for offset in offsets]
    values = [sequence[index] for index in root_indices]
    cap = fibonacci[witness_order - 1]
    assert values == [cap - 1] * 4 + [cap]
    assert values[4] - values[1] - values[3] + values[0] == 1
    root_rows = []
    literal_updates = 0
    for pattern, index in zip(patterns, root_indices):
        trajectory, transient, period = full_orbit(sequence, index)
        point = index - 1
        depth = sequence[index - 1]
        for iteration in range(depth):
            point = index - sequence[point]
        literal_updates += depth
        assert point == splits[index] and period == 1
        root_rows.append(dict(pattern=''.join(map(str, pattern)), index=index, value=sequence[index],
                              canonical_indices=list(canonical_fibonacci_indices(index, fibonacci)),
                              depth=depth, transient=transient, period=period, selected_split=point))
    current_indices = root_indices[:]
    first_spine_steps = 0
    spine_rows = []
    spine_weights = [Fraction(1)] * 5
    for order in range(witness_order, 18, -1):
        cap = fibonacci[order - 1]
        values = [sequence[index] for index in current_indices]
        defects = [cap - value for value in values]
        assert defects == [1, 1, 1, 1, 0]
        assert values[4] - values[1] - values[3] + values[0] == 1
        gaps = [fibonacci[order] - index for index in current_indices]
        assert all(gap <= unit_defect_width(order) for gap in gaps)
        spine_rows.append(dict(anchor_order=order, gaps=gaps, cap=cap, values=values,
                               interaction=1, cap_normalized_interaction=str(Fraction(1, cap))))
        if order == 19:
            break
        following_indices = []
        for row, (index, gap) in enumerate(zip(current_indices, gaps)):
            shift = unit_defect_shift(order, gap)
            split = cap - gap + shift
            assert split == splits[index]
            assert sequence[index - split] == fibonacci[order - 3]
            following_indices.append(split)
            spine_weights[row] *= Fraction(split, index)
            first_spine_steps += 1
        current_indices = following_indices
    spine_probabilities = [str(Fraction(terminal, root))
                           for terminal, root in zip(current_indices, root_indices)]
    assert spine_probabilities == [str(weight) for weight in spine_weights]
    assert all(terminal <= fibonacci[19] for terminal in current_indices)
    return dict(arithmetic_context_orders_inclusive=[8, 14], canonical_words_checked=canonical_words,
                arithmetic_context_rows=arithmetic_rows,
                arithmetic_scope='Canonical Zeckendorf identities, legal seams and proved unit-family qualifications; no direct C evaluation at the large arithmetic contexts.',
                actual_prefix_limit=prefix_limit, full_orbit_and_brent_agree=True,
                prefix_sha256=hashlib.sha256(','.join(map(str, sequence[1:])).encode('ascii')).hexdigest(),
                actual_root_rows=root_rows, literal_selected_endpoint_updates=literal_updates,
                actual_first_spine_steps=first_spine_steps, inherited_pattern_spine_rows=spine_rows,
                terminal_first_spine_probabilities=spine_probabilities,
                persistent_interaction_formula='k_m=ceil(3*(F_m-3)/2), h_m=F_(k_m)-F_m; C(h_m+w(x))=F_(k_m-1)-1+x1*x3, m>=8',
                all_root_basins_fixed=True, descendant_interaction=1,
                cap_normalized_terminal_interaction=str(Fraction(1, fibonacci[18])),
                scope='Infinite canonical-index interaction follows from the unit-sublevel theorem and telescoping Zeckendorf identities. The explicit first family member and inherited-label first spines are independently checked. Root interaction does not imply a long orbit or a residual selector label; terminal signal persistence does not prove uniform dispersion because its size-biased first-spine probability tends to zero.')


def five_pattern_interaction_audit(sequence, fibonacci):
    patterns = ((0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 0, 1), (1, 0, 1))
    function_count = 0
    for values in product(range(-2, 3), repeat=5):
        baseline, first, middle, last, joint = values
        coefficients = (baseline, first - baseline, middle - baseline,
                        last - baseline, joint - first - last + baseline)
        for pattern, expected in zip(patterns, values):
            features = (1, *pattern, pattern[0] * pattern[2])
            assert sum(coefficient * feature for coefficient, feature
                       in zip(coefficients, features)) == expected
        function_count += 1
    rows = []
    for order in range(7, 27):
        values = [sequence[fibonacci[order] + offset] for offset in (0, 2, 3, 5, 7)]
        interaction = values[4] - values[1] - values[3] + values[0]
        if order >= 23:
            assert values == [fibonacci[order - 1] + offset for offset in (0, 2, 3, 5, 7)]
            assert interaction == 0
        rows.append(dict(order=order, anchor=fibonacci[order], values=values,
                         interaction=interaction))
    assert rows[2]['values'] == [21, 23, 24, 25, 28]
    assert rows[2]['interaction'] == 1
    assert rows[4]['interaction'] == 0 and rows[5]['interaction'] == 1
    return dict(patterns=['000', '100', '010', '001', '101'],
                exact_functions_reconstructed=function_count, responses=rows,
                universal_lowest_window_zero_interaction_orders='all j>=23',
                fixed_window_threshold='j>=max(3*i+7,K(F_(3*i+3)+F_(3*i+5)))',
                persistent_canonical_context=persistent_canonical_interaction_audit(),
                scope='Interpolation is elementary; infinite fixed-window vanishing follows from the proved positive collar. The digit alphabet is not an inner period-five orbit, and scalar additivity does not certify basin or selected phase.')


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
    positive_collars, negative_boundary = positive_collar_extinction_audit(sequence, fibonacci_values(10 ** 6))
    report = dict(
        status='Exact moving negative plateau, shelf-barrier seed and boundary arithmetic closure; two-collar and single-negative-seed premises and finite corroboration; orbit bounds use golden-proof.md, and exact-collars.md states the induction, propagation and boundary proofs; no Lean formalization.',
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
        saturated_fibonacci_profiles=saturated_profile_audit(sequence, periods, splits, fibonacci),
        growing_positive_collars=positive_collars,
        negative_fibonacci_boundary=negative_boundary,
        five_pattern_interaction=five_pattern_interaction_audit(sequence, fibonacci),
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

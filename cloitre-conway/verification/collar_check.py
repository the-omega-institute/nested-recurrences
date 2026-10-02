"""Corroborate the proved Fibonacci collar consequences by exact computation."""

import bisect
from array import array
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


def higher_cap_width(order, level):
    if level == 0:
        return negative_plateau_width(order)
    if level == 1:
        return unit_defect_width(order)
    if level == 2:
        return 8 * order // 3 - 18
    assert level == 3
    return 3 * order + (order - 1) // 3 - 24


def higher_cap_shift(order, gap):
    for level in range(4):
        frontier = higher_cap_width(order - 1, level)
        if gap <= frontier + level:
            return level
        if gap == frontier + level + 1:
            parity = int((int((order - 1) % 3 != 0) - level - 1) % 2 == 0)
            assert level < 3 or parity == 1
            return level + parity
    raise AssertionError('Gap lies outside the proved cap-defect0..3 domain')


def higher_cap_first_spine_gap(initial_order, initial_gap, target_order, level):
    assert 21 <= target_order <= initial_order
    assert level in (2, 3)
    assert higher_cap_width(initial_order, level - 1) < initial_gap <= higher_cap_width(initial_order, level)
    return max(higher_cap_width(target_order, level - 1) + 1,
               min(initial_gap - level * (initial_order - target_order),
                   higher_cap_width(target_order, level)))


def periodic_predecessor_gap(root_gap, seed_gap, profile, domain_upper=None):
    if domain_upper is None:
        domain_upper = root_gap
    if not 0 <= seed_gap <= domain_upper:
        return None
    point = seed_gap
    for period in range(1, domain_upper + 2):
        following = root_gap - profile(point)
        if following == seed_gap:
            return point, period
        if not 0 <= following <= domain_upper:
            return None
        point = following
    return None


def allocation_seed_candidates(order, gap, parent_cap, sequence, fibonacci):
    first_anchor = fibonacci[order - 1]
    first_cap = fibonacci[order - 2]
    second_anchor = fibonacci[order - 2]
    second_cap = fibonacci[order - 3]
    domain_upper = min(gap, fibonacci[order - 3])
    lower_profile = lambda point: first_cap - sequence[first_anchor - point]
    candidates = []
    first_minimum = 4 if order >= 22 else 0
    for allocation in range(parent_cap - first_minimum + 1):
        first_defect = parent_cap - allocation
        decoded = periodic_predecessor_gap(gap, gap - first_defect, lower_profile, domain_upper)
        if decoded is None:
            continue
        selected_gap, period = decoded
        second_gap = gap - selected_gap
        if not 0 <= second_gap <= fibonacci[order - 4]:
            continue
        if second_cap - sequence[second_anchor - second_gap] != allocation:
            continue
        assert lower_profile(selected_gap) == first_defect
        candidates.append(dict(second_cap_defect=allocation, first_cap_defect=first_defect,
                               selected_gap=selected_gap, selected_split=first_anchor - selected_gap,
                               period=period))
    return candidates


def cap4_generated_width(order):
    assert order >= 22
    return 4 * order - 19


def generated_cap4_profile(order, gap):
    assert 0 <= gap <= cap4_generated_width(order)
    return next((level for level in range(4) if gap <= higher_cap_width(order, level)), 4)


def cap4_band_first_spine_gap(initial_order, initial_gap, target_order):
    assert 22 <= target_order <= initial_order
    assert higher_cap_width(initial_order, 3) < initial_gap <= cap4_generated_width(initial_order)
    return max(higher_cap_width(target_order, 3) + 1,
               initial_gap - 4 * (initial_order - target_order))


def cap4_generated_band_audit(sequence, splits, fibonacci):
    base_order = 22
    base_lower = higher_cap_width(base_order, 3) + 1
    base_upper = cap4_generated_width(base_order)
    base_shifts = []
    literal_updates = 0
    for gap in range(base_lower, base_upper + 1):
        root = fibonacci[base_order] - gap
        assert fibonacci[base_order - 1] - sequence[root] == 4
        endpoint = root - 1
        for iteration in range(sequence[root - 1]):
            endpoint = root - sequence[endpoint]
        assert endpoint == splits[root]
        assert sequence[endpoint] + sequence[root - endpoint] == fibonacci[base_order - 1] - 4
        base_shifts.append(endpoint - (fibonacci[base_order - 1] - gap))
        literal_updates += sequence[root - 1]
    projection_cases = 0
    completion_graphs = 0
    for initial_order in range(23, 121):
        for initial_gap in range(higher_cap_width(initial_order, 3) + 1,
                                 cap4_generated_width(initial_order) + 1):
            gap = initial_gap
            for target_order in range(initial_order, 21, -1):
                assert gap == cap4_band_first_spine_gap(initial_order, initial_gap, target_order)
                assert generated_cap4_profile(target_order, gap) == 4
                projection_cases += 1
                if target_order > 22:
                    frontier = higher_cap_width(target_order - 1, 3)
                    shift = 3 if gap == frontier + 4 else 4
                    assert shift == 4 or target_order % 3 != 1
                    gap -= shift
            if initial_order > 60:
                continue
            frontier = higher_cap_width(initial_order - 1, 3)
            known_width = cap4_generated_width(initial_order - 1)
            expected_cycle = ({frontier, frontier + 1} if initial_gap == frontier + 4
                              else {initial_gap - 4})
            for completion_kind in range(3):
                profile = []
                for point in range(initial_gap + 1):
                    if point <= known_width:
                        defect = generated_cap4_profile(initial_order - 1, point)
                    else:
                        maximum = max(4, point - frontier - 1)
                        defect = (4 if completion_kind == 0 else maximum if completion_kind == 1
                                  else 4 + (point - known_width) % (maximum - 3))
                    assert 0 <= defect <= 2 * point // 3
                    profile.append(defect)
                cycles = capped_profile_cycles(profile, initial_gap)
                assert len(cycles) == 1 and set(cycles[0]) == expected_cycle
                completion_graphs += 1
    actual_roots = 0
    actual_spine_states = 0
    basin_phases = 0
    minimum_ratio = None
    for order in range(23, 31):
        first_cap = fibonacci[order - 2]
        second_cap = fibonacci[order - 3]
        for gap in range(higher_cap_width(order, 3) + 1, cap4_generated_width(order) + 1):
            root = fibonacci[order] - gap
            assert sequence[root] == fibonacci[order - 1] - 4
            selected_gap = cap4_band_first_spine_gap(order, gap, order - 1)
            assert splits[root] == fibonacci[order - 1] - selected_gap
            assert gap - selected_gap in (3, 4)
            assert first_cap - sequence[splits[root]] == 4
            assert second_cap - sequence[root - splits[root]] == 0
            current = root
            for target_order in range(order, 21, -1):
                predicted_gap = cap4_band_first_spine_gap(order, gap, target_order)
                assert current == fibonacci[target_order] - predicted_gap
                assert sequence[current] == fibonacci[target_order - 1] - 4
                actual_spine_states += 1
                if target_order > 22:
                    current = splits[current]
            trajectory, transient, period = full_orbit(sequence, root)
            cycle = trajectory[transient:]
            assert period == (2 if gap == higher_cap_width(order - 1, 3) + 4 else 1)
            for first in cycle:
                second = root - first
                numerator = first_cap * second - second_cap * first
                assert 25 * numerator * numerator >= gap * gap * first * second
                ratio = Fraction(numerator * numerator, gap * gap * first * second)
                minimum_ratio = ratio if minimum_ratio is None else min(minimum_ratio, ratio)
                basin_phases += 1
            actual_roots += 1
    witness_order = 30
    witness_gap = 92
    witness_root = fibonacci[witness_order] - witness_gap
    trajectory, transient, period = full_orbit(sequence, witness_root)
    assert period == 1 and splits[witness_root] == fibonacci[29] - 88
    endpoint = witness_root - 1
    for iteration in range(sequence[witness_root - 1]):
        endpoint = witness_root - sequence[endpoint]
    assert endpoint == splits[witness_root]
    literal_updates += sequence[witness_root - 1]
    actual_excluded_model = dict(order=witness_order, root=witness_root, gap=witness_gap,
                                value=sequence[witness_root], depth=sequence[witness_root - 1],
                                selected=endpoint, selected_gap=88, period=period,
                                transient=transient, seed_query_cap=4,
                                scope='Actual nesting fixes the PR22 model seed response at4; its hypothetical responses10..15 are excluded at this actual index.')
    offsets = [0, 2, 3, 5, 7]
    finite_order = 26
    finite_gap = higher_cap_width(finite_order, 3) + 6
    finite_base = fibonacci[finite_order] - finite_gap
    finite_values = [sequence[finite_base + offset] for offset in offsets]
    assert [fibonacci[finite_order - 1] - value for value in finite_values] == [4, 4, 4, 4, 3]
    assert finite_values[4] - finite_values[1] - finite_values[3] + finite_values[0] == 1
    finite_children = [splits[finite_base + offset] - (fibonacci[finite_order - 1] - finite_gap)
                       for offset in offsets]
    assert finite_children == [4, 6, 7, 8, 10]
    finite_alphabet = sorted(set(offsets + finite_children))
    assert len(finite_alphabet) == 9
    for offset in offsets:
        root = finite_base + offset
        digits = set(canonical_fibonacci_indices(root, fibonacci))
        expected_digits = set(canonical_fibonacci_indices(finite_base, fibonacci))
        expected_digits.update(canonical_fibonacci_indices(offset, fibonacci))
        assert digits == expected_digits
        endpoint = root - 1
        for iteration in range(sequence[root - 1]):
            endpoint = root - sequence[endpoint]
        assert endpoint == splits[root]
        literal_updates += sequence[root - 1]
    finite_child_digits = []
    finite_child_base = fibonacci[finite_order - 1] - finite_gap
    for offset, child_offset in zip(offsets, finite_children):
        physical = splits[finite_base + offset]
        digits = set(canonical_fibonacci_indices(physical, fibonacci))
        expected_digits = set(canonical_fibonacci_indices(finite_child_base, fibonacci))
        expected_digits.update(canonical_fibonacci_indices(child_offset, fibonacci))
        assert digits == expected_digits
        finite_child_digits.append([int(position in digits) for position in range(2, 7)])
    digit_interactions = [finite_child_digits[4][position] - finite_child_digits[1][position]
                          - finite_child_digits[3][position] + finite_child_digits[0][position]
                          for position in range(5)]
    assert digit_interactions == [0, 1, 1, -1, 0]
    assert sum(fibonacci[position + 2] * coefficient
               for position, coefficient in enumerate(digit_interactions)) == 0
    assert finite_children[4] - finite_children[1] - finite_children[3] + finite_children[0] == 0
    finite_descendants = [finite_base + offset for offset in offsets]
    finite_spine_rows = []
    for target_order in range(finite_order, 21, -1):
        values = [sequence[physical] for physical in finite_descendants]
        assert [fibonacci[target_order - 1] - value for value in values] == [4, 4, 4, 4, 3]
        assert values[4] - values[1] - values[3] + values[0] == 1
        finite_spine_rows.append(dict(order=target_order,
                                      gaps=[fibonacci[target_order] - physical for physical in finite_descendants],
                                      inherited_scalar_interaction=1,
                                      distinct_physical_indices=len(set(finite_descendants))))
        if target_order > 22:
            finite_descendants = [splits[physical] for physical in finite_descendants]
    family_fibonacci = [0, 1]
    while len(family_fibonacci) <= 199:
        family_fibonacci.append(sum(family_fibonacci[-2:]))
    assert family_fibonacci[60] % 10 == 0 and family_fibonacci[61] % 10 == 1
    family_rows = []
    inherited_pattern_states = 0
    for fibonacci_order in range(19, 200, 60):
        gap = family_fibonacci[fibonacci_order]
        assert gap % 10 == 1
        order = 3 * ((gap + 19) // 10)
        assert order >= 23 and order >= fibonacci_order + 2 and order % 3 == 0
        assert higher_cap_width(order, 3) == gap - 6
        defects = [generated_cap4_profile(order, gap - offset) for offset in offsets]
        assert defects == [4, 4, 4, 4, 3]
        child_offsets = []
        for offset, defect in zip(offsets, defects):
            root_gap = gap - offset
            child_gap = (cap4_band_first_spine_gap(order, root_gap, order - 1) if defect == 4
                         else root_gap - higher_cap_shift(order, root_gap))
            child_offsets.append(gap - child_gap)
        assert child_offsets == [4, 6, 7, 8, 10]
        for pattern, child_offset in zip(((0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 0, 1), (1, 0, 1)),
                                         child_offsets):
            first_bit, middle_bit, last_bit = pattern
            digits = set(canonical_fibonacci_indices(child_offset, family_fibonacci))
            expected = [1 - middle_bit - last_bit, middle_bit + first_bit * last_bit,
                        1 - first_bit - middle_bit - last_bit + first_bit * last_bit,
                        first_bit + middle_bit - first_bit * last_bit, last_bit]
            assert [int(position in digits) for position in range(2, 7)] == expected
        alphabet = sorted(set(offsets + child_offsets))
        assert alphabet == [0, 2, 3, 4, 5, 6, 7, 8, 10]
        for target_order in (order, order - 1, order - 2, order - 9, order - 20, 22):
            descendant_defects = []
            descendant_gaps = []
            for offset, defect in zip(offsets, defects):
                descendant_gap = (cap4_band_first_spine_gap(order, gap - offset, target_order)
                                  if defect == 4 else higher_cap_first_spine_gap(
                                      order, gap - offset, target_order, 3))
                descendant_defects.append(generated_cap4_profile(target_order, descendant_gap))
                descendant_gaps.append(descendant_gap)
                inherited_pattern_states += 1
            assert descendant_defects == defects
            if target_order == 22:
                assert descendant_gaps == [50, 50, 50, 50, 49]
        family_rows.append(dict(fibonacci_order=fibonacci_order, gap=gap, anchor_order=order,
                                root_cap_defects=defects, selected_child_offsets=child_offsets,
                                one_edge_alphabet=alphabet, one_edge_label_bits=4,
                                persistent_inherited_interaction=1))
    return dict(base_order=base_order, base_gap_interval_inclusive=[base_lower, base_upper],
                base_cap4_value=fibonacci[21] - 4, base_selected_shifts=base_shifts,
                propagated_width='4K-19, K>=22; a certified initial band, not the full cap4 support',
                arithmetic_projection_orders_inclusive=[23, 120], arithmetic_projection_cases=projection_cases,
                synthetic_completion_graph_orders_inclusive=[23, 60], synthetic_completion_graphs=completion_graphs,
                actual_band_orders_inclusive=[23, 30], actual_cap4_roots=actual_roots,
                actual_first_spine_states=actual_spine_states, actual_basin_phases=basin_phases,
                basin_quadratic_constant='1/25', minimum_basin_quadratic_ratio=str(minimum_ratio),
                actual_model_seed_exclusion=actual_excluded_model,
                finite_canonical_window=dict(order=finite_order, gap=finite_gap, base=finite_base,
                                             values=finite_values, selected_child_offsets=finite_children,
                                             one_edge_alphabet=finite_alphabet, one_edge_label_bits=4,
                                             selected_child_digits_F2_through_F6=finite_child_digits,
                                             selected_child_digit_interactions=digit_interactions,
                                             selected_child_offset_interaction=0,
                                             inherited_pattern_spine_rows=finite_spine_rows),
                symbolic_canonical_family_rows=family_rows, symbolic_inherited_pattern_states=inherited_pattern_states,
                canonical_child_numeric_map='4+2*x1+3*x2+4*x3; interaction0',
                canonical_child_digit_interactions_F2_through_F6=[0, 1, 1, -1, 0],
                canonical_family_terminal_gaps_at_order22=[50, 50, 50, 50, 49],
                literal_endpoint_updates=literal_updates,
                scope='The certified20-value base band propagates by the cap3 shelf; profile values, selected shifts and descendants are arithmetic to order22. The canonical family m=19 mod60 has a persistent interaction and a nine-symbol one-edge alphabet including F6. Symbolic rows do not directly evaluate C at huge Fibonacci orders; four-bit label packing is not an independent selector-input lower bound. Full cap4 support, wide-block profiles, high-cap allocations and uniform dispersion remain open.')


def bounded_tail_height(order, gap):
    assert order >= 24 and gap > cap4_generated_width(order)
    return max(4 if order >= 26 else 9, gap - cap4_generated_width(order))


def bounded_tail_cycle_height(order, gap):
    assert order >= 25 and gap > cap4_generated_width(order)
    return max(4 if order >= 27 else 9, gap - cap4_generated_width(order))


def zero_allocation_collar_width(order):
    assert order >= 25
    return cap4_generated_width(order) + negative_plateau_width(order - 2)


def bounded_tail_dispersion_width(order):
    assert order >= 25
    width = cap4_generated_width(order)
    return width + (width - 2) // 5


def three_symbol_tail_predecessor(excess, parent_cap, word):
    assert 1 <= excess <= 13 and parent_cap in (4, 8, 9)
    assert len(word) == 5 and set(word) <= {4, 8, 9}
    seed = excess + 4 - parent_cap
    if not 0 <= seed <= excess:
        return None
    point = seed
    for period in range(1, 4):
        assert 0 <= point <= excess
        defect = 4 if point <= 8 else word[point - 9]
        following = excess + 4 - defect
        if following == seed:
            return point, period
        point = following
        if not 0 <= point <= excess:
            return None
    return None


def actual_thirteen_tail_word(order):
    assert order >= 26
    boundary = {26: (8, 4, 9, 9, 8), 27: (8, 4, 4, 9, 8),
                28: (4, 4, 4, 4, 8), 29: (4, 4, 4, 4, 8)}
    return boundary.get(order, (4, 4, 4, 4, 4))


def actual_thirteen_tail_selector(order, excess):
    assert order >= 27 and 1 <= excess <= 13
    parent_cap = 4 if excess <= 8 else actual_thirteen_tail_word(order)[excess - 9]
    decoded = three_symbol_tail_predecessor(excess, parent_cap, actual_thirteen_tail_word(order - 1))
    assert decoded is not None
    selected_excess, period = decoded
    return cap4_generated_width(order - 1) + selected_excess, parent_cap, period


def bounded_tail_shelf_audit(sequence, splits, fibonacci):
    base_order = 24
    base_width = cap4_generated_width(base_order)
    base_values = []
    literal_updates = 0
    for gap in range(base_width + 1, 3 * base_width):
        root = fibonacci[base_order] - gap
        defect = fibonacci[base_order - 1] - sequence[root]
        assert 4 <= defect <= bounded_tail_height(base_order, gap)
        endpoint = root - 1
        for iteration in range(sequence[root - 1]):
            endpoint = root - sequence[endpoint]
        assert endpoint == splits[root]
        assert sequence[endpoint] + sequence[root - endpoint] == sequence[root]
        base_values.append(defect)
        literal_updates += sequence[root - 1]
    strengthened_base_values = []
    ternary_base_values = []
    for excess in range(1, 14):
        root = fibonacci[26] - cap4_generated_width(26) - excess
        defect = fibonacci[25] - sequence[root]
        assert defect == (4 if excess <= 8 else [8, 4, 9, 9, 8][excess - 9])
        endpoint = root - 1
        for iteration in range(sequence[root - 1]):
            endpoint = root - sequence[endpoint]
        assert endpoint == splits[root]
        assert sequence[endpoint] + sequence[root - endpoint] == sequence[root]
        if excess <= 8:
            strengthened_base_values.append(defect)
        else:
            ternary_base_values.append(defect)
        literal_updates += sequence[root - 1]
    lower_bound_positions = 0
    for order in range(23, 29):
        for gap in range(fibonacci[order - 2] + 1):
            defect = fibonacci[order - 1] - sequence[fibonacci[order] - gap]
            assert defect <= max(0, gap - 12)
            lower_bound_positions += 1
    symbolic_inequalities = 0
    synthetic_graphs = 0
    synthetic_phases = 0
    for order in range(25, 101):
        width = cap4_generated_width(order)
        previous_width = cap4_generated_width(order - 1)
        frontier = higher_cap_width(order - 1, 3)
        for excess in range(1, 121):
            gap = width + excess
            height = bounded_tail_cycle_height(order, gap)
            for point in range(frontier + 1, gap - 3):
                complement = gap - point
                if point <= previous_width:
                    if complement > height:
                        continue
                    upper = 4 + max(0, complement - 12)
                else:
                    upper = bounded_tail_height(order - 1, point) + max(0, complement - 12)
                assert upper <= height
                symbolic_inequalities += 1
            if order > 55 or excess > 60:
                continue
            for completion_kind in range(3):
                profile = []
                for point in range(gap + 1):
                    if point <= previous_width:
                        defect = generated_cap4_profile(order - 1, point)
                    elif order >= 27 and point <= previous_width + 8:
                        defect = 4
                    else:
                        upper = min(bounded_tail_height(order - 1, point),
                                    max(4, point - frontier - 1), 2 * point // 3)
                        defect = (4 if completion_kind == 0 else upper if completion_kind == 1
                                  else 4 + (point - previous_width) % (upper - 3))
                    profile.append(defect)
                cycles = capped_profile_cycles(profile, gap)
                periodic_readouts = []
                for cycle in cycles:
                    assert len(cycle) <= height - 3
                    for point in cycle:
                        complement = gap - point
                        defect = profile[point]
                        assert frontier < point <= gap - 4
                        assert 4 <= defect <= height and 4 <= complement <= height
                        lower_upper = (0 if complement <= negative_plateau_width(order - 2)
                                       else max(0, complement - 12))
                        assert defect + lower_upper <= height
                        periodic_readouts.append(defect)
                        synthetic_phases += 1
                assert len(periodic_readouts) == len(set(periodic_readouts)) <= height - 3
                synthetic_graphs += 1
    full_block_positions = 0
    zero_allocation_roots = 0
    zero_allocation_phases = 0
    dispersion_phases = 0
    descendant_states = 0
    minimum_ratio = None
    actual_rows = []
    actual_witnesses = {}
    for order in range(24, 31):
        width = cap4_generated_width(order)
        for gap in range(fibonacci[order - 2] + 1):
            defect = fibonacci[order - 1] - sequence[fibonacci[order] - gap]
            if gap > width:
                assert 4 <= defect <= bounded_tail_height(order, gap)
            if order >= 26 and width < gap <= width + 8:
                assert defect == 4
            full_block_positions += 1
        if order == 24:
            continue
        cap_counts = {}
        period_counts = {}
        for gap in range(width + 1, bounded_tail_dispersion_width(order) + 1):
            root = fibonacci[order] - gap
            height = bounded_tail_cycle_height(order, gap)
            profile = [fibonacci[order - 2] - sequence[fibonacci[order - 1] - point]
                       for point in range(gap + 1)]
            cycles = capped_profile_cycles(profile, gap)
            readouts = []
            for cycle in cycles:
                for point in cycle:
                    first = fibonacci[order - 1] - point
                    second = root - first
                    shift = gap - point
                    assert 4 <= profile[point] <= height and 4 <= shift <= height
                    assert gap >= 6 * shift + 2
                    numerator = fibonacci[order - 2] * second - fibonacci[order - 3] * first
                    assert 25 * numerator * numerator >= gap * gap * first * second
                    ratio = Fraction(numerator * numerator, gap * gap * first * second)
                    minimum_ratio = ratio if minimum_ratio is None else min(minimum_ratio, ratio)
                    readouts.append(profile[point])
                    dispersion_phases += 1
                    if gap <= zero_allocation_collar_width(order):
                        assert fibonacci[order - 3] - sequence[second] == 0
                        zero_allocation_phases += 1
            assert len(readouts) == len(set(readouts)) <= height - 3
            if gap > zero_allocation_collar_width(order):
                continue
            parent_cap = fibonacci[order - 1] - sequence[root]
            selected_gap, period = periodic_predecessor_gap(gap, gap - parent_cap, profile.__getitem__)
            assert splits[root] == fibonacci[order - 1] - selected_gap
            options = allocation_seed_candidates(order, gap, parent_cap, sequence, fibonacci)
            assert len(options) == 1 and options[0]['second_cap_defect'] == 0
            excess = gap - width
            current = root
            current_order = order
            while current_order >= 25 and negative_plateau_width(current_order - 2) >= max(9, excess):
                current_gap = fibonacci[current_order] - current
                assert current_gap - cap4_generated_width(current_order) <= excess
                assert fibonacci[current_order - 1] - sequence[current] == parent_cap
                first = splits[current]
                second = current - first
                assert fibonacci[current_order - 3] - sequence[second] == 0
                descendant_states += 1
                current = first
                current_order -= 1
                if current_gap <= cap4_generated_width(current_order + 1):
                    break
            cap_counts[str(parent_cap)] = cap_counts.get(str(parent_cap), 0) + 1
            period_counts[str(period)] = period_counts.get(str(period), 0) + 1
            actual_witnesses.setdefault(str(parent_cap), dict(order=order, gap=gap, root=root,
                                                             parent_cap=parent_cap,
                                                             shift=gap - selected_gap, period=period,
                                                             selected=splits[root]))
            zero_allocation_roots += 1
        actual_rows.append(dict(order=order, maximum_gap=zero_allocation_collar_width(order),
                                cap_counts=cap_counts, period_counts=period_counts))
    complete_word_graphs = 0
    complete_word_decodings = 0
    word_descriptors = set()
    for word in product((4, 8, 9), repeat=5):
        descriptor = []
        for excess in range(9, 14):
            profile = [word[point - 9] if 9 <= point <= 13 else 4
                       for point in range(excess + 5)]
            cycles = capped_profile_cycles(profile, excess + 4)
            vertices = [point for cycle in cycles for point in cycle]
            assert len(vertices) <= 3 and set(vertices) <= {excess, excess - 4, excess - 5}
            options = {profile[point]: point for point in vertices}
            assert len(options) == len(vertices)
            for parent_cap in (4, 8, 9):
                decoded = three_symbol_tail_predecessor(excess, parent_cap, word)
                if parent_cap in options:
                    assert decoded is not None and decoded[0] == options[parent_cap]
                else:
                    assert decoded is None
                descriptor.append(None if decoded is None else decoded[0])
                complete_word_decodings += 1
            complete_word_graphs += 1
        word_descriptors.add(tuple(descriptor))
    assert len(word_descriptors) == 243
    ternary_rows = []
    ternary_selected_roots = 0
    ternary_periodic_phases = 0
    ternary_spine_states = 0
    inherited_window_states = 0
    for order in range(26, 31):
        width = cap4_generated_width(order)
        word = [fibonacci[order - 1] - sequence[fibonacci[order] - width - excess]
                for excess in range(9, 14)]
        assert set(word) <= {4, 8, 9}
        assert tuple(word) == actual_thirteen_tail_word(order)
        ternary_rows.append(dict(order=order, response_word=word))
        if 27 <= order <= 29:
            for excess in range(9, 14):
                root = fibonacci[order] - width - excess
                endpoint = root - 1
                for iteration in range(sequence[root - 1]):
                    endpoint = root - sequence[endpoint]
                assert endpoint == splits[root]
                assert sequence[endpoint] + sequence[root - endpoint] == sequence[root]
                literal_updates += sequence[root - 1]
        if order == 26:
            continue
        previous_word = [fibonacci[order - 2] - sequence[
            fibonacci[order - 1] - cap4_generated_width(order - 1) - excess]
                         for excess in range(9, 14)]
        for excess in range(1, 14):
            gap = width + excess
            root = fibonacci[order] - gap
            parent_cap = fibonacci[order - 1] - sequence[root]
            assert parent_cap == (4 if excess <= 8 else word[excess - 9])
            decoded = three_symbol_tail_predecessor(excess, parent_cap, previous_word)
            assert decoded is not None
            selected_excess, period = decoded
            assert actual_thirteen_tail_selector(order, excess) == (
                cap4_generated_width(order - 1) + selected_excess, parent_cap, period)
            assert splits[root] == fibonacci[order - 1] - cap4_generated_width(order - 1) - selected_excess
            profile = [fibonacci[order - 2] - sequence[fibonacci[order - 1] - point]
                       for point in range(gap + 1)]
            cycles = capped_profile_cycles(profile, gap)
            vertices = [point for cycle in cycles for point in cycle]
            allowed = {excess} if excess <= 8 else {excess, excess - 4, excess - 5}
            assert len(vertices) <= 3
            for point in vertices:
                assert point - cap4_generated_width(order - 1) in allowed
                assert profile[point] in (4, 8, 9)
                ternary_periodic_phases += 1
            current = root
            for target_order in range(order, 25, -1):
                current_excess = fibonacci[target_order] - current - cap4_generated_width(target_order)
                assert 1 <= current_excess <= excess
                assert fibonacci[target_order - 1] - sequence[current] == parent_cap
                ternary_spine_states += 1
                if target_order > 26:
                    second = current - splits[current]
                    assert sequence[second] == fibonacci[target_order - 3]
                    current = splits[current]
            ternary_selected_roots += 1
        for excess in range(9, 14):
            roots = [fibonacci[order] - width - excess + offset for offset in (0, 2, 3, 5, 7)]
            values = [sequence[root] for root in roots]
            interaction = values[4] - values[1] - values[3] + values[0]
            assert interaction == sequence[roots[0]] - sequence[roots[1]]
            assert interaction in (-5, -4, -1, 0, 1, 4, 5)
            for target_order in range(order, 25, -1):
                values = [sequence[root] for root in roots]
                assert values[4] - values[1] - values[3] + values[0] == interaction
                inherited_window_states += 5
                if target_order > 26:
                    roots = [splits[root] for root in roots]
    terminal_flat_values = []
    for excess in range(9, 17):
        root = fibonacci[30] - cap4_generated_width(30) - excess
        assert fibonacci[29] - sequence[root] == 4
        endpoint = root - 1
        for iteration in range(sequence[root - 1]):
            endpoint = root - sequence[endpoint]
        assert endpoint == splits[root]
        assert sequence[endpoint] + sequence[root - endpoint] == sequence[root]
        terminal_flat_values.append(4)
        literal_updates += sequence[root - 1]
    late_arithmetic_states = 0
    for order in range(31, 121):
        assert actual_thirteen_tail_word(order) == (4, 4, 4, 4, 4)
        for excess in range(1, 14):
            assert actual_thirteen_tail_selector(order, excess) == (
                cap4_generated_width(order - 1) + excess, 4, 1)
            late_arithmetic_states += 1
    window_order = 26
    window_gap = 97
    window_base = fibonacci[window_order] - window_gap
    window_offsets = [0, 2, 3, 5, 7]
    window_caps = [fibonacci[window_order - 1] - sequence[window_base + offset]
                   for offset in window_offsets]
    assert window_caps == [9, 4, 8, 4, 4]
    higher_digits = set(canonical_fibonacci_indices(window_base, fibonacci))
    assert min(higher_digits) >= 7
    word = [fibonacci[window_order - 2] - sequence[
        fibonacci[window_order - 1] - cap4_generated_width(window_order - 1) - position]
            for position in range(1, 13)]
    assert word == [4, 4, 4, 4, 4, 4, 9, 4, 8, 8, 9, 9]
    def shared_profile(point):
        previous_width = cap4_generated_width(window_order - 1)
        if point <= previous_width:
            return generated_cap4_profile(window_order - 1, point)
        assert 1 <= point - previous_width <= len(word)
        return word[point - previous_width - 1]
    window_children = []
    for offset, defect in zip(window_offsets, window_caps):
        root = window_base + offset
        assert set(canonical_fibonacci_indices(root, fibonacci)) == higher_digits | set(
            canonical_fibonacci_indices(offset, fibonacci))
        selected_gap, period = periodic_predecessor_gap(window_gap - offset,
                                                       window_gap - offset - defect, shared_profile)
        assert splits[root] == fibonacci[window_order - 1] - selected_gap
        endpoint = root - 1
        for iteration in range(sequence[root - 1]):
            endpoint = root - sequence[endpoint]
        assert endpoint == splits[root]
        literal_updates += sequence[root - 1]
        window_children.append(window_gap - selected_gap)
    assert window_children == [9, 10, 7, 14, 11]
    window_spine = []
    current_roots = [window_base + offset for offset in window_offsets]
    for order in range(26, 23, -1):
        values = [sequence[root] for root in current_roots]
        assert [fibonacci[order - 1] - value for value in values] == window_caps
        interaction = values[4] - values[1] - values[3] + values[0]
        assert interaction == -5
        window_spine.append(dict(order=order, gaps=[fibonacci[order] - root for root in current_roots],
                                 inherited_scalar_interaction=interaction))
        if order > 24:
            current_roots = [splits[root] for root in current_roots]
    late_order = 29
    late_gap = 110
    late_base = fibonacci[late_order] - late_gap
    late_higher_digits = set(canonical_fibonacci_indices(late_base, fibonacci))
    assert min(late_higher_digits) >= 7
    late_caps = [fibonacci[late_order - 1] - sequence[late_base + offset] for offset in window_offsets]
    assert late_caps == [8, 4, 4, 4, 4]
    late_word = [fibonacci[late_order - 2] - sequence[
        fibonacci[late_order - 1] - cap4_generated_width(late_order - 1) - position]
                 for position in range(9, 14)]
    assert late_word == [4, 4, 4, 4, 8]
    def late_shared_profile(point):
        previous_width = cap4_generated_width(late_order - 1)
        if point <= previous_width:
            return generated_cap4_profile(late_order - 1, point)
        if point <= previous_width + 8:
            return 4
        assert 9 <= point - previous_width <= 13
        return late_word[point - previous_width - 9]
    late_children = []
    for offset, defect in zip(window_offsets, late_caps):
        root = late_base + offset
        assert set(canonical_fibonacci_indices(root, fibonacci)) == late_higher_digits | set(
            canonical_fibonacci_indices(offset, fibonacci))
        selected_gap, period = periodic_predecessor_gap(late_gap - offset,
                                                       late_gap - offset - defect, late_shared_profile)
        assert splits[root] == fibonacci[late_order - 1] - selected_gap
        endpoint = root - 1
        for iteration in range(sequence[root - 1]):
            endpoint = root - sequence[endpoint]
        assert endpoint == splits[root]
        literal_updates += sequence[root - 1]
        late_children.append(late_gap - selected_gap)
    assert late_children == [4, 6, 7, 9, 11]
    late_spine = []
    current_roots = [late_base + offset for offset in window_offsets]
    for order in range(late_order, 25, -1):
        values = [sequence[root] for root in current_roots]
        assert [fibonacci[order - 1] - value for value in values] == late_caps
        interaction = values[4] - values[1] - values[3] + values[0]
        assert interaction == -4
        late_spine.append(dict(order=order, gaps=[fibonacci[order] - root for root in current_roots],
                               inherited_scalar_interaction=interaction))
        if order > 26:
            current_roots = [splits[root] for root in current_roots]
    capacities = []
    late_capacities = []
    for width in (1, 5, 9, 12, 24):
        capacity = 1
        for position in range(14, width + 1):
            capacity *= position - 3
        capacities.append(dict(tail_positions=width, relaxed_profile_words=capacity,
                               packed_bits=(capacity - 1).bit_length()))
        late_capacity = 1
        for position in range(17, width + 1):
            late_capacity *= position - 3
        late_capacities.append(dict(tail_positions=width, relaxed_profile_words=late_capacity,
                                    packed_bits=(late_capacity - 1).bit_length()))
    return dict(base_order=base_order, base_tail_gap_interval_inclusive=[base_width + 1, 3 * base_width - 1],
                base_tail_values=len(base_values), base_tail_sha256=hashlib.sha256(
                    ','.join(map(str, base_values)).encode('ascii')).hexdigest(),
                literal_endpoint_updates=literal_updates,
                shelf_formula='4<=Q_K(v)<=max(9,v-(4K-19)) for K>=24; sharper max(4,v-(4K-19)) for K>=26',
                strengthened_base_order=26, strengthened_base_gap_interval_inclusive=[86, 93],
                strengthened_base_values=strengthened_base_values,
                extended_generated_band='Q_K(V_K+j)=4 for1<=j<=8, K>=26; first spine keeps j to order26',
                ternary_base_gap_interval_inclusive=[94, 98], ternary_base_values=ternary_base_values,
                ternary_tail=dict(base_order=26, response_positions_inclusive=[9, 13],
                                  response_alphabet=[4, 8, 9], response_word_bits=8,
                                  complete_response_words=243, complete_word_graphs=complete_word_graphs,
                                  complete_word_decodings=complete_word_decodings,
                                  distinct_complete_option_descriptors=len(word_descriptors),
                                  actual_words=ternary_rows, actual_selected_roots=ternary_selected_roots,
                                  actual_periodic_phases=ternary_periodic_phases,
                                  actual_first_spine_states=ternary_spine_states,
                                  inherited_five_pattern_states=inherited_window_states,
                                  scalar_interaction_alphabet=[-5, -4, -1, 0, 1, 4, 5],
                                  terminal_flat_seed_order=30,
                                  terminal_flat_seed_gap_interval_inclusive=[110, 117],
                                  terminal_flat_seed_values=terminal_flat_values,
                                  eventual_generated_band='Q_K(V_K+j)=4 for1<=j<=16, K>=30; first spine keeps j above finite order30',
                                  explicit_word_boundary_orders_inclusive=[26, 29],
                                  explicit_word_late_orders_inclusive=[31, 120],
                                  explicit_word_late_symbolic_states=late_arithmetic_states,
                                  actual_residual_word_or_parent_cap_inputs=0,
                                  scope='Five order26 values start the actual ternary-alphabet induction; fifteen order27..29 entries give its boundary words. An eight-value order30 flat seed propagates the first16 tail entries. The actual thirteen-position word and selector are therefore arithmetic in the order and excess, with zero residual word/cap/phase inputs above finite order26. Eight bits is exact only for the larger complete relaxed option-table contract. The general wider tail response construction, full minimum and global closure remain open.'),
                lower_child_bound='Q_l(q)<=max(0,q-12), l>=23',
                lower_bound_positions=lower_bound_positions,
                symbolic_inequality_orders_inclusive=[25, 100], symbolic_inequalities=symbolic_inequalities,
                synthetic_graph_orders_inclusive=[25, 55], synthetic_graphs=synthetic_graphs,
                synthetic_periodic_phases=synthetic_phases,
                actual_full_block_orders_inclusive=[24, 30], full_block_positions=full_block_positions,
                zero_allocation_width='4K-19+L_(K-2), K>=25',
                zero_allocation_roots=zero_allocation_roots, zero_allocation_phases=zero_allocation_phases,
                first_spine_states=descendant_states, actual_tail_rows=actual_rows,
                actual_tail_cap_witnesses=actual_witnesses,
                dispersion_width='4K-19+floor((4K-21)/5), K>=25',
                all_periodic_dispersion_phases=dispersion_phases,
                quadratic_constant='1/25', minimum_quadratic_ratio=str(minimum_ratio),
                canonical_five_row_word=dict(order=window_order, gap=window_gap, base=window_base,
                                             cap_vector=window_caps, root_offsets=window_offsets,
                                             shared_lower_tail_responses=word,
                                             selected_child_offsets=window_children,
                                             inherited_first_spine=window_spine),
                late_canonical_five_row_word=dict(order=late_order, gap=late_gap, base=late_base,
                                                  cap_vector=late_caps, root_offsets=window_offsets,
                                                  residual_positions_inclusive=[9, 13],
                                                  shared_lower_tail_responses=late_word,
                                                  selected_child_offsets=late_children,
                                                  inherited_first_spine=late_spine),
                relaxed_tail_profile_capacities=capacities,
                late_relaxed_tail_profile_capacities=late_capacities,
                scope='A153-value order24 shelf premise propagates height9; thirteen order26 values give height4, eight generated positions and a ternary tail. Fifteen order27..29 entries and an eight-value order30 flat seed supply the actual thirteen-position word explicitly and extend the generated band to16. At K>=27 only positions above13 remain unknown; at K>=31 only positions above16 remain unknown. Their height is max(4,D), with parent cap still supplied outside the generated profiles. Packing counts relaxed response words, not actual independent inputs or an optimal whole-recursion code. High-cap allocations and global dispersion/convergence remain open.')


def finite_tail_alphabet_audit(sequence, splits, fibonacci):
    base_order = 26
    tail_width = 47
    alphabet = {4, 7, 8, 9, 10, 13}
    seed_word = [4, 4, 4, 4, 4, 4, 4, 4, 8, 4, 9, 9, 8, 8, 9, 9,
                 8, 8, 8, 8, 8, 8, 8, 7, 7, 7, 7, 7, 7, 7, 7, 7,
                 8, 8, 8, 8, 8, 8, 9, 9, 8, 9, 9, 10, 10, 13, 9]
    assert len(seed_word) == tail_width and set(seed_word) == alphabet
    assert max(alphabet) == negative_plateau_width(base_order - 1)
    literal_updates = 0
    for excess, defect in enumerate(seed_word, 1):
        root = fibonacci[base_order] - cap4_generated_width(base_order) - excess
        assert fibonacci[base_order - 1] - sequence[root] == defect
        endpoint = root - 1
        for iteration in range(sequence[root - 1]):
            endpoint = root - sequence[endpoint]
        assert endpoint == splits[root]
        assert sequence[endpoint] + sequence[root - endpoint] == sequence[root]
        literal_updates += sequence[root - 1]
    synthetic_graphs = 0
    synthetic_phases = 0
    ordered_alphabet = sorted(alphabet)
    for order in range(27, 61):
        previous_width = cap4_generated_width(order - 1)
        for excess in range(1, tail_width + 1):
            gap = cap4_generated_width(order) + excess
            for completion_kind in range(len(alphabet) + 2):
                profile = [generated_cap4_profile(order - 1, point) if point <= previous_width
                           else ordered_alphabet[completion_kind] if completion_kind < len(alphabet)
                           else ordered_alphabet[((point - previous_width) *
                                                  (completion_kind - len(alphabet) + 1)) % len(alphabet)]
                           for point in range(gap + 1)]
                cycles = capped_profile_cycles(profile, gap)
                readouts = []
                for cycle in cycles:
                    for point in cycle:
                        shift = gap - point
                        assert point <= previous_width + excess
                        assert profile[point] in alphabet and shift in alphabet
                        assert shift <= negative_plateau_width(order - 2)
                        readouts.append(profile[point])
                        synthetic_phases += 1
                assert len(readouts) == len(set(readouts)) <= len(alphabet)
                synthetic_graphs += 1
    actual_roots = 0
    periodic_phases = 0
    high_cap_spine_states = 0
    strict_edges = 0
    copy_edges = 0
    observed_periods = {}
    for order in range(27, 31):
        width = cap4_generated_width(order)
        previous_width = cap4_generated_width(order - 1)
        profile = [fibonacci[order - 2] - sequence[fibonacci[order - 1] - point]
                   for point in range(width + tail_width + 1)]
        for excess in range(1, tail_width + 1):
            gap = width + excess
            root = fibonacci[order] - gap
            parent_cap = fibonacci[order - 1] - sequence[root]
            assert parent_cap in alphabet
            cycles = capped_profile_cycles(profile[:gap + 1], gap)
            readouts = []
            for cycle in cycles:
                for point in cycle:
                    shift = gap - point
                    first = fibonacci[order - 1] - point
                    second = fibonacci[order - 2] - shift
                    assert profile[point] in alphabet and shift in alphabet
                    assert fibonacci[order - 3] - sequence[second] == 0
                    assert gap >= 6 * shift + 2
                    numerator = fibonacci[order - 2] * second - fibonacci[order - 3] * first
                    assert 25 * numerator * numerator >= gap * gap * first * second
                    readouts.append(profile[point])
                    periodic_phases += 1
            assert len(readouts) == len(set(readouts)) <= len(alphabet)
            decoded = periodic_predecessor_gap(gap, gap - parent_cap, profile.__getitem__)
            assert decoded is not None and decoded[1] <= len(alphabet)
            selected_gap, period = decoded
            assert splits[root] == fibonacci[order - 1] - selected_gap
            observed_periods[str(period)] = observed_periods.get(str(period), 0) + 1
            if parent_cap > 4:
                current = root
                current_excess = excess
                current_strict = 0
                current_copies = 0
                for current_order in range(order, base_order, -1):
                    first = splits[current]
                    second = current - first
                    child_excess = fibonacci[current_order - 1] - first - cap4_generated_width(current_order - 1)
                    shift = current_excess + 4 - child_excess
                    assert fibonacci[current_order - 2] - sequence[first] == parent_cap
                    assert fibonacci[current_order - 3] - sequence[second] == 0
                    assert 1 <= child_excess <= current_excess and shift in alphabet
                    if child_excess == current_excess:
                        successor = current - sequence[first]
                        assert successor != first and current - sequence[successor] == first
                        assert fibonacci[current_order - 2] - sequence[successor] == 4
                        current_copies += 1
                        copy_edges += 1
                    else:
                        assert current_excess - child_excess >= 3
                        current_strict += 1
                        strict_edges += 1
                    high_cap_spine_states += 1
                    current = first
                    current_excess = child_excess
                assert current_strict <= 15
                assert current_copies >= max(0, order - base_order - 15)
            actual_roots += 1
    parity_witnesses = []
    for order, expected_cap, expected_clock, expected_depth in (
            (29, 8, 13, 317807), (30, 4, 14, 514225)):
        width = cap4_generated_width(order)
        root = fibonacci[order] - width - 13
        word = [fibonacci[order - 2] - sequence[
            fibonacci[order - 1] - cap4_generated_width(order - 1) - excess]
                for excess in range(1, 15)]
        assert word == [4] * 12 + [8, 4]
        trajectory, transient, period = full_orbit(sequence, root)
        assert transient == expected_clock and period == 2
        assert sequence[root - 1] == expected_depth and expected_depth % 2 == 1
        assert fibonacci[order - 1] % 2 == 1
        entry_excess = fibonacci[order - 1] - trajectory[transient] - cap4_generated_width(order - 1)
        selected_excess = fibonacci[order - 1] - splits[root] - cap4_generated_width(order - 1)
        assert entry_excess == 13 and selected_excess == (13 if expected_cap == 8 else 9)
        assert fibonacci[order - 1] - sequence[root] == expected_cap
        endpoint = root - 1
        for iteration in range(expected_depth):
            endpoint = root - sequence[endpoint]
        assert endpoint == splits[root]
        literal_updates += expected_depth
        parity_witnesses.append(dict(order=order, root=root, lower_word=word,
                                     first_anchor_parity=1, prescribed_depth=expected_depth,
                                     entry_clock=transient, entry_excess=entry_excess,
                                     selected_excess=selected_excess, parent_cap=expected_cap,
                                     phase_residue=(expected_depth - transient) % period))
    return dict(base_order=base_order, tail_positions=tail_width,
                base_gap_interval_inclusive=[86, 132], base_word=seed_word,
                base_word_sha256=hashlib.sha256(','.join(map(str, seed_word)).encode('ascii')).hexdigest(),
                response_alphabet=ordered_alphabet, maximum_response=13,
                literal_endpoint_updates=literal_updates,
                synthetic_orders_inclusive=[27, 60], synthetic_graphs=synthetic_graphs,
                synthetic_periodic_phases=synthetic_phases,
                actual_orders_inclusive=[27, 30], actual_roots=actual_roots,
                actual_periodic_phases=periodic_phases, actual_selected_period_counts=observed_periods,
                high_cap_first_spine_states=high_cap_spine_states,
                strict_excess_drop_edges=strict_edges, translated_excess_copy_edges=copy_edges,
                maximum_strict_drops_any_depth=15,
                copy_rule='Every zero-drop high-cap edge selects response state4 with readout e>4. It is a two-cycle exactly when H_d(e)=4; zero drop alone does not prove that extra response. The checked finite actual copies are two-cycles. All strict drops are at least3.',
                preceding_word_response_bits_Kge27=(6 ** 34 - 1).bit_length(),
                preceding_word_response_bits_Kge31=(6 ** 28 - 1).bit_length(),
                actual_parity_shortcut_counterexamples=parity_witnesses,
                quadratic_dispersion='constant1/25 for gaps0..V_K+max(47,floor((V_K-2)/5)), K>=27',
                scope='The47-value actual order26 seed propagates its alphabet at all orders>=26; every higher-order periodic phase has zero second cap and at most six periodic vertices. Wider words and parent caps remain supplied outside generated regions. High-cap spines have at most15 strict translated-excess drops, so arbitrarily long high spines require long zero-drop copy runs; two-cycle qualification is additional. Actual local-word/depth-parity collisions need entry clocks; these different-order examples are not independent-input lower bounds with full order supplied. Alphabet packing bounds are not exact actual costs. Seed26 internal allocation, copy-run control, wider profile construction and global dispersion/convergence remain outside this theorem.')


def even_anchor_landing(sequence, root, anchor):
    point = root - 1
    pairs = 0
    while point > anchor:
        following = root - sequence[point]
        point = root - sequence[following]
        pairs += 1
    return point, pairs


def frontier_reset_from_landing(order, excess, landing_gap, response):
    assert order >= 27 and 9 <= excess <= 43
    previous_width = cap4_generated_width(order - 1)
    frontier = higher_cap_width(order - 1, 3)
    high_gap = previous_width + excess
    assert 0 <= landing_gap <= high_gap and high_gap - frontier > 9
    if landing_gap == high_gap:
        return 1, None, None
    if landing_gap > frontier:
        return 0, None, None
    landing_cap = generated_cap4_profile(order - 1, landing_gap)
    assert 0 <= landing_cap <= 3
    query_excess = excess + 4 - landing_cap
    queried_cap = response(query_excess)
    assert queried_cap in (4, 7, 8, 9, 10, 13)
    return int(queried_cap == 4), query_excess, queried_cap


def frontier_reset_audit(sequence, splits, fibonacci):
    alphabet = (4, 7, 8, 9, 10, 13)
    offsets = (0, 2, 3, 5, 7)
    patterns = ((0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 0, 1), (1, 0, 1))
    symbolic_cases = 0
    symbolic_updates = 0
    branch_counts = {'high_member_landing': 0, 'cap4_band_landing': 0, 'one_tail_query': 0}
    for order in range(27, 61):
        previous_width = cap4_generated_width(order - 1)
        frontier = higher_cap_width(order - 1, 3)
        for excess in range(9, 44):
            gap = cap4_generated_width(order) + excess
            high_gap = previous_width + excess
            landing_gaps = sorted({0, negative_plateau_width(order - 1),
                                   unit_defect_width(order - 1), higher_cap_width(order - 1, 2),
                                   frontier, frontier + 1, high_gap - 1, high_gap})
            for high_cap in alphabet[1:]:
                if high_cap > excess:
                    continue
                for landing_gap in landing_gaps:
                    query_choices = alphabet if landing_gap <= frontier else (4,)
                    for queried_cap in query_choices:
                        if landing_gap <= frontier:
                            query_excess = excess + 4 - generated_cap4_profile(order - 1, landing_gap)
                            if queried_cap > query_excess:
                                continue
                        reset, query_excess, response_cap = frontier_reset_from_landing(
                            order, excess, landing_gap, lambda position: queried_cap)
                        def profile(point):
                            if point <= previous_width:
                                return generated_cap4_profile(order - 1, point)
                            if point < high_gap:
                                return 4
                            if point == high_gap:
                                return high_cap
                            assert query_excess is not None and point == previous_width + query_excess
                            return response_cap
                        for depth_parity in (0, 1):
                            point = landing_gap
                            for iteration in range(8 + depth_parity):
                                point = gap - profile(point)
                                symbolic_updates += 1
                            selected_high = depth_parity != reset
                            assert point == (gap - 4 if selected_high else gap - high_cap)
                            selected_cap = profile(point)
                            assert selected_cap == (high_cap if selected_high else 4)
                            values = [-selected_cap, -4, -4, -4, -4]
                            children = [gap - point, 6, 7, 9, 11]
                            scalar_joint = values[4] - values[1] - values[3] + values[0]
                            index_joint = children[4] - children[1] - children[3] + children[0]
                            assert scalar_joint == (4 - high_cap if selected_high else 0)
                            assert index_joint == (0 if selected_high else high_cap - 4)
                            assert index_joint - scalar_joint == high_cap - 4
                            for pattern, child, value in zip(patterns, children, values):
                                first_digit, second_digit, third_digit = pattern
                                polynomial = (-gap + high_cap + 4 + (6 - high_cap) * first_digit
                                              + (7 - high_cap) * second_digit + (9 - high_cap) * third_digit
                                              + (high_cap - 4) * first_digit * third_digit)
                                assert child - value - gap == polynomial
                            branch = ('high_member_landing' if landing_gap == high_gap
                                      else 'cap4_band_landing' if landing_gap > frontier else 'one_tail_query')
                            branch_counts[branch] += 1
                            symbolic_cases += 1
    actual_rows = []
    literal_updates = 0
    wall_positions = 0
    actual_pattern_rows = 0
    for order in range(27, 31):
        anchor = fibonacci[order - 1]
        first_cap = fibonacci[order - 2]
        previous_width = cap4_generated_width(order - 1)
        excess = next(position for position in range(1, 44)
                      if first_cap - sequence[anchor - previous_width - position] > 4)
        high_cap = first_cap - sequence[anchor - previous_width - excess]
        gap = cap4_generated_width(order) + excess
        root = fibonacci[order] - gap
        high_member = anchor - previous_width - excess
        threshold = first_cap - 4
        for point in range(1, root):
            if point < high_member:
                assert sequence[point] <= threshold
            elif point > high_member:
                assert sequence[point] >= threshold
            wall_positions += 1
        trajectory, transient, period = full_orbit(sequence, root)
        assert period == 2
        landing, pairs = even_anchor_landing(sequence, root, anchor)
        clock = 2 * pairs
        assert trajectory[clock] == landing
        assert all(point > anchor for point in trajectory[:clock:2])
        assert high_member <= landing <= anchor
        assert pairs <= capture_pair_budget(root - 1 - anchor)
        response = lambda position: first_cap - sequence[anchor - previous_width - position]
        reset, query_excess, queried_cap = frontier_reset_from_landing(
            order, excess, anchor - landing, response)
        first_hit = next(clock for clock, point in enumerate(trajectory) if sequence[point] == threshold)
        assert first_hit % 2 == int(trajectory[first_hit] < high_member) == reset
        depth_parity = sequence[root - 1] % 2
        selected_high = depth_parity != reset
        predicted_cap = high_cap if selected_high else 4
        predicted_split = high_member if selected_high else high_member + high_cap - 4
        assert splits[root] == predicted_split
        assert anchor - sequence[root] == predicted_cap
        values = [sequence[root + offset] for offset in offsets]
        children = [splits[root + offset] - (anchor - gap) for offset in offsets]
        assert [anchor - value for value in values] == [predicted_cap, 4, 4, 4, 4]
        assert children == [4 if selected_high else high_cap, 6, 7, 9, 11]
        scalar_joint = values[4] - values[1] - values[3] + values[0]
        index_joint = children[4] - children[1] - children[3] + children[0]
        assert index_joint - scalar_joint == high_cap - 4
        for offset, child, value, pattern in zip(offsets, children, values, patterns):
            current = root + offset
            endpoint = current - 1
            for iteration in range(sequence[current - 1]):
                endpoint = current - sequence[endpoint]
            assert endpoint == splits[current]
            assert sequence[endpoint] + sequence[current - endpoint] == sequence[current]
            literal_updates += sequence[current - 1]
            first_digit, second_digit, third_digit = pattern
            polynomial = (-gap + high_cap + 4 + (6 - high_cap) * first_digit
                          + (7 - high_cap) * second_digit + (9 - high_cap) * third_digit
                          + (high_cap - 4) * first_digit * third_digit)
            assert splits[current] - value == polynomial
            actual_pattern_rows += 1
        higher = set(canonical_fibonacci_indices(root, fibonacci))
        canonical = (min(higher) >= 7 and all(set(canonical_fibonacci_indices(root + offset, fibonacci))
                     == higher | set(canonical_fibonacci_indices(offset, fibonacci)) for offset in offsets))
        actual_rows.append(dict(order=order, root=root, frontier_excess=excess,
                                first_high_cap=high_cap, even_landing_clock=clock,
                                landing_offset_from_anchor=landing - anchor,
                                reset_bit=reset, query_excess=query_excess, queried_cap=queried_cap,
                                depth_parity=depth_parity, selected_cap=predicted_cap,
                                child_offsets=children, scalar_joint=scalar_joint, index_joint=index_joint,
                                joint_difference=index_joint - scalar_joint,
                                common_canonical_higher_word=canonical))
    assert [row['common_canonical_higher_word'] for row in actual_rows] == [False, False, True, False]
    assert actual_rows[2]['even_landing_clock'] == actual_rows[3]['even_landing_clock'] == 12
    assert actual_rows[2]['reset_bit'] == 0 and actual_rows[3]['reset_bit'] == 1
    return dict(symbolic_orders_inclusive=[27, 60], frontier_positions_inclusive=[9, 43],
                symbolic_landing_phase_cases=symbolic_cases, symbolic_map_updates=symbolic_updates,
                symbolic_branch_counts=branch_counts,
                actual_orders_inclusive=[27, 30], actual_frontiers=len(actual_rows),
                actual_five_pattern_rows=actual_pattern_rows, literal_endpoint_updates=literal_updates,
                global_threshold_wall_positions=wall_positions, actual_rows=actual_rows,
                entry_rule='First even point at or below F_(K-1); no supplied entry clock/current parent cap. One arithmetic low-cap read and at most one tail query derive a reset bit.',
                maximum_tail_lookahead=4,
                joint_identity='I_selected_child_index-I_parent_scalar=e-4; the entire g-C five-pattern response is phase independent.',
                conditional_periodic_option_count=2, conditional_fixed_width_phase_bits=1,
                scope='A written frontier theorem follows from the existing alphabet, shelves, capture and depth-in-cycle results; no new infinite finite-base premise. Symbolic landing cases corroborate local phase and feature formulas, not exterior stopping qualification. Actual first-even landings and literal endpoints verify orders27..30. Only the order29 root is a certified canonical FIB window. The one-bit phase cost counts the declared two-periodic-option table; a qualified landing derives it and it is not an independent-input lower bound with full order supplied. Exterior landing construction uses actual global sequence queries; general nonfrontier copy runs, wider word evolution and global dispersion/convergence remain open.')


def frontier_hole_reset(order, excess, landing_gap, response):
    assert order >= 27 and 9 <= excess <= 46
    previous_width = cap4_generated_width(order - 1)
    frontier = higher_cap_width(order - 1, 3)
    high_gap = previous_width + excess
    assert 0 <= landing_gap <= high_gap
    if landing_gap == high_gap:
        return 1, None, None
    if landing_gap > frontier:
        return 0, None, None
    landing_cap = generated_cap4_profile(order - 1, landing_gap)
    query_excess = excess + 4 - landing_cap
    queried_cap = response(query_excess)
    assert 4 <= queried_cap <= query_excess <= 50
    if queried_cap > 4:
        following_gap = previous_width + excess + 4 - queried_cap
        assert frontier < following_gap < high_gap
    return int(queried_cap == 4), query_excess, queried_cap


def frontier_copy_hole_audit(sequence, splits, fibonacci):
    alphabet = (4, 7, 8, 9, 10, 13)
    shifted_alphabet = tuple(letter - 4 for letter in alphabet)
    adjacent_graphs = 0
    for excess in range(9, 47):
        for current, adjacent in product(shifted_alphabet, repeat=2):
            if current > excess - 4 or adjacent > excess - 3:
                continue
            profile = [0] * (excess + 2)
            profile[excess] = current
            profile[excess + 1] = adjacent
            first_cycles = capped_profile_cycles(profile[:excess + 1], excess)
            first_points = {point for cycle in first_cycles for point in cycle}
            assert first_points == ({excess} if current == 0 else {excess, excess - current})
            assert {profile[point] for point in first_points} == {0, current}
            following_cycles = capped_profile_cycles(profile, excess + 1)
            following_points = {point for cycle in following_cycles for point in cycle}
            assert following_points == ({excess + 1} if adjacent == 0
                                        else {excess + 1, excess + 1 - adjacent})
            assert {profile[point] for point in following_points} == {0, adjacent}
            adjacent_graphs += 1
    clock_cases = 0
    minima = []
    for horizon in range(1, 151):
        minimum = horizon
        even_minimum = horizon
        odd_minimum = horizon
        for first_residue in range(3):
            even_resets = sum((first_residue + step) % 3 == 1 for step in range(horizon))
            odd_resets = horizon - even_resets
            even_minimum = min(even_minimum, even_resets)
            odd_minimum = min(odd_minimum, odd_resets)
            for odd_prefix in range(horizon + 1):
                resets = sum(int((first_residue + step) % 3 != 1) == int(step < odd_prefix)
                             for step in range(horizon))
                minimum = min(minimum, resets)
                assert resets >= (horizon - 1) // 3
                clock_cases += 1
        assert minimum == (horizon - 1) // 3
        assert even_minimum == horizon // 3 and odd_minimum == 2 * horizon // 3
        if horizon in (1, 2, 3, 4, 6, 7, 30, 150):
            minima.append(dict(updates=horizon, general_minimum=minimum,
                               even_adjacent_minimum=even_minimum,
                               never_erased_odd_minimum=odd_minimum))
    symbolic_cases = 0
    symbolic_updates = 0
    out_of_alphabet_queries = 0
    arithmetic_fibonacci = [0, 1]
    while len(arithmetic_fibonacci) <= 60:
        arithmetic_fibonacci.append(sum(arithmetic_fibonacci[-2:]))
    for order in range(27, 61):
        width = cap4_generated_width(order - 1)
        frontier = higher_cap_width(order - 1, 3)
        assert width > frontier and width + 50 < arithmetic_fibonacci[order - 3]
        landing_gaps = sorted({0, negative_plateau_width(order - 1),
                               unit_defect_width(order - 1), higher_cap_width(order - 1, 2),
                               frontier, frontier + 1})
        for excess in range(9, 47):
            high_gap = width + excess
            for high_cap in alphabet[1:]:
                if high_cap > excess:
                    continue
                for landing_gap in landing_gaps + [high_gap - 1, high_gap]:
                    if landing_gap <= frontier:
                        landing_cap = generated_cap4_profile(order - 1, landing_gap)
                        query = excess + 4 - landing_cap
                        choices = alphabet if query <= 47 else range(4, query + 1)
                    else:
                        query = None
                        choices = (4,)
                    for queried_cap in choices:
                        if query is not None and queried_cap > query:
                            continue
                        reset, query_excess, response_cap = frontier_hole_reset(
                            order, excess, landing_gap, lambda position: queried_cap)
                        def profile(point):
                            if point <= width:
                                return generated_cap4_profile(order - 1, point)
                            if point < high_gap:
                                return 4
                            if point == high_gap:
                                return high_cap
                            assert query_excess is not None and point == width + query_excess
                            return response_cap
                        for parity in (0, 1):
                            point = landing_gap
                            for iteration in range(8 + parity):
                                point = width + excess + 4 - profile(point)
                                symbolic_updates += 1
                            selected_high = parity != reset
                            assert point == (high_gap if selected_high else high_gap + 4 - high_cap)
                            assert profile(point) == (high_cap if selected_high else 4)
                            symbolic_cases += 1
                        out_of_alphabet_queries += queried_cap not in alphabet
    assert out_of_alphabet_queries > 0
    actual_roots = 0
    actual_high = []
    actual_flat = 0
    literal_updates = 0
    actual_by_key = {}
    for order in range(27, 31):
        anchor, first_cap = fibonacci[order - 1], fibonacci[order - 2]
        width = cap4_generated_width(order - 1)
        response = lambda position: first_cap - sequence[anchor - width - position]
        for excess in range(9, 47):
            if not all(response(position) == 4 for position in range(1, excess)):
                continue
            high_cap = response(excess)
            adjacent_before = response(excess + 1) - 4
            root = fibonacci[order] - cap4_generated_width(order) - excess
            current = anchor - sequence[root] - 4
            adjacent_after = anchor - sequence[root - 1] - 4
            assert current in (0, high_cap - 4)
            assert adjacent_after in (0, adjacent_before)
            if high_cap == 4:
                assert current == 0 and splits[root] == anchor - width - excess
                actual_flat += 1
            else:
                high_member = anchor - width - excess
                landing, pairs = even_anchor_landing(sequence, root, anchor)
                reset, query, queried_cap = frontier_hole_reset(order, excess, anchor - landing, response)
                trajectory, transient, period = full_orbit(sequence, root)
                assert period == 2
                path_holes = [(clock, point) for clock, point in enumerate(trajectory)
                              if clock % 2 and point < high_member and sequence[point] == first_cap - 4]
                assert bool(path_holes) == bool(reset)
                witness, witness_clock = None, None
                if reset:
                    witness = trajectory[2 * pairs - 1] if landing == high_member else root - sequence[landing]
                    witness_clock = 2 * pairs - 1 if landing == high_member else 2 * pairs + 1
                    assert (witness_clock, witness) in path_holes
                    assert witness < high_member and sequence[witness] == first_cap - 4
                depth = sequence[root - 1]
                assert bool(current) == bool((depth - reset) % 2)
                endpoint = root - 1
                for iteration in range(depth):
                    endpoint = root - sequence[endpoint]
                assert endpoint == splits[root]
                literal_updates += depth
                row = dict(order=order, excess=excess, root=root, preceding_cap=high_cap,
                           parent_cap=current + 4, adjacent_before=adjacent_before,
                           adjacent_after=adjacent_after, reset=reset, depth_parity=depth % 2,
                           even_landing_clock=2 * pairs, hole=witness, hole_clock=witness_clock,
                           hole_value=sequence[witness] if witness is not None else None,
                           frontier_index=high_member, frontier_value=sequence[high_member],
                           tail_query=query, queried_cap=queried_cap)
                actual_high.append(row)
                actual_by_key[(order, excess)] = row
            actual_roots += 1
    histories = []
    for excess in range(9, 47):
        seed_order = next((order for order in range(26, 31)
                           if all(fibonacci[order - 1] - sequence[fibonacci[order] - cap4_generated_width(order) - position] == 4
                                  for position in range(1, excess))), None)
        if seed_order is None:
            continue
        seed_root = fibonacci[seed_order] - cap4_generated_width(seed_order) - excess
        seed_cap = fibonacci[seed_order - 1] - sequence[seed_root]
        if seed_cap == 4:
            continue
        seed_adjacent = fibonacci[seed_order - 1] - sequence[seed_root - 1] - 4
        updates = []
        erased_order = None
        for order in range(seed_order + 1, 31):
            root = fibonacci[order] - cap4_generated_width(order) - excess
            cap = fibonacci[order - 1] - sequence[root]
            if cap == 4:
                erased_order = order
                assert all(fibonacci[following - 1] - sequence[fibonacci[following] - cap4_generated_width(following) - position] == 4
                           for following in range(order, 31) for position in range(1, excess + 1))
                break
            assert cap == seed_cap
            updates.append(actual_by_key[(order, excess)])
        resets = sum(row['reset'] for row in updates)
        count = len(updates)
        assert resets >= max(0, (count - 1) // 3)
        if seed_adjacent % 2 == 0:
            assert resets >= count // 3
        histories.append(dict(seed_order=seed_order, excess=excess, seed_cap=seed_cap,
                               seed_adjacent=seed_adjacent, observed_copies=count,
                               observed_copy_resets=resets, erased_order=erased_order,
                               scope='Finite observed prefix of the conditional copy history; no lifetime extrapolation.'))
    assert any(row['hole'] == 514118 and row['frontier_index'] == 514119
               and row['parent_cap'] == 4 for row in actual_high)
    return dict(shifted_alphabet=list(shifted_alphabet), frontier_positions_inclusive=[9, 46],
                adjacent_profile_graphs=adjacent_graphs, clock_horizons_inclusive=[1, 150],
                clock_histories=clock_cases, clock_minima=minima,
                symbolic_orders_inclusive=[27, 60], symbolic_landing_cases=symbolic_cases,
                symbolic_map_updates=symbolic_updates, out_of_alphabet_lookahead_cases=out_of_alphabet_queries,
                maximum_tail_lookahead_position=50, actual_orders_inclusive=[27, 30],
                actual_qualified_roots=actual_roots, actual_flat_roots=actual_flat,
                actual_high_frontiers=actual_high, actual_literal_endpoint_updates=literal_updates,
                actual_copy_histories=histories,
                reset_lower_bound='floor((t-1)/3); floor(t/3) with initially even adjacent cap; floor(2t/3) while adjacent cap remains odd.',
                hole_rule='Reset1 iff an odd-clock actual path point y lies below the high frontier and has C(y)=F_(K-2)-4. Witnesses at different orders are distinct.',
                scope='Infinite copy/erase, clock-density and hole-witness deductions use existing alphabet/shelf/zero-allocation premises. Envelope sharpness is not actual history sharpness. Hole-free frontier paths give conditional widening only. Nonfrontier runs, actual hole-frequency control, additive martingale occupation, global dispersion/convergence and position47 remain outside this result.')


def response_state_orbit(mapping, start):
    states = []
    point = start
    while point not in states:
        states.append(point)
        point = mapping[point]
    transient = states.index(point)
    return states, transient, len(states) - transient


def response_state_endpoint(mapping, start, steps):
    assert steps >= 0
    states, transient, period = response_state_orbit(mapping, start)
    position = steps if steps < len(states) else transient + (steps - transient) % period
    return states[position]


def copy_clock_variation_audit(sequence, splits, fibonacci):
    alphabet = (4, 7, 8, 9, 10, 13)
    maps = 0
    seeds = 0
    direct_updates = 0
    maximum_transient = 0
    for high_cap in alphabet[1:]:
        free = [letter for letter in alphabet if letter not in (4, high_cap)]
        for responses in product(alphabet, repeat=4):
            mapping = dict(zip(free, responses))
            mapping.update({4: high_cap, high_cap: 4})
            maps += 1
            for start in alphabet:
                states, transient, period = response_state_orbit(mapping, start)
                if set(states[transient:]) != {4, high_cap}:
                    continue
                assert period == 2 and transient <= 4
                maximum_transient = max(maximum_transient, transient)
                reset = int((transient + int(states[transient] == high_cap)) % 2 == 0)
                point = start
                for step in range(16):
                    if step >= transient:
                        assert (point == 4) == bool((step - reset) % 2)
                    point = mapping[point]
                    direct_updates += 1
                seeds += 1
    assert maps == 5 * 6 ** 4 and maximum_transient == 4
    clock_cases = 0
    sharp_cases = 0
    for horizon in range(1, 15):
        for first_residue in range(3):
            clock = [int((first_residue + step) % 3 == 1) for step in range(horizon)]
            clock_variation = sum(before != after for before, after in zip(clock, clock[1:]))
            assert clock_variation >= 2 * (horizon - 1) // 3
            for parities in product((0, 1), repeat=horizon):
                resets = [phase ^ parity for phase, parity in zip(clock, parities)]
                switches = sum(before != after for before, after in zip(parities, parities[1:]))
                reset_variation = sum(before != after for before, after in zip(resets, resets[1:]))
                cost = 2 * sum(resets) - resets[0] - resets[-1] + switches
                assert clock_variation <= switches + reset_variation <= cost
                assert sum(resets) >= max(0, (clock_variation - switches + 1) // 2)
                sharp_cases += cost == clock_variation
                clock_cases += 1
            assert 2 * sum(clock) - clock[0] - clock[-1] == clock_variation
    actual_rows = []
    categories = {}
    literal_updates = 0
    copied = {}
    maximum_actual_transient = 0
    for order in range(27, 31):
        anchor, lower = fibonacci[order - 1], fibonacci[order - 2]
        width = cap4_generated_width(order)
        previous_width = cap4_generated_width(order - 1)
        response = lambda position: lower - sequence[anchor - previous_width - position]
        for excess in range(9, 44):
            root = fibonacci[order] - width - excess
            high_member = anchor - previous_width - excess
            high_cap = response(excess)
            if high_cap == 4:
                continue
            partner = high_member + high_cap - 4
            if sequence[partner] != lower - 4:
                continue
            trajectory, transient, period = full_orbit(sequence, root)
            if set(trajectory[transient:]) != {high_member, partner}:
                continue
            assert period == 2
            reset = int(trajectory.index(high_member) % 2 == 0)
            landing, pairs = even_anchor_landing(sequence, root, anchor)
            landing_cap = lower - sequence[landing]
            seed = response(excess + 4 - landing_cap)
            mapping = {letter: response(excess + 4 - letter) for letter in alphabet}
            states, delay, mapped_period = response_state_orbit(mapping, seed)
            assert mapped_period == 2 and set(states[delay:]) == {4, high_cap}
            assert delay <= 4
            maximum_actual_transient = max(maximum_actual_transient, delay)
            assert reset == int((delay + int(states[delay] == high_cap)) % 2 == 0)
            holes = [(clock, point) for clock, point in enumerate(trajectory)
                     if clock % 2 and point < high_member and sequence[point] == lower - 4]
            if reset:
                precursor = trajectory[transient - 1]
                precursor_clock = transient - 1
                assert precursor not in (high_member, partner)
                if trajectory[transient] == high_member:
                    assert precursor_clock % 2 == 1 and sequence[precursor] == lower - 4
                    category = 'lower_cap4_hole' if precursor < high_member else 'upper_cap4_precursor'
                else:
                    assert precursor_clock % 2 == 0 and precursor > high_member
                    assert sequence[precursor] == lower - high_cap
                    category = 'upper_high_cap_precursor'
            else:
                category, precursor, precursor_clock = 'no_reset', None, None
                assert not holes
            depth = sequence[root - 1]
            copying = bool((depth - reset) % 2)
            endpoint = root - 1
            for iteration in range(depth):
                endpoint = root - sequence[endpoint]
            literal_updates += depth
            assert endpoint == splits[root] == (high_member if copying else partner)
            parent_cap = anchor - sequence[root]
            assert parent_cap == (high_cap if copying else 4)
            key = category + ('_copy' if copying else '_erase')
            categories[key] = categories.get(key, 0) + 1
            row = dict(order=order, excess=excess, root=root, high_cap=high_cap,
                       parent_cap=parent_cap, adjacent_cap=anchor - sequence[root - 1],
                       high_member=high_member, partner=partner, reset=reset,
                       category=category, precursor=precursor, precursor_clock=precursor_clock,
                       first_cycle_clock=transient, even_landing_clock=2 * pairs,
                       response_seed=seed, response_transient=delay,
                       odd_lower_cap4_holes=[dict(clock=clock, index=point) for clock, point in holes])
            actual_rows.append(row)
            if copying:
                copied[(order, excess)] = row
    runs = []
    migrations = []
    for excess in range(9, 44):
        orders = [order for order in range(27, 31) if (order, excess) in copied]
        while orders:
            start = orders.pop(0)
            consecutive = [start]
            while orders and orders[0] == consecutive[-1] + 1:
                consecutive.append(orders.pop(0))
            rows = [copied[(order, excess)] for order in consecutive]
            assert len({row['high_cap'] for row in rows}) == 1
            parities = [row['adjacent_cap'] % 2 for row in rows]
            resets = [row['reset'] for row in rows]
            switches = sum(before != after for before, after in zip(parities, parities[1:]))
            clock = [int(order % 3 == 1) for order in consecutive]
            clock_variation = sum(before != after for before, after in zip(clock, clock[1:]))
            assert resets == [phase ^ parity for phase, parity in zip(clock, parities)]
            assert 2 * sum(resets) - resets[0] - resets[-1] + switches >= clock_variation
            for position in range(1, len(rows)):
                if parities[position] == parities[position - 1]:
                    continue
                row = rows[position]
                order = row['order']
                adjacent = row['root'] - 1
                child = splits[adjacent]
                child_excess = fibonacci[order - 1] - child - cap4_generated_width(order - 1)
                shift = fibonacci[order - 2] - (adjacent - child)
                assert child_excess == excess + 5 - shift <= excess - 2
                assert shift in alphabet and shift >= 7
                assert fibonacci[order - 2] - sequence[child] == row['adjacent_cap']
                assert fibonacci[order - 3] - sequence[adjacent - child] == 0
                migrations.append(dict(order=order, excess=excess, adjacent_root=adjacent,
                                       child=child, child_excess=child_excess, shift=shift))
            runs.append(dict(excess=excess, orders=consecutive, resets=resets,
                             adjacent_parities=parities, switches=switches,
                             clock_variation=clock_variation))
    witness = next(row for row in actual_rows if row['root'] == 196314)
    assert witness['reset'] == 1 and witness['parent_cap'] == witness['high_cap'] == 9
    assert witness['precursor'] == 121297 and witness['precursor_clock'] == 12
    assert witness['category'] == 'upper_high_cap_precursor' and not witness['odd_lower_cap4_holes']
    assert migrations
    return dict(two_cycle_maps=maps, qualified_response_seeds=seeds,
                direct_map_updates=direct_updates, maximum_response_transient=maximum_transient,
                binary_clock_horizons_inclusive=[1, 14], binary_clock_cases=clock_cases,
                sharp_binary_clock_cases=sharp_cases,
                clock_inequality='2M-reset_first-reset_last+S >= B_t >= floor(2(t-1)/3).',
                actual_orders_inclusive=[27, 30], actual_two_cycle_rows=len(actual_rows),
                actual_categories=categories, actual_literal_endpoint_updates=literal_updates,
                maximum_actual_response_transient=maximum_actual_transient,
                actual_rows=actual_rows, actual_copy_runs=runs, actual_adjacent_migrations=migrations,
                scope='General selected {4,e} two-cycle phase decoder and reset/adjacent-variation tradeoff are infinite written deductions from existing premises. Reset precursors can be lower holes, upper cap4 points or upper same-high-cap points. Actual196314 resets and copies with no odd lower cap4 hole. Binary sharpness is a relaxed clock envelope, not actual history sharpness. Adjacent migration counts cross orders and are not bounded by the single-spine15-drop budget or additive martingale occupation. Actual entry/word generation and global dispersion remain open.')


def binary_prefix_audit(sequence, splits, fibonacci):
    alphabet = (4, 7, 8, 9, 10, 13)
    even_alphabet = (4, 8, 10)
    binary_alphabet = (4, 8)
    adjacent_maps = 0
    adjacent_periods = set()
    for own in alphabet:
        for earlier in product(even_alphabet, repeat=5):
            mapping = dict(zip(alphabet, (own,) + earlier))
            for start in alphabet:
                states, transient, period = response_state_orbit(mapping, start)
                adjacent_periods.add(period)
                for state in states[transient:]:
                    output = mapping[state]
                    assert output % 2 == 0 or output == own
                    if own % 2 == 0:
                        assert output % 2 == 0
            adjacent_maps += 1
    binary_maps = 0
    binary_updates = 0
    for outputs in product(binary_alphabet, repeat=2):
        mapping = dict(zip(binary_alphabet, outputs))
        for start in binary_alphabet:
            states, transient, period = response_state_orbit(mapping, start)
            assert transient <= 1 and period <= 2
            if 4 in states[transient:] and mapping[4] == 8:
                assert period == 2 and mapping[8] == 4
            point = start
            for step in range(20):
                assert response_state_endpoint(mapping, start, step) == point
                point = mapping[point]
                binary_updates += 1
        binary_maps += 1
    relaxed_order, relaxed_excess = 32, 33
    previous_width = cap4_generated_width(relaxed_order - 1)
    relaxed_gap = cap4_generated_width(relaxed_order) + relaxed_excess
    profile = [generated_cap4_profile(relaxed_order - 1, point)
               if point <= previous_width else 4
               for point in range(relaxed_gap + 1)]
    profile[previous_width + 33] = 8
    profile[previous_width + 29] = 10
    mapping = {letter: profile[relaxed_gap - letter] for letter in even_alphabet}
    assert [mapping[letter] for letter in even_alphabet] == [8, 10, 4]
    states, transient, period = response_state_orbit(mapping, 4)
    assert states == [4, 8, 10] and transient == 0 and period == 3
    cycles = capped_profile_cycles(profile, relaxed_gap)
    selected_gap = relaxed_gap - 4
    cycle = next(cycle for cycle in cycles if selected_gap in cycle)
    assert len(cycle) == 3 and profile[selected_gap] == 8
    assert profile[relaxed_gap - 8] == 10
    for position in range(1, 48):
        if previous_width + position < len(profile):
            assert 4 <= profile[previous_width + position] <= max(4, position)
    assert all(letter <= negative_plateau_width(relaxed_order - 2) for letter in even_alphabet)
    offsets = (0, 2, 3, 5, 7)
    shared_positions = sorted({offset + shift for offset in offsets for shift in (0, 4)})
    assert shared_positions == [0, 2, 3, 4, 5, 6, 7, 9, 11]
    shared_words = 0
    complete_map_descriptors = set()
    maximum_options = 0
    sharp_words = 0
    sharp_word = [4, 4, 4, 8, 4, 8, 8, 8, 4]
    sharp_maps = None
    shared_profile_graphs = 0
    for word in product(binary_alphabet, repeat=len(shared_positions)):
        response = dict(zip(shared_positions, word))
        row_maps = []
        options = 1
        for offset in offsets:
            mapping = {letter: response[offset + letter - 4] for letter in binary_alphabet}
            periodic = set()
            for start in binary_alphabet:
                states, transient, period = response_state_orbit(mapping, start)
                assert transient <= 1 and period <= 2
                periodic.update(states[transient:])
            options *= len(periodic)
            row_maps.append(tuple(mapping[letter] for letter in binary_alphabet))
        descriptor = tuple(row_maps)
        assert descriptor not in complete_map_descriptors
        complete_map_descriptors.add(descriptor)
        maximum_options = max(maximum_options, options)
        sharp_words += options == 32
        if list(word) == sharp_word:
            assert options == 32
            sharp_maps = row_maps
        previous_width = cap4_generated_width(31)
        full_gap = cap4_generated_width(32) + 31
        profile = [generated_cap4_profile(31, point) if point <= previous_width else 4
                   for point in range(full_gap + 1)]
        for position, letter in response.items():
            profile[previous_width + 31 - position] = letter
            assert 20 <= 31 - position <= 31 and letter <= 31 - position
        assert profile[previous_width + 1:previous_width + 20] == [4] * 19
        for offset, outputs in zip(offsets, row_maps):
            row_gap = full_gap - offset
            mapping = dict(zip(binary_alphabet, outputs))
            periodic = set()
            for start in binary_alphabet:
                states, transient, period = response_state_orbit(mapping, start)
                periodic.update(states[transient:])
            cycles = capped_profile_cycles(profile[:row_gap + 1], row_gap)
            assert {point for cycle in cycles for point in cycle} == {
                row_gap - letter for letter in periodic}
            shared_profile_graphs += 1
        shared_words += 1
    assert shared_words == 512 and maximum_options == 32 and sharp_maps is not None
    literal_updates = 0
    checked_endpoints = {}
    def verify_root(root):
        nonlocal literal_updates
        if root in checked_endpoints:
            return checked_endpoints[root]
        endpoint = root - 1
        for iteration in range(sequence[root - 1]):
            endpoint = root - sequence[endpoint]
        assert endpoint == splits[root]
        assert sequence[endpoint] + sequence[root - endpoint] == sequence[root]
        literal_updates += sequence[root - 1]
        checked_endpoints[root] = endpoint
        return endpoint
    premises = []
    for order, excess, cap in ((30, 17, 8), (30, 18, 8), (30, 19, 4),
                              (31, 17, 4), (31, 18, 4)):
        root = fibonacci[order] - cap4_generated_width(order) - excess
        assert fibonacci[order - 1] - sequence[root] == cap
        endpoint = verify_root(root)
        premises.append(dict(order=order, position=excess, index=root, response=cap,
                              value=sequence[root], split=endpoint))
    seed_word = [fibonacci[29] - sequence[fibonacci[30] - cap4_generated_width(30) - position]
                 for position in range(1, 20)]
    assert seed_word == [4] * 16 + [8, 8, 4]
    shifts = []
    periods = []
    landing_reads = 0
    for excess in range(1, 20):
        order = 31
        anchor, lower = fibonacci[30], fibonacci[29]
        gap = cap4_generated_width(order) + excess
        root = fibonacci[order] - gap
        endpoint = verify_root(root)
        shift = gap - (anchor - endpoint)
        assert shift == (8 if excess in (17, 18) else 4)
        assert anchor - sequence[root] == 4
        assert lower - sequence[endpoint] == 4
        assert fibonacci[28] - sequence[root - endpoint] == 0
        trajectory, transient, period = full_orbit(sequence, root)
        assert period == (2 if excess in (17, 18) else 1)
        shifts.append(shift)
        periods.append(period)
        if excess >= 9:
            response = lambda position: lower - sequence[anchor - cap4_generated_width(30) - position]
            mapping = {letter: response(excess + 4 - letter) for letter in binary_alphabet}
            landing, pairs = even_anchor_landing(sequence, root, anchor)
            landing_cap = lower - sequence[landing]
            initial_seed = response(excess + 4 - landing_cap)
            binary_seed = response(excess + 4 - initial_seed)
            assert binary_seed in binary_alphabet
            assert response_state_endpoint(mapping, binary_seed,
                                           sequence[root - 1] - 2 * pairs - 3) == shift
            assert sequence[root - 1] % 2 == anchor % 2
            landing_reads += 3
    symbolic_orders = 0
    symbolic_rows = 0
    for order in range(32, 121):
        previous_width = cap4_generated_width(order - 1)
        for excess in range(1, 20):
            gap = cap4_generated_width(order) + excess
            profile = [generated_cap4_profile(order - 1, point)
                       if point <= previous_width else 4 for point in range(gap + 1)]
            cycles = capped_profile_cycles(profile, gap)
            assert cycles == [(gap - 4,)]
            symbolic_rows += 1
        symbolic_orders += 1
    canonical_root = fibonacci[31] - cap4_generated_width(31) - 18
    higher_word = set(canonical_fibonacci_indices(canonical_root, fibonacci))
    assert sorted(higher_word) == [8, 11] + list(range(14, 31, 2))
    canonical_values = []
    canonical_splits = []
    canonical_periods = []
    for offset in offsets:
        root = canonical_root + offset
        assert set(canonical_fibonacci_indices(root, fibonacci)) == (
            higher_word | set(canonical_fibonacci_indices(offset, fibonacci)))
        canonical_values.append(sequence[root])
        canonical_splits.append(verify_root(root))
        trajectory, transient, period = full_orbit(sequence, root)
        canonical_periods.append(period)
    assert canonical_values == [832036] * 5
    assert canonical_splits == [831925, 831923, 831924, 831926, 831928]
    scalar_joint = canonical_values[4] - canonical_values[1] - canonical_values[3] + canonical_values[0]
    index_joint = canonical_splits[4] - canonical_splits[1] - canonical_splits[3] + canonical_splits[0]
    assert scalar_joint == 0 and index_joint == 4
    return dict(adjacent_even_prefix_maps=adjacent_maps,
                adjacent_even_prefix_periods=sorted(adjacent_periods),
                binary_maps=binary_maps, binary_direct_updates=binary_updates,
                even_three_cycle_profile=dict(order=relaxed_order, excess=relaxed_excess,
                                               tail_overrides={'33': 8, '29': 10},
                                               cycle_states=[4, 8, 10], period=3,
                                               selected_state=4, parent_cap=8, excess_drop=0,
                                               scope='Relaxed even captured profile, not an actual C copy or alternative sequence.'),
                shared_five_row_positions=shared_positions, relaxed_shared_words=shared_words,
                distinct_complete_map_collections=len(complete_map_descriptors),
                relaxed_word_bits=9, maximum_periodic_output_options=maximum_options,
                sharp_periodic_output_bits=5, sharp_shared_words=sharp_words,
                sharp_shared_word=sharp_word, sharp_maps=sharp_maps,
                sharpness_order=32, sharpness_excess=31, shared_profile_graphs=shared_profile_graphs,
                new_scalar_premises=premises, binary_seed_order=30,
                binary_seed_positions_inclusive=[1, 19], binary_seed_word=seed_word,
                flat_positions_inclusive=[1, 19], flat_from_order=31,
                actual_order31_shifts=shifts, actual_order31_periods=periods,
                literal_checked_roots=len(checked_endpoints), literal_endpoint_updates=literal_updates,
                qualified_landing_response_reads=landing_reads,
                symbolic_flat_orders_inclusive=[32, 120], symbolic_orders=symbolic_orders,
                symbolic_fixed_graphs=symbolic_rows,
                canonical_boundary_window=dict(order=31, root=canonical_root,
                                               higher_fibonacci_indices=sorted(higher_word),
                                               offsets=list(offsets), values=canonical_values,
                                               splits=canonical_splits, periods=canonical_periods,
                                               scalar_joint=scalar_joint, index_joint=index_joint),
                scope='Infinite causal subset propagation, one-way adjacent parity and binary periodic/three-step landing decoder. Five new independently regenerated/literal scalar premises give the explicit actual first19 word, zero residual selected descent to order30, and a finite canonical index interaction4 after scalar flattening. Nine/five-bit sharpness is a relaxed wide binary-prefix contract, not actual input minima or a proved actual wide binary seed. Even prefix alone allows period3 and zero drop alone does not certify period2. Qualified two-cycle reset density does not supply lower-hole equivalence, exterior word/entry construction or additive martingale occupation; global dispersion/convergence remain open.')



def ternary_support_audit(sequence=None, splits=None):
    fibonacci = [0, 1]
    while len(fibonacci) <= 34:
        fibonacci.append(sum(fibonacci[-2:]))
    order = 34
    width = cap4_generated_width(order)
    limit = fibonacci[order] - width - 1
    if sequence is None:
        sequence = array('I', [0, 1, 1])
        splits = array('I', [0, 0, 0])
        for index in range(3, limit + 1):
            trajectory, transient, period = full_orbit(sequence, index)
            depth = sequence[index - 1]
            position = depth if depth < len(trajectory) else transient + (depth - transient) % period
            endpoint = trajectory[position]
            value = sequence[endpoint] + sequence[index - endpoint]
            assert 2 <= value < index
            sequence.append(value)
            splits.append(endpoint)
        independent = brent_generate(limit)
        assert len(sequence) == len(independent)
        assert all(value == independent[index] for index, value in enumerate(sequence))
        del independent
    assert splits is not None and len(sequence) > limit
    digest = hashlib.sha256()
    for start in range(1, limit + 1, 65536):
        if start > 1:
            digest.update(b',')
        digest.update(','.join(map(str, sequence[start:min(start + 65536, limit + 1)])).encode('ascii'))
    word = [fibonacci[order - 1] - sequence[fibonacci[order] - width - position]
            for position in range(1, 48)]
    expected_word = [4] * 24 + [8, 8, 4, 4, 9, 8, 4, 4, 4, 8, 4, 4, 4, 8, 4, 4] + [8] * 7
    assert word == expected_word
    semigroup = {4 * first + 5 * second for first in range(12) for second in range(10)}
    support8 = {position for position in range(1, 48)
                if position - 25 in semigroup or position - 26 in semigroup}
    support9 = {position for position in range(1, 48) if position - 29 in semigroup}
    assert support9 <= support8
    assert [position for position in range(25, 48) if position not in support8] == [27, 28, 32]
    assert [position for position, value in enumerate(word, 1) if value == 9] == [29]
    for position, value in enumerate(word, 1):
        assert value == 4 or position in (support8 if value == 8 else support9)
    for support in (support8, support9):
        for position in support:
            for shift in (0, 4, 5):
                assert position + shift > 47 or position + shift in support
    literal_updates = 0
    premises = []
    for position in range(20, 48):
        root = fibonacci[order] - width - position
        endpoint = root - 1
        for iteration in range(sequence[root - 1]):
            endpoint = root - sequence[endpoint]
        assert endpoint == splits[root]
        assert sequence[endpoint] + sequence[root - endpoint] == sequence[root]
        literal_updates += sequence[root - 1]
        premises.append(dict(position=position, index=root, response=word[position - 1],
                              value=sequence[root], split=endpoint))
    alphabet = (4, 8, 9)
    periodic_sizes = {}
    map_updates = 0
    observed_periods = set()
    map_graphs = 0
    previous_width = cap4_generated_width(34)
    full_gap = cap4_generated_width(35) + 43
    for outputs in product(alphabet, repeat=3):
        mapping = dict(zip(alphabet, outputs))
        periodic = set()
        for start in alphabet:
            states, transient, period = response_state_orbit(mapping, start)
            assert transient <= 2 and period <= 3
            observed_periods.add(period)
            periodic.update(states[transient:])
            point = start
            for steps in range(24):
                assert response_state_endpoint(mapping, start, steps) == point
                point = mapping[point]
                map_updates += 1
        periodic_sizes[outputs] = len(periodic)
        profile = [generated_cap4_profile(34, point) if point <= previous_width else 4
                   for point in range(full_gap + 1)]
        for letter, output in zip(alphabet, outputs):
            position = 43 + 4 - letter
            assert position in support9
            profile[previous_width + position] = output
        cycles = capped_profile_cycles(profile, full_gap)
        assert {point for cycle in cycles for point in cycle} == {
            full_gap - letter for letter in periodic}
        map_graphs += 1
    assert observed_periods == {1, 2, 3}
    offsets = (0, 2, 3, 5, 7)
    shared_positions = sorted({offset + shift for offset in offsets for shift in (0, 4, 5)})
    assert shared_positions == [0, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    stencils = [tuple(shared_positions.index(offset + shift) for shift in (0, 4, 5))
                for offset in offsets]
    contracts = []
    graph_checks = 0
    for excess in range(16, 44):
        domains = [tuple([4] + ([8] if excess - position in support8 else [])
                        + ([9] if excess - position in support9 else []))
                   for position in shared_positions]
        words = 0
        maximum_options = 0
        sharp_word = None
        for shared_word in product(*domains):
            descriptors = [tuple(shared_word[index] for index in stencil) for stencil in stencils]
            recovered = {}
            options = 1
            for offset, outputs in zip(offsets, descriptors):
                options *= periodic_sizes[outputs]
                for letter, output in zip(alphabet, outputs):
                    position = offset + letter - 4
                    assert recovered.get(position, output) == output
                    recovered[position] = output
            assert tuple(recovered[position] for position in shared_positions) == shared_word
            if options > maximum_options:
                maximum_options = options
                sharp_word = shared_word
            words += 1
        full_gap = cap4_generated_width(35) + excess
        profile = [generated_cap4_profile(34, point) if point <= previous_width else 4
                   for point in range(full_gap + 1)]
        for position, value in zip(shared_positions, sharp_word):
            profile[previous_width + excess - position] = value
        for offset in offsets:
            row_gap = full_gap - offset
            mapping = {letter: profile[row_gap - letter] for letter in alphabet}
            periodic = set()
            for start in alphabet:
                states, transient, period = response_state_orbit(mapping, start)
                periodic.update(states[transient:])
            cycles = capped_profile_cycles(profile[:row_gap + 1], row_gap)
            assert {point for cycle in cycles for point in cycle} == {
                row_gap - letter for letter in periodic}
            graph_checks += 1
        contracts.append(dict(excess=excess, words=words, word_bits=(words - 1).bit_length(),
                              maximum_options=maximum_options,
                              output_bits=(maximum_options - 1).bit_length(),
                              sharp_word=list(sharp_word)))
    assert max(row['words'] for row in contracts) == 34992
    assert max(row['maximum_options'] for row in contracts) == 162
    assert next(row for row in contracts if row['excess'] == 41)['sharp_word'] == [
        4, 4, 4, 9, 8, 8, 9, 8, 4, 4, 4, 8]
    relaxed_next_word = [4] * 24
    for excess in range(25, 48):
        mapping = {letter: word[excess + 3 - letter] for letter in alphabet}
        selected = 9 if excess == 34 else response_state_endpoint(mapping, 4, 6)
        states, transient, period = response_state_orbit(mapping, selected)
        assert transient == 0
        relaxed_next_word.append(mapping[selected])
    assert [relaxed_next_word[position - 1] for position in (38, 34, 33)] == [8, 9, 4]
    for position, value in enumerate(relaxed_next_word, 1):
        assert value == 4 or position in (support8 if value == 8 else support9)
    mapping = {letter: relaxed_next_word[38 + 3 - letter] for letter in alphabet}
    assert [mapping[letter] for letter in alphabet] == [8, 9, 4]
    return dict(seed_order=34, new_scalar_premises=premises, seed_word=word,
                prefix_limit=limit, independent_brent_agrees_through=limit,
                prefix_sha256=digest.hexdigest(), literal_endpoint_updates=literal_updates,
                response_alphabet=list(alphabet), response_support8=sorted(support8),
                response_support9=sorted(support9), flat_positions_inclusive=[1, 24],
                additional_permanent_flat_positions=[27, 28, 32],
                binary_prefix_positions_inclusive=[1, 28],
                sufficient_full_word_bits=(2 ** 7 * 3 ** 13 - 1).bit_length(),
                maximum_strict_drops_above_seed_by_cap={'8': 5, '9': 4},
                ternary_maps=len(periodic_sizes), map_direct_updates=map_updates,
                map_profile_graphs=map_graphs, possible_periods=sorted(observed_periods),
                shared_positions=shared_positions, shared_contracts=contracts,
                shared_word_graphs=graph_checks, shared_words_checked=sum(row['words'] for row in contracts),
                exact_relaxed_max_word_bits=16, exact_relaxed_max_output_bits=8,
                relaxed_next_word=relaxed_next_word,
                reachable_relaxed_three_cycle=dict(order=36, excess=38, map_values=[8, 9, 4],
                                                   cycle=[4, 8, 9], period=3),
                scope='Twenty-eight independently regenerated/literal scalar premises extend actual alphabet closure to{4,8,9}, first24 flat responses, permanent holes27/28/32 and binary prefix28 for every order>=34. Spatial4/5 support cones and cap-specific strict-drop bounds are infinite deductions. Full-word28-bit packing and exact five-row16/8-bit contracts describe relaxed support-compatible words, not actual input minima. A periodic-only update of the actual order34 seed permits a three-cycle at order36, but is not claimed to be the actual selected recurrence. Exterior landing and modulo3 clock construction, generic copy frequency and additive occupation/global dispersion remain open.')


def six_response_map_audit(sequence, splits, fibonacci):
    alphabet = (4, 7, 8, 9, 10, 13)
    offsets = (0, 2, 3, 5, 7)
    stencil = tuple(letter - 4 for letter in alphabet)
    shared_positions = sorted({offset + shift for offset in offsets for shift in stencil})
    assert shared_positions == [0, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 16]
    synthetic_maps = 0
    synthetic_starts = 0
    direct_updates = 0
    maximum_transient = 0
    observed_periods = set()
    for word in product(alphabet, repeat=6):
        mapping = dict(zip(alphabet, word))
        periodic = set()
        for start in alphabet:
            states, transient, period = response_state_orbit(mapping, start)
            assert transient <= 5 and 1 <= period <= 6
            maximum_transient = max(maximum_transient, transient)
            observed_periods.add(period)
            periodic.update(states[transient:])
            point = start
            for steps in range(18):
                assert response_state_endpoint(mapping, start, steps) == point
                if steps >= 5:
                    assert point == states[transient + (steps - transient) % period]
                point = mapping[point]
                direct_updates += 1
            synthetic_starts += 1
        assert 1 <= len(periodic) <= 6
        synthetic_maps += 1
    assert synthetic_maps == 6 ** 6 and maximum_transient == 5
    assert observed_periods == set(range(1, 7))
    sharp_word = [7, 8, 9, 13, 4, 10, 7, 13, 8, 10, 9, 4, 8, 7, 13]
    sharp_responses = dict(zip(shared_positions, sharp_word))
    sharp_maps = []
    for offset in offsets:
        mapping = {letter: sharp_responses[offset + letter - 4] for letter in alphabet}
        assert set(mapping.values()) == set(alphabet)
        assert all(response_state_orbit(mapping, letter)[1] == 0 for letter in alphabet)
        sharp_maps.append([mapping[letter] for letter in alphabet])
    assert 2 ** 38 < 6 ** 15 <= 2 ** 39
    assert 2 ** 12 < 6 ** 5 <= 2 ** 13
    for order in range(31, 61):
        width = cap4_generated_width(order - 1)
        profile = [generated_cap4_profile(order - 1, point) for point in range(width + 1)]
        profile.extend([4] * 47)
        for position, letter in sharp_responses.items():
            profile[width + 33 - position] = letter
        assert profile[width + 1:width + 17] == [4] * 16
        assert all(4 <= profile[width + position] <= max(4, position) for position in range(1, 48))
        for offset, sharp_map in zip(offsets, sharp_maps):
            gap = cap4_generated_width(order) + 33 - offset
            cycles = capped_profile_cycles(profile[:gap + 1], gap)
            periodic = {point for cycle in cycles for point in cycle}
            assert periodic == {gap - letter for letter in alphabet}
            mapping = dict(zip(alphabet, sharp_map))
            assert all(gap - profile[gap - letter] == gap - mapping[letter] for letter in alphabet)
    actual_roots = 0
    actual_periods = {}
    landing_tail_reads = 0
    extra_lookahead_reads = 0
    five_windows = 0
    literal_updates = 0
    for order in range(27, 31):
        anchor, first_cap = fibonacci[order - 1], fibonacci[order - 2]
        width = cap4_generated_width(order)
        previous_width = cap4_generated_width(order - 1)
        for excess in range(9, 44):
            gap = width + excess
            root = fibonacci[order] - gap
            response = lambda position: first_cap - sequence[anchor - previous_width - position]
            mapping = {letter: response(excess + 4 - letter) for letter in alphabet}
            assert all(letter in alphabet for letter in mapping.values())
            cycles = capped_profile_cycles([first_cap - sequence[anchor - point]
                                           for point in range(gap + 1)], gap)
            actual_periodic = {point for cycle in cycles for point in cycle}
            map_periodic = set()
            for letter in alphabet:
                states, transient, period = response_state_orbit(mapping, letter)
                map_periodic.update(states[transient:])
            assert actual_periodic == {gap - letter for letter in map_periodic}
            landing, pairs = even_anchor_landing(sequence, root, anchor)
            landing_gap = anchor - landing
            assert 0 <= landing_gap <= previous_width + excess
            assert pairs <= capture_pair_budget(first_cap) < 2 * order
            landing_cap = first_cap - sequence[landing]
            assert landing_cap in (0, 1, 2, 3) + alphabet
            seed = response(excess + 4 - landing_cap)
            assert seed in alphabet
            following = root - sequence[landing]
            assert root - sequence[following] == anchor - gap + seed
            remaining = sequence[root - 1] - 2 * pairs - 2
            assert remaining >= 5
            selected = response_state_endpoint(mapping, seed, remaining)
            states, transient, period = response_state_orbit(mapping, seed)
            assert splits[root] == anchor - gap + selected
            assert anchor - sequence[root] == mapping[selected]
            assert fibonacci[order - 3] - sequence[first_cap - selected] == 0
            trajectory, actual_transient, actual_period = full_orbit(sequence, root)
            assert actual_period == period
            actual_periods[str(period)] = actual_periods.get(str(period), 0) + 1
            landing_tail_reads += landing_gap > previous_width
            extra_lookahead_reads += landing_cap <= 3
            if excess in (9, 33, 43):
                endpoint = root - 1
                for iteration in range(sequence[root - 1]):
                    endpoint = root - sequence[endpoint]
                assert endpoint == splits[root]
                literal_updates += sequence[root - 1]
            if excess >= 16:
                shared = {position: response(excess - position) for position in shared_positions}
                for offset in offsets:
                    assert {letter: shared[offset + letter - 4] for letter in alphabet} == {
                        letter: response(excess - offset + 4 - letter) for letter in alphabet}
                five_windows += 1
            actual_roots += 1
    witness_fibonacci = list(fibonacci)
    while len(witness_fibonacci) <= 32:
        witness_fibonacci.append(sum(witness_fibonacci[-2:]))
    witness_order, witness_excess = 32, 33
    witness_gap = cap4_generated_width(witness_order) + witness_excess
    witness_root = witness_fibonacci[witness_order] - witness_gap
    witness_limit = witness_root + 5
    witness_sequence, _, _, witness_splits = generate(witness_limit)
    assert witness_sequence == brent_generate(witness_limit)
    assert witness_sequence[:len(sequence)] == sequence
    anchor, first_cap = witness_fibonacci[31], witness_fibonacci[30]
    mapping = {letter: first_cap - witness_sequence[anchor - witness_gap + letter]
               for letter in alphabet}
    assert [mapping[letter] for letter in alphabet] == [8, 8, 9, 4, 4, 9]
    landing, pairs = even_anchor_landing(witness_sequence, witness_root, anchor)
    landing_cap = first_cap - witness_sequence[landing]
    seed = first_cap - witness_sequence[anchor - witness_gap + landing_cap]
    depth = witness_sequence[witness_root - 1]
    remaining = depth - 2 * pairs - 2
    selected = response_state_endpoint(mapping, seed, remaining)
    clock_omitted = response_state_endpoint(mapping, seed, depth - 2)
    trajectory, transient, period = full_orbit(witness_sequence, witness_root)
    assert period == 3 and seed == 8 and pairs == 7 and landing == anchor - 123
    assert selected == 9 and mapping[selected] == 4 and selected != clock_omitted
    assert witness_splits[witness_root] == anchor - witness_gap + selected
    endpoint = witness_root - 1
    for iteration in range(depth):
        endpoint = witness_root - witness_sequence[endpoint]
    assert endpoint == witness_splits[witness_root]
    assert witness_sequence[endpoint] + witness_sequence[witness_root - endpoint] == witness_sequence[witness_root]
    witness = dict(order=witness_order, excess=witness_excess, root=witness_root,
                   map_values=[mapping[letter] for letter in alphabet], cycle=[8, 9, 4],
                   even_landing_clock=2 * pairs, landing_offset=landing - anchor,
                   landing_cap=landing_cap, response_seed=seed, depth=depth,
                   selected_state=selected, parent_cap=mapping[selected], selected_split=endpoint,
                   clock_omitted_state=clock_omitted, prefix_limit=witness_limit,
                   independent_brent_agrees_through=witness_limit,
                   prefix_sha256=hashlib.sha256(','.join(map(str, witness_sequence[1:])).encode('ascii')).hexdigest(),
                   literal_endpoint_updates=depth)
    canonical_root = witness_root - 2
    higher_word = set(canonical_fibonacci_indices(canonical_root, witness_fibonacci))
    assert sorted(higher_word) == list(range(13, 32, 2))
    canonical_rows = []
    canonical_literal_updates = 0
    option_count = 1
    for offset in offsets:
        current = canonical_root + offset
        assert set(canonical_fibonacci_indices(current, witness_fibonacci)) == (
            higher_word | set(canonical_fibonacci_indices(offset, witness_fibonacci)))
        current_gap = witness_fibonacci[witness_order] - current
        current_map = {letter: first_cap - witness_sequence[anchor - current_gap + letter]
                       for letter in alphabet}
        periodic = set()
        for letter in alphabet:
            states, transient, period = response_state_orbit(current_map, letter)
            periodic.update(states[transient:])
        option_count *= len(periodic)
        trajectory, transient, period = full_orbit(witness_sequence, current)
        endpoint = current - 1
        for iteration in range(witness_sequence[current - 1]):
            endpoint = current - witness_sequence[endpoint]
        assert endpoint == witness_splits[current]
        assert witness_sequence[endpoint] + witness_sequence[current - endpoint] == witness_sequence[current]
        canonical_literal_updates += witness_sequence[current - 1]
        canonical_rows.append(dict(offset=offset, index=current, value=witness_sequence[current],
                                   cap=anchor - witness_sequence[current], split=endpoint,
                                   period=period, periodic_states=sorted(periodic)))
    scalar_joint = canonical_rows[4]['value'] - canonical_rows[1]['value'] - canonical_rows[3]['value'] + canonical_rows[0]['value']
    index_joint = canonical_rows[4]['split'] - canonical_rows[1]['split'] - canonical_rows[3]['split'] + canonical_rows[0]['split']
    assert scalar_joint == 0 and index_joint == -5 and option_count == 6
    assert [row['period'] for row in canonical_rows] == [1, 3, 2, 1, 1]
    canonical = dict(root=canonical_root, order=witness_order, excess=35,
                     common_higher_fibonacci_indices=sorted(higher_word), rows=canonical_rows,
                     scalar_joint=scalar_joint, index_joint=index_joint,
                     full_periodic_option_count=option_count,
                     conditional_option_bits=(option_count - 1).bit_length(),
                     literal_endpoint_updates=canonical_literal_updates,
                     scope='One finite actual canonical FIB window, including a three-cycle row. Zero current scalar interaction coexists with index interaction-5. The option count allows periodic rows independently and is not actual input cost or an infinite family.')
    return dict(alphabet=list(alphabet), stencil_subtractions=list(stencil),
                synthetic_maps=synthetic_maps, synthetic_starts=synthetic_starts,
                synthetic_direct_updates=direct_updates, maximum_response_transient=maximum_transient,
                synthetic_periods=sorted(observed_periods), shared_five_row_positions=shared_positions,
                shared_response_count=len(shared_positions), full_response_word_options=6 ** 15,
                relaxed_response_word_bits=39, sharp_shared_word=sharp_word, sharp_five_maps=sharp_maps,
                relaxed_periodic_output_options=6 ** 5, sharp_periodic_output_bits=13,
                actual_orders_inclusive=[27, 30], actual_roots=actual_roots,
                actual_period_counts=actual_periods, actual_five_windows=five_windows,
                landing_tail_reads=landing_tail_reads, low_cap_extra_lookahead_reads=extra_lookahead_reads,
                actual_literal_endpoint_updates=literal_updates, three_cycle_witness=witness,
                canonical_three_cycle_window=canonical,
                binary_prefix=binary_prefix_audit(witness_sequence, witness_splits, witness_fibonacci),
                scope='Written conjugacy and two-step landing decoder hold at K>=27, d9..43 without frontier flatness, using existing finite-alphabet premises. Six shared stencil answers give every periodic option and no parent cap is supplied. Five additive rows share15 answers for d16..43. Exact39bit word and13bit phase costs concern relaxed independent response/periodic-output contracts, not actual-C input minima. Landings, clock residues, actual response words and wider recursive evolution remain supplied or open; global dispersion is unchanged.')


def cap4_tail_query_domain(order, gap):
    frontier = higher_cap_width(order - 1, 3)
    excess = gap - frontier
    assert order >= 22 and excess >= 5
    return dict(minimum_gap=frontier + min(5, excess - 4), maximum_gap=gap - 4,
                maximum_first_cap=max(4, excess - 5), maximum_queries=max(1, excess - 8))


def cap4_tail_predecessor(order, gap, profile):
    domain = cap4_tail_query_domain(order, gap)
    seed = gap - 4
    point = seed
    for period in range(1, domain['maximum_queries'] + 1):
        assert domain['minimum_gap'] <= point <= domain['maximum_gap']
        defect = profile(point)
        assert 4 <= defect <= domain['maximum_first_cap']
        following = gap - defect
        if following == seed:
            assert defect == 4
            return point, period
        point = following
    raise AssertionError('The supplied cap4 seed did not return inside its shelf domain.')


def cap4_profile_response_audit():
    contexts = 0
    completions = 0
    checked_profile_positions = 0
    checked_start_maps = 0
    witness = None
    fibonacci = [0, 1]
    while len(fibonacci) <= 120:
        fibonacci.append(sum(fibonacci[-2:]))
    for order in range(24, 121):
        if order % 3 == 1:
            continue
        frontier = higher_cap_width(order - 1, 3)
        lower_zero_width = negative_plateau_width(order - 2)
        gap = frontier + lower_zero_width + 5
        seed = gap - 4
        depth = fibonacci[order - 1] - 4
        assert depth % 2 == 1 and gap + 1 <= fibonacci[order - 4]
        first_widths = [higher_cap_width(order - 1, level) for level in range(4)]
        second_widths = [higher_cap_width(order - 2, level) for level in range(4)]
        first_base = [next((level for level in range(4) if point <= first_widths[level]), 4)
                      for point in range(gap + 2)]
        second = [next((level for level in range(4) if point <= second_widths[level]), 4)
                  for point in range(gap + 2)]
        for ceiling in (5, 9, 16, 31):
            if lower_zero_width < ceiling + 2:
                continue
            common_truncation = first_base[:]
            common_truncation[seed] = ceiling
            common_support = [point for point, defect in enumerate(first_base)
                              if defect == 4 and point != seed]
            selected_gaps = []
            for response in range(ceiling + 1, lower_zero_width + 1):
                first = first_base[:]
                first[seed] = response
                assert [min(defect, ceiling) for defect in first] == common_truncation
                assert [point for point, defect in enumerate(first) if defect == 4] == common_support
                for child_order, profile in ((order - 1, first), (order - 2, second)):
                    child_widths = [higher_cap_width(child_order, level) for level in range(4)]
                    budget = (child_order - 2) ** 2 // 3 - 3 * child_order + 30
                    for point, defect in enumerate(profile):
                        assert 0 <= defect <= 2 * point // 3
                        assert not defect or point <= defect * budget
                        for level, child_frontier in enumerate(child_widths):
                            if point > child_frontier:
                                assert level + 1 <= defect <= max(level + 1, point - child_frontier - 1)
                        checked_profile_positions += 1
                selected, period = cap4_tail_predecessor(order, gap, first.__getitem__)
                assert period == 2 and selected == gap - response
                assert first[selected] == 4 and second[response] == 0
                assert first[seed] == response and second[4] == 0
                first_index = fibonacci[order - 1] - selected
                second_index = fibonacci[order - 2] - response
                numerator = (fibonacci[order - 2] * second_index
                             - fibonacci[order - 3] * first_index)
                assert 100 * numerator * numerator >= gap * gap * first_index * second_index
                neighbor_fixed = gap + 1 - 4
                for start in range(gap + 2):
                    point = start
                    for iteration in range(2):
                        point = gap + 1 - first[point]
                    assert point == neighbor_fixed
                    checked_start_maps += 1
                assert first[neighbor_fixed] == 4 and second[4] == 0
                selected_gaps.append(selected)
                completions += 1
            assert len(set(selected_gaps)) == lower_zero_width - ceiling
            contexts += 1
            if order == 30 and ceiling == 9:
                witness = dict(order=order, profile_ceiling=ceiling, frontier=frontier,
                               zero_width=lower_zero_width, root_gap=gap, periodic_seed=seed,
                               common_depth=depth, common_period=2,
                               response_values=list(range(ceiling + 1, lower_zero_width + 1)),
                               selected_gaps=selected_gaps,
                               exact_fixed_length_summary_bits=(len(selected_gaps) - 1).bit_length())
    assert witness is not None
    return dict(model_orders_inclusive=[24, 120], model_profile_ceilings=[5, 9, 16, 31],
                model_contexts=contexts, model_completions=completions,
                checked_profile_positions=checked_profile_positions,
                checked_neighbor_start_maps=checked_start_maps, model_collision=witness,
                common_one_step_quadratic_constant='1/100',
                scope='Captured-map models, not alternative actual Cloitre sequences. Identical cap0..3 bands, shelves, local cap budgets, truncated first profile and complete cap4 membership support admit distinct selected children with the same odd local depth and period2. The omitted scalar response ranges from h+1 to L_(K-2), giving exactly ceil(log2(L_(K-2)-h)) summary bits in this family. Actual exterior qualification and globally nested profile construction are not asserted.')


def higher_projection_and_allocation_audit(sequence, splits, fibonacci):
    jump_cases = 0
    for initial_order in range(22, 101):
        for level in (2, 3):
            for initial_gap in range(higher_cap_width(initial_order, level - 1) + 1,
                                     higher_cap_width(initial_order, level) + 1):
                gap = initial_gap
                for target_order in range(initial_order, 20, -1):
                    assert gap == higher_cap_first_spine_gap(initial_order, initial_gap, target_order, level)
                    if target_order > 21:
                        gap -= higher_cap_shift(target_order, gap)
                    jump_cases += 1
    synthetic_profiles = 0
    synthetic_seeds = 0
    for gap in range(1, 5):
        for profile in product(range(gap + 1), repeat=gap + 1):
            cycles = capped_profile_cycles(profile, gap)
            periodic = {point for cycle in cycles for point in cycle}
            for seed in range(gap + 1):
                decoded = periodic_predecessor_gap(gap, seed, profile.__getitem__)
                if seed not in periodic:
                    assert decoded is None
                else:
                    predecessors = [point for point in periodic if gap - profile[point] == seed]
                    assert len(predecessors) == 1 and decoded[0] == predecessors[0]
                    assert decoded[1] == next(len(cycle) for cycle in cycles if seed in cycle)
                synthetic_seeds += 1
            synthetic_profiles += 1
    actual_projection_states = 0
    cap4_rows = []
    cap4_spine_edges = 0
    tail_roots = 0
    tail_profile_queries = 0
    maximum_tail_query_cap = 0
    tail_period_counts = {}
    minimum_variance_ratio = None
    period_witnesses = {}
    allocation_roots = 0
    allocation_option_counts = {}
    maximum_allocation_options = 0
    for order in range(22, 31):
        anchor = fibonacci[order]
        first_anchor = fibonacci[order - 1]
        first_cap = fibonacci[order - 2]
        second_anchor = fibonacci[order - 2]
        second_cap = fibonacci[order - 3]
        for level in (2, 3):
            for initial_gap in range(higher_cap_width(order, level - 1) + 1,
                                     higher_cap_width(order, level) + 1):
                current = anchor - initial_gap
                for target_order in range(order, 20, -1):
                    predicted = higher_cap_first_spine_gap(order, initial_gap, target_order, level)
                    assert current == fibonacci[target_order] - predicted
                    assert fibonacci[target_order - 1] - sequence[current] == level
                    actual_projection_states += 1
                    if target_order > 21:
                        current = splits[current]
        roots = 0
        shifts = set()
        periods = set()
        maximum_gap = 0
        for gap in range(fibonacci[order - 2] + 1):
            root = anchor - gap
            parent_cap = first_anchor - sequence[root]
            if 4 <= parent_cap <= 8:
                candidates = allocation_seed_candidates(order, gap, parent_cap, sequence, fibonacci)
                assert 1 <= len(candidates) <= parent_cap - 3
                selected_second_cap = second_cap - sequence[root - splits[root]]
                selected = [row for row in candidates if row['second_cap_defect'] == selected_second_cap]
                assert len(selected) == 1 and selected[0]['selected_split'] == splits[root]
                assert len({row['selected_split'] for row in candidates}) == len(candidates)
                allocation_roots += 1
                allocation_option_counts[str(len(candidates))] = allocation_option_counts.get(str(len(candidates)), 0) + 1
                maximum_allocation_options = max(maximum_allocation_options, len(candidates))
            if parent_cap != 4:
                continue
            first = splits[root]
            second = root - first
            assert first_cap - sequence[first] == 4
            assert second_cap - sequence[second] == 0
            lower_profile = lambda point: first_cap - sequence[first_anchor - point]
            selected_gap, period = periodic_predecessor_gap(gap, gap - 4, lower_profile)
            assert first == first_anchor - selected_gap
            if gap >= higher_cap_width(order - 1, 3) + 5:
                query_domain = cap4_tail_query_domain(order, gap)
                queried_caps = []
                def restricted_profile(point):
                    assert query_domain['minimum_gap'] <= point <= query_domain['maximum_gap']
                    defect = lower_profile(point)
                    queried_caps.append(defect)
                    return defect
                restricted_gap, restricted_period = cap4_tail_predecessor(order, gap, restricted_profile)
                assert (restricted_gap, restricted_period) == (selected_gap, period)
                assert len(set(queried_caps)) == period and queried_caps[-1] == 4
                assert 4 <= gap - selected_gap <= negative_plateau_width(order - 2)
                tail_roots += 1
                tail_profile_queries += len(queried_caps)
                maximum_tail_query_cap = max(maximum_tail_query_cap, max(queried_caps))
                tail_period_counts[str(period)] = tail_period_counts.get(str(period), 0) + 1
            profile = [lower_profile(point) for point in range(gap + 1)]
            cycles = capped_profile_cycles(profile, gap)
            scalar_valid = []
            for cycle in cycles:
                for point in cycle:
                    first_point = first_anchor - point
                    second_point = root - first_point
                    if sequence[first_point] + sequence[second_point] == sequence[root]:
                        scalar_valid.append(point)
                    if gap >= higher_cap_width(order - 1, 3) + 5:
                        assert sequence[first_point] + sequence[second_point] <= sequence[root]
            assert scalar_valid == [selected_gap]
            numerator = first_cap * second - second_cap * first
            assert 100 * numerator * numerator >= gap * gap * first * second
            golden_defect = sequence[root] - g_closed(root)
            if golden_defect:
                ratio = Fraction(numerator * numerator, first * second * golden_defect * golden_defect)
                minimum_variance_ratio = ratio if minimum_variance_ratio is None else min(minimum_variance_ratio, ratio)
            current = root
            for target_order in range(order, 21, -1):
                first = splits[current]
                second = current - first
                assert fibonacci[target_order - 2] - sequence[first] == 4
                assert fibonacci[target_order - 3] - sequence[second] == 0
                current = first
                cap4_spine_edges += 1
            if period not in period_witnesses:
                period_witnesses[period] = dict(order=order, gap=gap, index=root,
                                               value=sequence[root], selected=splits[root],
                                               depth=sequence[root - 1], shift=gap - selected_gap,
                                               period=period)
            roots += 1
            shifts.add(gap - selected_gap)
            periods.add(period)
            maximum_gap = max(maximum_gap, gap)
        cap4_rows.append(dict(order=order, cap4_roots=roots, maximum_gap=maximum_gap,
                              selected_shifts=sorted(shifts), selected_periods=sorted(periods)))
    literal_updates = 0
    witness_rows = []
    for root in (310, 17629):
        order = bisect.bisect_left(fibonacci, root)
        gap = fibonacci[order] - root
        parent_cap = fibonacci[order - 1] - sequence[root]
        trajectory, transient, period = full_orbit(sequence, root)
        cycle = trajectory[transient:]
        candidates = allocation_seed_candidates(order, gap, parent_cap, sequence, fibonacci)
        supplied_cycle_candidates = [row for row in candidates if row['selected_split'] in cycle]
        assert len(supplied_cycle_candidates) == 2
        expected = {(182, 3), (185, 7)} if root == 310 else {(10870, 0), (10875, 1)}
        assert {(row['selected_split'], row['second_cap_defect']) for row in supplied_cycle_candidates} == expected
        endpoint = root - 1
        depth = sequence[root - 1]
        for iteration in range(depth):
            endpoint = root - sequence[endpoint]
        assert endpoint == splits[root]
        literal_updates += depth
        witness_rows.append(dict(order=order, root=root, gap=gap, value=sequence[root],
                                 parent_cap_defect=parent_cap, depth=depth, selected=endpoint,
                                 transient=transient, cycle=cycle,
                                 allocation_seed_candidates=candidates,
                                 supplied_cycle_phase_code_bits=1))
    for witness in period_witnesses.values():
        root = witness['index']
        endpoint = root - 1
        for iteration in range(witness['depth']):
            endpoint = root - sequence[endpoint]
        assert endpoint == splits[root]
        literal_updates += witness['depth']
    response_models = cap4_profile_response_audit()
    response_witness = response_models['model_collision']
    response_order = response_witness['order'] - 2
    descendant_gaps = {target_order: set() for target_order in range(19, response_order + 1)}
    actual_response_states = 0
    for response in response_witness['response_values']:
        current = fibonacci[response_order] - response
        for target_order in range(response_order, 18, -1):
            target_gap = min(response, negative_plateau_width(target_order))
            assert current == fibonacci[target_order] - target_gap
            assert sequence[current] == fibonacci[target_order - 1]
            descendant_gaps[target_order].add(target_gap)
            actual_response_states += 1
            if target_order > 19:
                current = splits[current]
    response_models['actual_zero_child_descendant_states'] = actual_response_states
    response_models['actual_zero_child_descendant_rows'] = [
        dict(order=target_order, gaps=sorted(descendant_gaps[target_order]),
             distinct_child_indices=len(descendant_gaps[target_order]))
        for target_order in range(response_order, 18, -1)]
    return dict(arithmetic_projection_orders_inclusive=[22, 100], arithmetic_projection_cases=jump_cases,
                actual_projection_states=actual_projection_states, boundary_order=21,
                synthetic_profiles=synthetic_profiles, synthetic_seed_cases=synthetic_seeds,
                actual_cap4_complete_block_orders_inclusive=[22, 30], cap4_block_rows=cap4_rows,
                actual_cap4_first_spine_edges=cap4_spine_edges,
                cap4_period_witnesses=list(period_witnesses.values()),
                actual_allocation_root_caps_inclusive=[4, 8], actual_allocation_roots=allocation_roots,
                allocation_option_counts=allocation_option_counts, maximum_allocation_options=maximum_allocation_options,
                cap4_one_step_quadratic_constant='1/100', minimum_cap4_quadratic_ratio=str(minimum_variance_ratio),
                actual_allocation_witnesses=witness_rows, literal_selected_endpoint_updates=literal_updates,
                tail_query_interface=dict(actual_tail_roots=tail_roots,
                                          actual_profile_queries=tail_profile_queries,
                                          maximum_observed_query_cap=maximum_tail_query_cap,
                                          actual_period_counts=tail_period_counts,
                                          profile_response_models=response_models),
                cap4_generated_band=cap4_generated_band_audit(sequence, splits, fibonacci),
                bounded_tail_shelf=bounded_tail_shelf_audit(sequence, splits, fibonacci),
                finite_tail_alphabet=finite_tail_alphabet_audit(sequence, splits, fibonacci),
                frontier_reset=frontier_reset_audit(sequence, splits, fibonacci),
                frontier_copy_holes=frontier_copy_hole_audit(sequence, splits, fibonacci),
                six_response_map=six_response_map_audit(sequence, splits, fibonacci),
                copy_clock_variation=copy_clock_variation_audit(sequence, splits, fibonacci),
                ternary_support=ternary_support_audit(),
                scope='Direct cap2/3 projection and cap4 single-defect closure/periodic seed follow from existing higher-cap shelves. A supplied actual second-child cap determines the periodic predecessor without separate entrance/depth/cycle labels; its admissible range is0..e-4 at K>=22. Exact phase-code size counts scalar-valid allocation options, not independent-input lower bounds for actual C. Actual310 five-cycle and17629 branching each realize two options. Full profile construction, wide-block allocation and global dispersion remain open.')


def higher_cap_closure_audit(sequence, splits, fibonacci):
    literal, literal_updates = literal_generate(fibonacci[21])
    assert literal == sequence[:fibonacci[21] + 1] == brent_generate(fibonacci[21])
    base_rows = []
    for level, order in ((2, 20), (3, 21)):
        profile = [fibonacci[order - 1] - sequence[fibonacci[order] - gap]
                   for gap in range(fibonacci[order - 2] + 1)]
        width = higher_cap_width(order, level)
        assert all((defect <= level) == (gap <= width)
                   for gap, defect in enumerate(profile))
        assert all(level + 1 <= defect <= max(level + 1, gap - width - 1)
                   for gap, defect in enumerate(profile) if gap > width)
        base_rows.append(dict(level=level, order=order, width=width,
                              full_gap_positions=len(profile),
                              profile_sha256=hashlib.sha256(','.join(map(str, profile)).encode('ascii')).hexdigest()))
    lower_bound_checks = 0
    for order, level in ((19, 2), (20, 3)):
        for gap in range(fibonacci[order - 2] + 1):
            defect = fibonacci[order - 1] - sequence[fibonacci[order] - gap]
            assert defect <= max(0, gap - 2 * level - 2)
            lower_bound_checks += 1
    abstract_profiles = 0
    abstract_readouts = 0
    for level in (2, 3):
        for lower_width in (2, 3):
            for width in range(lower_width + level + 1, lower_width + level + 4):
                for previous in product(range(level), repeat=lower_width + 1):
                    for gap in range(lower_width + level + 1, width + level + 5):
                        ranges = [range(level + 1, max(level + 1, point - width - 1) + 1)
                                  for point in range(width + 1, gap + 1)]
                        for tail in product(*ranges):
                            profile = (list(previous) + [level] * (width - lower_width) + list(tail))[:gap + 1]
                            cycles = capped_profile_cycles(profile, gap)
                            if gap <= width + level:
                                assert cycles == [(gap - level,)]
                            elif gap == width + level + 1:
                                assert len(cycles) == 1 and set(cycles[0]) == {width, width + 1}
                            else:
                                for cycle in cycles:
                                    for point in cycle:
                                        complement = gap - point
                                        assert width < point <= gap - level - 1
                                        upper_readout = profile[point] + max(0, complement - 2 * level - 2)
                                        assert level + 1 <= upper_readout <= max(level + 1, gap - width - level - 2)
                                        abstract_readouts += 1
                            abstract_profiles += 1
    block_positions = 0
    selector_rows = 0
    phase_rows = 0
    spine_steps = 0
    boundary_rows = []
    dispersion_minimum = None
    dispersion_witness = None
    for order in range(20, 31):
        anchor, cap = fibonacci[order], fibonacci[order - 1]
        for gap in range(fibonacci[order - 2] + 1):
            defect = cap - sequence[anchor - gap]
            for level in (2, 3):
                if level == 3 and order < 21:
                    continue
                width = higher_cap_width(order, level)
                assert (defect <= level) == (gap <= width)
                if gap > width:
                    assert level + 1 <= defect <= max(level + 1, gap - width - 1)
            block_positions += 1
        for level in (2, 3):
            if order <= 20 + int(level == 3):
                continue
            previous = higher_cap_width(order - 1, level)
            assert previous + level + 2 < fibonacci[order - 3]
            assert previous - higher_cap_width(order - 1, level - 1) >= level + 1
            parity = int((cap - level - 1) % 2 == 0)
            assert higher_cap_width(order, level) == previous + level + parity
            gap = previous + level + 1
            index = anchor - gap
            trajectory, transient, period = full_orbit(sequence, index)
            lower, upper = cap - previous - 1, cap - previous
            assert period == 2 and set(trajectory[transient:]) == {lower, upper}
            assert all(point >= upper if position % 2 == 0 else point <= lower
                       for position, point in enumerate(trajectory))
            assert sequence[index - 1] == cap - level - 1
            assert splits[index] == (upper if parity else lower)
            assert cap - sequence[index] == level + 1 - parity
            boundary_rows.append(dict(order=order, level=level, gap=gap, depth=sequence[index - 1],
                                      cycle=[lower, upper], transient=transient,
                                      selected_shift=level + parity, cap_defect=level + 1 - parity))
        if order < 22:
            continue
        frontiers = [higher_cap_width(order - 1, level) + level + 1 for level in range(4)]
        for gap in range(higher_cap_width(order, 3) + 1):
            index = anchor - gap
            defect = next(level for level in range(4) if gap <= higher_cap_width(order, level))
            shift = higher_cap_shift(order, gap)
            split = cap - gap + shift
            assert split == splits[index] and sequence[index] == cap - defect
            assert sequence[split] == fibonacci[order - 2] - defect
            assert sequence[index - split] == fibonacci[order - 3]
            trajectory, transient, period = full_orbit(sequence, index)
            cycle = trajectory[transient:]
            if gap in frontiers:
                boundary_level = frontiers.index(gap)
                assert set(cycle) == {cap - gap + boundary_level, cap - gap + boundary_level + 1}
            else:
                assert list(cycle) == [split]
            selector_rows += 1
            spine_order, spine_gap = order, gap
            while spine_order >= 22:
                spine_gap -= higher_cap_shift(spine_order, spine_gap)
                spine_order -= 1
                assert spine_gap <= higher_cap_width(spine_order, defect)
                assert sequence[fibonacci[spine_order] - spine_gap] == fibonacci[spine_order - 1] - defect
                spine_steps += 1
            golden_defect = sequence[index] - g_closed(index)
            assert 0 <= golden_defect <= gap
            for point in cycle:
                complement = index - point
                phase_shift = point - (cap - gap)
                numerator = fibonacci[order - 2] * complement - fibonacci[order - 3] * point
                assert numerator == (-1) ** (order - 1) + fibonacci[order - 3] * gap - cap * phase_shift
                assert 0 <= phase_shift <= 4
                if phase_shift:
                    assert gap >= 6 * phase_shift + 2
                if gap:
                    assert 2 * numerator >= fibonacci[order - 3] * gap
                assert 25 * numerator ** 2 >= gap ** 2 * point * complement
                assert 25 * numerator ** 2 >= golden_defect ** 2 * point * complement
                if golden_defect:
                    ratio = Fraction(numerator ** 2, point * complement * golden_defect ** 2)
                    if dispersion_minimum is None or ratio < dispersion_minimum:
                        dispersion_minimum = ratio
                        dispersion_witness = dict(order=order, gap=gap, phase_shift=phase_shift,
                                                  golden_defect=golden_defect)
                phase_rows += 1
    gaps = [0, 16, 31, 56, 69]
    shifts = [higher_cap_shift(28, gap) for gap in gaps]
    defects = [next(level for level in range(4) if gap <= higher_cap_width(28, level)) for gap in gaps]
    assert shifts == [0, 0, 2, 2, 4] and defects == [0, 1, 1, 2, 3]
    parent_parameters, first_parameters, second_parameters = [], [], []
    for row, gap in enumerate(gaps):
        following = (row + 1) % 5
        index = fibonacci[28] - gap
        split = splits[index]
        first_offset = fibonacci[25] - gap + shifts[row]
        second_offset = fibonacci[24] - shifts[row]
        assert split - fibonacci[26] == first_offset
        assert index - split - fibonacci[25] == second_offset
        parent_parameter = fibonacci[27] - gaps[following] - defects[row]
        first_parameter = fibonacci[26] - gaps[following] + shifts[following] - defects[row]
        second_parameter = fibonacci[25] - shifts[following]
        assert first_parameter + second_parameter == parent_parameter
        first_profile = sequence[split] - fibonacci[25]
        second_profile = sequence[index - split] - fibonacci[24]
        assert first_profile == fibonacci[24] - defects[row]
        assert second_profile == fibonacci[23]
        assert fibonacci[25] - gaps[following] + shifts[following] + first_profile == first_parameter
        assert fibonacci[24] - shifts[following] + second_profile == second_parameter
        parent_parameters.append(parent_parameter)
        first_parameters.append(first_parameter)
        second_parameters.append(second_parameter)
    counterexample = []
    for gap in (55, 57):
        index = fibonacci[20] - gap
        defect = fibonacci[19] - sequence[index]
        assert defect == (5 if gap == 55 else 4)
        counterexample.append(dict(gap=gap, index=index, cap_defect=defect, selected_split=splits[index]))
    return dict(base_rows=base_rows, literal_and_brent_checked_through=fibonacci[21],
                base_literal_updates=literal_updates, lower_gap_bound_checks=lower_bound_checks,
                abstract_profiles=abstract_profiles, abstract_periodic_upper_readouts=abstract_readouts,
                level2_width='floor(8k/3)-18, k>=20',
                level3_width='3k+floor((k-1)/3)-24, k>=21',
                actual_complete_block_orders_inclusive=[20, 30], actual_block_positions=block_positions,
                actual_selector_rows=selector_rows, first_spine_steps=spine_steps,
                boundary_phase_rows=boundary_rows, all_basin_phase_variance_checks=phase_rows,
                quadratic_constant='1/25', basin_ratio_minimum=str(dispersion_minimum),
                basin_ratio_witness=dispersion_witness,
                five_row_witness=dict(order=28, gaps=gaps, shifts=shifts, cap_defects=defects,
                                      parent_parameters=parent_parameters,
                                      first_parameters=first_parameters, second_parameters=second_parameters,
                                      residual_selector_labels=0),
                actual_level4_noncontiguity=counterexample,
                direct_projection_and_allocation=higher_projection_and_allocation_audit(sequence, splits, fibonacci),
                scope='Independent full-block finite premises and abstract shelf graphs support the written phase-selected level2/3 induction. Arithmetic supplied-order/gap selectors close cap-defect0..3 along one first-child spine to base20/21; context/table costs separate. All basin phases satisfy the scoped quadratic bound. Actual level4 holes forbid arbitrary-level extrapolation; no global dispersion, convergence, full-interface minimum or Lean claim.')


def cap_gap_budget(order):
    assert order >= 9
    if order == 9:
        return 13
    return (order - 2) ** 2 // 3 - 3 * order + 30


def local_cap_endpoint(gap, start_gap, remaining, profile):
    assert 0 <= start_gap <= gap and remaining >= 0
    point = start_gap
    positions = {}
    trajectory = []
    while point not in positions:
        positions[point] = len(trajectory)
        trajectory.append(point)
        point = gap - profile[point]
        assert 0 <= point <= gap
    transient = positions[point]
    period = len(trajectory) - transient
    assert len(trajectory) <= gap + 1
    selected = (trajectory[remaining] if remaining < len(trajectory)
                else trajectory[transient + (remaining - transient) % period])
    return selected, transient, period


def fibonacci_mod(order, modulus):
    assert order >= 0 and modulus >= 1
    first, second = 0, 1 % modulus
    for digit in bin(order)[2:]:
        doubled = first * (2 * second - first) % modulus
        following = (first * first + second * second) % modulus
        if digit == '0':
            first, second = doubled, following
        else:
            first, second = following, (doubled + following) % modulus
    return first


def fibonacci_capped(order, threshold):
    assert order >= 0 and threshold >= 0
    first, second = 0, min(1, threshold)
    position = 0
    while position < order and first < threshold:
        first, second = second, min(threshold, first + second)
        position += 1
    return first


def symbolic_cap_selector(order, gap, start_gap, entrance, predecessor_defect, profile):
    assert order >= 1 and 0 <= start_gap <= gap
    assert entrance >= 0 and predecessor_defect >= 0 and len(profile) >= gap + 1

    def following(point):
        result = gap - profile[point]
        assert 0 <= result <= gap
        return result

    slow = following(start_gap)
    fast = following(following(start_gap))
    while slow != fast:
        slow = following(slow)
        fast = following(following(fast))
    cycle_entry = start_gap
    transient = 0
    while cycle_entry != slow:
        cycle_entry = following(cycle_entry)
        slow = following(slow)
        transient += 1
    period = 1
    point = following(cycle_entry)
    while point != cycle_entry:
        point = following(point)
        period += 1
    assert transient + period <= gap + 1
    threshold = predecessor_defect + entrance + transient
    assert fibonacci_capped(order - 1, threshold) == threshold
    residue = (fibonacci_mod(order - 1, period) - predecessor_defect - entrance - transient) % period
    selected = cycle_entry
    for step in range(residue):
        selected = following(selected)
    return dict(selected_gap=selected, local_transient=transient,
                period=period, cycle_entry_gap=cycle_entry, selected_residue=residue)


def modular_selector_audit(sequence, splits, fibonacci):
    def matrix_product(left, right, modulus):
        return tuple(tuple(sum(left[row][middle] * right[middle][column] for middle in range(2)) % modulus
                           for column in range(2)) for row in range(2))

    def matrix_fibonacci_mod(order, modulus):
        result = ((1, 0), (0, 1))
        power = ((1, 1), (1, 0))
        remaining = order
        while remaining:
            if remaining % 2:
                result = matrix_product(result, power, modulus)
            power = matrix_product(power, power, modulus)
            remaining //= 2
        return result[0][1] % modulus

    modular_checks = capped_checks = 0
    first, second = 0, 1
    moduli = (1, 2, 3, 5, 7, 16, 97, 1009)
    for order in range(1001):
        for modulus in moduli:
            expected = first % modulus
            assert fibonacci_mod(order, modulus) == matrix_fibonacci_mod(order, modulus) == expected
            modular_checks += 1
        for threshold in (0, 1, 2, 13, 100, 10000):
            assert fibonacci_capped(order, threshold) == min(first, threshold)
            capped_checks += 1
        first, second = second, first + second
    huge_orders = (10 ** 100, 10 ** 1000 + 123, 2 ** 4096 + 17)
    huge_rows = []
    for order in huge_orders:
        residues = []
        for modulus in moduli:
            residue = fibonacci_mod(order, modulus)
            assert residue == matrix_fibonacci_mod(order, modulus)
            residues.append(residue)
            modular_checks += 1
        for modulus, pisano in ((2, 3), (3, 8), (5, 20)):
            assert fibonacci_mod(order, modulus) == fibonacci_mod(order % pisano, modulus)
        assert fibonacci_capped(order, 10 ** 100) == 10 ** 100
        huge_rows.append(dict(order_bit_length=order.bit_length(), moduli=list(moduli), residues=residues,
                              capped_threshold_bit_length=(10 ** 100).bit_length()))
    decoded = 0
    phase_period_counts = {}
    maximum_period = None
    maximum_local_transient = None
    witnesses = {}
    actual_modular_rows = []
    for order in range(11, 31):
        anchor, cap = fibonacci[order], fibonacci[order - 1]
        width = min(16 * cap_gap_budget(order), fibonacci[order - 4])
        previous = [fibonacci[order - 2] - sequence[cap - gap] for gap in range(width + 1)]
        lower = [fibonacci[order - 3] - sequence[fibonacci[order - 2] - gap] for gap in range(width + 1)]
        for gap in range(2, width + 1):
            index = anchor - gap
            defect = cap - sequence[index]
            if defect > 16:
                continue
            assert 0 <= defect and gap <= 16 * cap_gap_budget(order)
            trajectory, transient, period = full_orbit(sequence, index)
            entrance = next(position for position, point in enumerate(trajectory)
                            if cap - gap <= point <= cap)
            start_gap = cap - trajectory[entrance]
            predecessor = cap - sequence[index - 1]
            decoded_row = symbolic_cap_selector(order, gap, start_gap, entrance, predecessor, previous)
            selected_gap = decoded_row['selected_gap']
            exact_depth = sequence[index - 1]
            reference_gap, reference_transient, reference_period = local_cap_endpoint(
                gap, start_gap, exact_depth - entrance, previous)
            assert selected_gap == reference_gap == cap - splits[index]
            assert decoded_row['local_transient'] == reference_transient == transient - entrance
            assert decoded_row['period'] == reference_period == period
            assert previous[selected_gap] + lower[gap - selected_gap] == defect
            assert decoded_row['selected_residue'] == (exact_depth - entrance - reference_transient) % period
            decoded += 1
            phase_period_counts[str(period)] = phase_period_counts.get(str(period), 0) + 1
            row = dict(order=order, gap=gap, index=index, cap_defect=defect,
                       entrance_clock=entrance, entrance_gap=start_gap, predecessor_defect=predecessor,
                       exact_depth=exact_depth, exact_depth_bits=exact_depth.bit_length(), **decoded_row)
            if maximum_period is None or period > maximum_period['period']:
                maximum_period = row
            if maximum_local_transient is None or reference_transient > maximum_local_transient['local_transient']:
                maximum_local_transient = row
            if str(period) not in witnesses:
                witnesses[str(period)] = row
            if (order, gap) in ((19, 50), (19, 54), (20, 57), (24, 83)):
                actual_modular_rows.append(row)
    literal_updates = 0
    for row in witnesses.values():
        point = row['index'] - 1
        for step in range(sequence[row['index'] - 1]):
            point = row['index'] - sequence[point]
            literal_updates += 1
        assert point == splits[row['index']] == fibonacci[row['order'] - 1] - row['selected_gap']
    return dict(modular_checks=modular_checks, capped_fibonacci_checks=capped_checks,
                independent_modular_method='2x2 matrix binary exponentiation; exact Fibonacci values through order1000',
                huge_order_arithmetic_rows=huge_rows, huge_order_scope='Modular and capped Fibonacci arithmetic only; no C or actual entrance at these huge orders is evaluated.',
                actual_orders_inclusive=[11, 30], actual_cap_bound=16,
                actual_gap_domain='2<=v<=min(16Pk,F_(k-4)); cap defect<=16',
                actual_symbolic_decodings=decoded, actual_period_counts=phase_period_counts,
                maximum_period=maximum_period, maximum_local_transient=maximum_local_transient,
                actual_phase_witnesses=actual_modular_rows, literal_period_witnesses=list(witnesses.values()),
                literal_selected_updates=literal_updates,
                decoder_formula='F_(k-1) mod p minus predecessor defect, entrance clock and local transient, all modulo p',
                workspace_bound='O(log m+log k) bits with read-only random-access profiles and certified entrance; symbolic anchor/gap outputs',
                scope='Standard Floyd cycle detection and modular Fibonacci doubling implement the proved conditional symbolic decoder. Exact-depth trajectory evaluation and actual literal witnesses cross-check the selected gaps. Profiles, actual predecessor/entrance provenance and their verification are supplied resources; physical integer output, table construction and full recursive minimum remain separate. No global dispersion or large-order C claim.')


def cap_adaptive_dispersion_audit(sequence, splits, fibonacci):
    arithmetic_checks = 0
    for order in range(22, 1001):
        assert higher_cap_width(order, 3) + 1 >= 4 * negative_plateau_width(order - 1) + 4
        arithmetic_checks += 1
    candidate_counts = dict(low_cap_phases=0, zero_child_stops=0, positive_child_branches=0)
    scalar_candidate_checks = 0
    low_cap_graph_checks = 0
    terminal_scalar_mismatches = 0
    independent_choice_checks = 0
    records = {}

    def local_variance(order, gap, first_gap):
        index = fibonacci[order] - gap
        first = fibonacci[order - 1] - first_gap
        second = index - first
        numerator = fibonacci[order - 2] * second - fibonacci[order - 3] * first
        return Fraction(numerator ** 2, index ** 2 * first * second)

    @lru_cache(maxsize=None)
    def stopped_minimum(order, gap):
        nonlocal scalar_candidate_checks, low_cap_graph_checks
        nonlocal terminal_scalar_mismatches, independent_choice_checks
        index = fibonacci[order] - gap
        defect = fibonacci[order - 1] - sequence[index]
        assert order >= 22 + 2 * max(0, defect - 3)
        options = []
        if defect <= 3:
            frontiers = [higher_cap_width(order - 1, level) + level + 1 for level in range(4)]
            if gap in frontiers:
                level = frontiers.index(gap)
                candidates = [gap - level, gap - level - 1]
            else:
                candidates = [gap - higher_cap_shift(order, gap)]
            trajectory, transient, _ = full_orbit(sequence, index)
            assert set(candidates) == {fibonacci[order - 1] - point for point in trajectory[transient:]}
            low_cap_graph_checks += 1
            for first_gap in candidates:
                variance = local_variance(order, gap, first_gap)
                assert variance >= Fraction(gap ** 2, 25 * index ** 2)
                first = fibonacci[order - 1] - first_gap
                terminal_scalar_mismatches += int(sequence[first] + sequence[index - first] != sequence[index])
                candidate_counts['low_cap_phases'] += 1
                options.append((variance, first_gap, 1))
        else:
            assert gap > higher_cap_width(order, 3)
            lower_gap = max(0, gap - fibonacci[order - 4])
            upper_gap = min(gap, fibonacci[order - 3])
            candidates = []
            for first_gap in range(lower_gap, upper_gap + 1):
                first = fibonacci[order - 1] - first_gap
                second = index - first
                first_defect = fibonacci[order - 2] - sequence[first]
                second_defect = fibonacci[order - 3] - sequence[second]
                scalar_candidate_checks += 1
                assert first_defect >= 0 and second_defect >= 0
                if first_defect + second_defect != defect:
                    continue
                candidates.append(first_gap)
                variance = local_variance(order, gap, first_gap)
                if first_defect == 0 or second_defect == 0:
                    zero_gap = first_gap if first_defect == 0 else gap - first_gap
                    zero_order = order - 1 if first_defect == 0 else order - 2
                    assert zero_gap <= negative_plateau_width(zero_order)
                    assert variance >= Fraction(gap ** 2, 100 * index ** 2)
                    height = 1
                    candidate_counts['zero_child_stops'] += 1
                else:
                    assert max(first_defect, second_defect) < defect
                    first_result, first_height, _ = stopped_minimum(order - 1, first_gap)
                    second_result, second_height, _ = stopped_minimum(order - 2, gap - first_gap)
                    variance += Fraction(first, index) * first_result + Fraction(second, index) * second_result
                    height = 1 + max(first_height, second_height)
                    candidate_counts['positive_child_branches'] += 1
                assert variance >= Fraction(gap ** 2, 100 * index ** 2)
                options.append((variance, first_gap, height))
            assert candidates and fibonacci[order - 1] - splits[index] in candidates
            if index <= fibonacci[24]:
                first_lower = fibonacci[order - 1] - upper_gap
                first_upper = fibonacci[order - 1] - lower_gap
                independent = [fibonacci[order - 1] - first
                               for first in range(first_lower, first_upper + 1)
                               if sequence[first] + sequence[index - first] == sequence[index]]
                assert set(independent) == set(candidates)
                independent_choice_checks += len(independent)
        best = min(options)
        height = max(option[2] for option in options)
        assert height <= max(1, defect - 2)
        records[(order, gap)] = (defect, best[1])
        return best[0], height, best[1]

    @lru_cache(maxsize=None)
    def actual_variance(order, gap, depth):
        if depth == 0:
            return Fraction(0)
        index = fibonacci[order] - gap
        first = splits[index]
        second = index - first
        first_gap = fibonacci[order - 1] - first
        second_gap = fibonacci[order - 2] - second
        return (local_variance(order, gap, first_gap)
                + Fraction(first, index) * actual_variance(order - 1, first_gap, depth - 1)
                + Fraction(second, index) * actual_variance(order - 2, second_gap, depth - 1))

    roots = 0
    defect_counts = {}
    minimum_ratio = None
    minimum_witness = None
    off_basin_choices = 0
    off_basin_witness = None
    nonperiodic_choices = 0
    nonperiodic_witness = None
    literal_rows = {}
    for order in range(22, 31):
        width = min(7 * cap_gap_budget(order), fibonacci[order - 2])
        for gap in range(width + 1):
            index = fibonacci[order] - gap
            defect = fibonacci[order - 1] - sequence[index]
            if defect > 7 or order < 22 + 2 * max(0, defect - 3):
                continue
            bound, height, first_gap = stopped_minimum(order, gap)
            depth = max(1, defect - 2)
            actual = actual_variance(order, gap, depth)
            assert bound <= actual
            assert bound >= Fraction(gap ** 2, 100 * index ** 2)
            golden_defect = sequence[index] - g_closed(index)
            assert 0 <= golden_defect <= gap
            assert actual >= Fraction(golden_defect ** 2, 100 * index ** 2)
            if defect <= 6:
                assert actual_variance(order, gap, 4) >= bound
            roots += 1
            defect_counts[str(defect)] = defect_counts.get(str(defect), 0) + 1
            if gap:
                ratio = bound * Fraction(index ** 2, gap ** 2)
                if minimum_ratio is None or ratio < minimum_ratio:
                    minimum_ratio = ratio
                    minimum_witness = dict(order=order, gap=gap, index=index, cap_defect=defect,
                                           horizon=depth, maximum_stopped_height=height,
                                           selected_first_gap=fibonacci[order - 1] - splits[index],
                                           minimizing_first_gap=first_gap, stopped_variance=str(bound),
                                           actual_variance=str(actual))
            if defect > 3:
                trajectory, transient, _ = full_orbit(sequence, index)
                selected = fibonacci[order - 1] - first_gap
                if selected not in trajectory[transient:]:
                    off_basin_choices += 1
                    if off_basin_witness is None:
                        off_basin_witness = dict(order=order, gap=gap, index=index, cap_defect=defect,
                                                minimizing_first_gap=first_gap, minimizing_split=selected,
                                                actual_split=splits[index], stopped_variance=str(bound))
                point = selected
                visited = set()
                while point not in visited:
                    visited.add(point)
                    assert fibonacci[order - 1] - gap <= point <= fibonacci[order - 1]
                    point = index - sequence[point]
                if point != selected:
                    nonperiodic_choices += 1
                    if nonperiodic_witness is None:
                        nonperiodic_witness = dict(order=order, gap=gap, index=index, cap_defect=defect,
                                                  minimizing_split=selected, actual_split=splits[index],
                                                  entry_point=point, visited_points=len(visited))
                if str(defect) not in literal_rows:
                    literal_rows[str(defect)] = dict(order=order, gap=gap, index=index,
                                                     cap_defect=defect, split=splits[index], horizon=depth)
    literal_updates = 0
    for row in literal_rows.values():
        point = row['index'] - 1
        for step in range(sequence[row['index'] - 1]):
            point = row['index'] - sequence[point]
            literal_updates += 1
        assert point == row['split']
    return dict(constant='1/100', horizon='max(1,e-2)',
                order_threshold='22+2max(0,e-3)', root_orders_inclusive=[22, 30], cap_bound=7,
                arithmetic_threshold_checks=arithmetic_checks, actual_roots=roots,
                root_cap_defect_counts=defect_counts, stopped_contexts=len(records),
                scalar_candidate_checks=scalar_candidate_checks, admissible_candidate_counts=candidate_counts,
                independent_complementary_sum_choices=independent_choice_checks,
                arithmetic_low_cap_basin_checks=low_cap_graph_checks,
                final_low_cap_phases_with_different_scalar=terminal_scalar_mismatches,
                minimum_stopped_ratio_to_gap_squared=str(minimum_ratio), minimum_witness=minimum_witness,
                minimizing_high_cap_choices_outside_prescribed_basin=off_basin_choices,
                off_basin_witness=off_basin_witness,
                minimizing_high_cap_nonperiodic_choices=nonperiodic_choices,
                nonperiodic_witness=nonperiodic_witness, literal_rows=list(literal_rows.values()),
                literal_updates=literal_updates,
                scope='The written cap-adaptive stopping/induction proof uses integer child-cap conservation, the exact zero plateau and the previously proved cap0..3 basin inequality; no new infinite sequence premise. Above cap3 the stopped minimum permits every scalar-valid geometric split, without orbit, entrance or phase qualification. Low-cap finishing uses the arithmetic prescribed-basin kernel. This envelope is compared with actual accumulated variance at every qualifying bounded-cap root, preserving inherited labels. A four-generation quadratic bound follows on cap<=6, not on unbounded caps or all block interiors; no global rate or full minimum interface is proved.')


def logarithmic_cap_dispersion_audit(sequence, splits, fibonacci):
    def horizon(defect):
        depth, capacity = 1, 3
        while defect > capacity:
            depth += 1
            capacity *= 2
        return depth

    def constant(depth):
        return Fraction(1, 25 * 4 ** (depth - 1))

    def local_variance(order, gap, first_gap):
        index = fibonacci[order] - gap
        first = fibonacci[order - 1] - first_gap
        second = index - first
        numerator = fibonacci[order - 2] * second - fibonacci[order - 3] * first
        return Fraction(numerator ** 2, index ** 2 * first * second)

    geometric_transfer_checks = 0
    for order in range(22, 27):
        for gap in range(1, 49):
            index = fibonacci[order] - gap
            for first_gap in range(gap + 1):
                first = fibonacci[order - 1] - first_gap
                second = index - first
                variance = local_variance(order, gap, first_gap)
                for child, child_gap in ((first, first_gap), (second, gap - first_gap)):
                    for coefficient in (constant(1), constant(2), constant(3)):
                        transfer = variance + coefficient * Fraction(child_gap ** 2, index * child)
                        assert transfer >= coefficient * Fraction(gap ** 2, 4 * index ** 2)
                        geometric_transfer_checks += 1
    candidate_checks = 0
    low_cap_graph_checks = 0
    zero_child_options = 0
    retained_child_options = [0, 0]
    transfer_checks = 0
    contexts = set()

    @lru_cache(maxsize=None)
    def spine_minimum(order, gap, depth):
        nonlocal candidate_checks, low_cap_graph_checks, zero_child_options, transfer_checks
        index = fibonacci[order] - gap
        defect = fibonacci[order - 1] - sequence[index]
        assert defect <= 3 * 2 ** (depth - 1) and order >= 22 + 2 * (depth - 1)
        contexts.add((order, gap, depth))
        options = []
        if defect <= 3:
            frontiers = [higher_cap_width(order - 1, level) + level + 1 for level in range(4)]
            shifts = ([frontiers.index(gap), frontiers.index(gap) + 1] if gap in frontiers
                      else [higher_cap_shift(order, gap)])
            trajectory, transient, _ = full_orbit(sequence, index)
            assert {fibonacci[order - 1] - gap + shift for shift in shifts} == set(trajectory[transient:])
            low_cap_graph_checks += 1
            for shift in shifts:
                first_gap = gap - shift
                variance = local_variance(order, gap, first_gap)
                assert variance >= Fraction(gap ** 2, 25 * index ** 2)
                options.append((variance, first_gap, 0, 1))
        else:
            assert depth >= 2 and gap > higher_cap_width(order, 3)
            lower_gap = max(0, gap - fibonacci[order - 4])
            upper_gap = min(gap, fibonacci[order - 3])
            for first_gap in range(lower_gap, upper_gap + 1):
                first = fibonacci[order - 1] - first_gap
                second = index - first
                first_defect = fibonacci[order - 2] - sequence[first]
                second_defect = fibonacci[order - 3] - sequence[second]
                candidate_checks += 1
                if first_defect + second_defect != defect:
                    continue
                assert first_defect >= 0 and second_defect >= 0
                variance = local_variance(order, gap, first_gap)
                if first_defect == 0 or second_defect == 0:
                    assert variance >= Fraction(gap ** 2, 100 * index ** 2)
                    zero_child_options += 1
                    options.append((variance, first_gap, 0, 1))
                    continue
                children = ((first, first_gap, first_defect, order - 1),
                            (second, gap - first_gap, second_defect, order - 2))
                eligible = 0
                for side, (child, child_gap, child_defect, child_order) in enumerate(children):
                    if child_defect > 3 * 2 ** (depth - 2):
                        continue
                    eligible += 1
                    coefficient = constant(depth - 1)
                    transfer = variance + coefficient * Fraction(child_gap ** 2, index * child)
                    assert transfer >= constant(depth) * Fraction(gap ** 2, index ** 2)
                    transfer_checks += 1
                    child_result, _, _, child_height = spine_minimum(child_order, child_gap, depth - 1)
                    option = variance + Fraction(child, index) * child_result
                    assert option >= constant(depth) * Fraction(gap ** 2, index ** 2)
                    retained_child_options[side] += 1
                    options.append((option, first_gap, side + 1, child_height + 1))
                assert eligible >= 1
        assert options
        result = min(options)
        assert result[3] <= depth
        assert result[0] >= constant(depth) * Fraction(gap ** 2, index ** 2)
        return result

    @lru_cache(maxsize=None)
    def actual_variance(order, gap, depth):
        if depth == 0:
            return Fraction(0)
        index = fibonacci[order] - gap
        first = splits[index]
        second = index - first
        first_gap = fibonacci[order - 1] - first
        second_gap = fibonacci[order - 2] - second
        return (local_variance(order, gap, first_gap)
                + Fraction(first, index) * actual_variance(order - 1, first_gap, depth - 1)
                + Fraction(second, index) * actual_variance(order - 2, second_gap, depth - 1))

    roots = 0
    defect_counts = {}
    depth_rows = {}
    literal_rows = {}
    nonperiodic_choices = 0
    nonperiodic_witness = None
    for order in range(22, 31):
        width = min(24 * cap_gap_budget(order), fibonacci[order - 2])
        for gap in range(width + 1):
            index = fibonacci[order] - gap
            defect = fibonacci[order - 1] - sequence[index]
            depth = horizon(defect)
            if defect > 24 or order < 22 + 2 * (depth - 1):
                continue
            bound, first_gap, side, height = spine_minimum(order, gap, depth)
            actual = actual_variance(order, gap, depth)
            assert bound <= actual
            golden_defect = sequence[index] - g_closed(index)
            assert 0 <= golden_defect <= gap
            assert actual >= constant(depth) * Fraction(golden_defect ** 2, index ** 2)
            if order >= 28:
                assert actual_variance(order, gap, 4) >= bound
                assert bound >= Fraction(golden_defect ** 2, 1600 * index ** 2)
            roots += 1
            defect_counts[str(defect)] = defect_counts.get(str(defect), 0) + 1
            row = depth_rows.setdefault(str(depth), dict(roots=0, constant=str(constant(depth)),
                                                        minimum_gap_ratio=None, witness=None))
            row['roots'] += 1
            if gap:
                ratio = bound * Fraction(index ** 2, gap ** 2)
                if row['minimum_gap_ratio'] is None or ratio < Fraction(row['minimum_gap_ratio']):
                    row['minimum_gap_ratio'] = str(ratio)
                    row['witness'] = dict(order=order, gap=gap, index=index, cap_defect=defect,
                                          horizon=depth, minimizing_first_gap=first_gap,
                                          retained_child=side, spine_height=height,
                                          actual_split=splits[index], spine_variance=str(bound),
                                          actual_variance=str(actual))
            if defect > 3:
                point = fibonacci[order - 1] - first_gap
                start = point
                visited = set()
                while point not in visited:
                    visited.add(point)
                    point = index - sequence[point]
                if point != start:
                    nonperiodic_choices += 1
                    if nonperiodic_witness is None:
                        nonperiodic_witness = dict(order=order, gap=gap, index=index, cap_defect=defect,
                                                  minimizing_split=start, retained_child=side,
                                                  actual_split=splits[index])
                if str(depth) not in literal_rows:
                    literal_rows[str(depth)] = dict(order=order, gap=gap, index=index,
                                                    cap_defect=defect, horizon=depth, split=splits[index])
    literal_updates = 0
    for row in literal_rows.values():
        point = row['index'] - 1
        for step in range(sequence[row['index'] - 1]):
            point = row['index'] - sequence[point]
            literal_updates += 1
        assert point == row['split']
    return dict(capacity='3*2^(t-1)', constant='1/(25*4^(t-1))', order_threshold='22+2(t-1)',
                root_orders_inclusive=[22, 30], cap_bound=24, actual_roots=roots,
                root_cap_defect_counts=defect_counts, horizon_rows=depth_rows,
                spine_contexts=len(contexts), scalar_candidate_checks=candidate_checks,
                geometric_one_child_transfer_checks=geometric_transfer_checks,
                scalar_valid_one_child_transfer_checks=transfer_checks,
                zero_child_options=zero_child_options, retained_child_options=retained_child_options,
                arithmetic_low_cap_graph_checks=low_cap_graph_checks,
                nonperiodic_minimizing_high_cap_choices=nonperiodic_choices,
                nonperiodic_witness=nonperiodic_witness,
                literal_rows=list(literal_rows.values()), literal_updates=literal_updates,
                scope='The written one-child variance transfer and cap-halving induction give a logarithmic horizon, with a cap-dependent constant and order threshold. The minimum keeps only one eligible positive-cap child and discards all other descendant variance, while permitting every scalar-valid geometric high-cap split and finishing at the arithmetic cap0..3 basin kernel. It is compared with exact actual V_t at every qualifying cap<=24 root; inherited labels are preserved. Four generations suffice on cap<=24 at k>=28 with constant1/1600. This is not a uniform constant on unbounded caps, a global rate or a full minimum endpoint interface.')


def cap_budget_interface_audit(sequence, splits, fibonacci):
    arithmetic_fibonacci = fibonacci[:]
    while len(arithmetic_fibonacci) <= 1000:
        arithmetic_fibonacci.append(arithmetic_fibonacci[-1] + arithmetic_fibonacci[-2])
    for order in range(11, 1001):
        budget = cap_gap_budget(order)
        assert budget == cap_gap_budget(order - 1) + negative_plateau_width(order - 2)
        assert budget >= cap_gap_budget(order - 2) + negative_plateau_width(order - 1)
        assert budget >= 2 * negative_plateau_width(order - 1)
        assert 2 * cap_gap_budget(order + 1) <= 3 * budget
        if order >= 30:
            assert budget >= 10 * negative_plateau_width(order - 1)
            assert 10 * cap_gap_budget(order + 1) <= 11 * budget
    thresholds = {}
    for level in range(1, 65):
        order = 11
        while level * cap_gap_budget(order) > arithmetic_fibonacci[order - 4]:
            order += 1
        thresholds[str(level)] = order
        assert all(level * cap_gap_budget(current) <= arithmetic_fibonacci[current - 4]
                   for current in range(order, 1001))
    assert thresholds['4'] == 17
    dispersion_thresholds = {}
    for level in range(1, 65):
        order = 30
        while True:
            width = level * cap_gap_budget(order)
            if (arithmetic_fibonacci[order - 3] >= 4 * width ** 2
                    and arithmetic_fibonacci[order] - width >= width ** 3):
                break
            order += 1
        dispersion_thresholds[str(level)] = order
        for current in range(order, 1001):
            width = level * cap_gap_budget(current)
            assert arithmetic_fibonacci[current - 3] >= 4 * width ** 2
            assert arithmetic_fibonacci[current] - width >= width ** 3
    assert [dispersion_thresholds[str(level)] for level in range(1, 5)] == [39, 45, 49, 51]
    geometric_variance_checks = 0
    actual_cubic_phase_checks = 0
    maximum_cubic_gap = 0
    for order in range(21, 41):
        anchor, cap = arithmetic_fibonacci[order], arithmetic_fibonacci[order - 1]
        previous, lower = arithmetic_fibonacci[order - 2], arithmetic_fibonacci[order - 3]
        gap = 1
        while gap ** 3 <= anchor - gap:
            index = anchor - gap
            assert lower >= 4 * gap ** 2
            for shift in range(gap + 1):
                first, second = cap - gap + shift, previous - shift
                assert previous <= first <= cap and lower <= second <= previous
                norm = gap ** 2 - 3 * gap * shift + shift ** 2
                assert norm != 0
                numerator = (-1) ** (order - 1) + lower * gap - cap * shift
                assert 4 * gap ** 2 * numerator ** 2 >= lower ** 2
                assert 25 * gap ** 2 * numerator ** 2 >= first * second
                assert 25 * numerator ** 2 * index ** 2 >= gap ** 4 * first * second
                geometric_variance_checks += 1
            if order <= 30:
                trajectory, transient, period = full_orbit(sequence, index)
                defect = sequence[index] - g_closed(index)
                assert 0 <= defect <= gap
                for point in trajectory[transient:]:
                    complement = index - point
                    numerator = previous * complement - lower * point
                    assert 25 * numerator ** 2 * index ** 2 >= defect ** 4 * point * complement
                    actual_cubic_phase_checks += 1
            maximum_cubic_gap = max(maximum_cubic_gap, gap)
            gap += 1
    block_positions = 0
    conservation_checks = 0
    branch_counts = dict(both_positive=0, first_only=0, second_only=0, both_zero=0)
    local_rows = 0
    exterior_trace_points = 0
    maximum_entrance = None
    support_rows = []
    cycle_witness = None
    for order in range(9, 31):
        anchor, cap = fibonacci[order], fibonacci[order - 1]
        profile = [cap - sequence[anchor - gap] for gap in range(fibonacci[order - 2] + 1)]
        allowed = []
        for gap, defect in enumerate(profile):
            if defect:
                assert gap <= defect * cap_gap_budget(order)
            else:
                assert gap <= negative_plateau_width(order)
            block_positions += 1
            if order >= 11:
                index = anchor - gap
                split = splits[index]
                first_gap = cap - split
                second_gap = fibonacci[order - 2] - (index - split)
                first_defect = fibonacci[order - 2] - sequence[split]
                second_defect = fibonacci[order - 3] - sequence[index - split]
                assert first_gap + second_gap == gap
                assert first_defect + second_defect == defect
                assert 0 <= first_gap <= fibonacci[order - 3]
                assert 0 <= second_gap <= fibonacci[order - 4]
                assert first_defect >= 0 and second_defect >= 0
                branch = ('both_positive' if first_defect and second_defect
                          else 'first_only' if first_defect
                          else 'second_only' if second_defect else 'both_zero')
                branch_counts[branch] += 1
                conservation_checks += 1
            if defect <= 4:
                allowed.append(gap)
        if order >= 19:
            support_rows.append(dict(order=order, full_block_checked=True,
                                     first_width=next(gap - 1 for gap, defect in enumerate(profile) if defect > 4),
                                     maximum_gap=max(allowed),
                                     holes=[gap for gap in range(max(allowed) + 1) if profile[gap] > 4],
                                     bound=4 * cap_gap_budget(order)))
        if order < thresholds['4']:
            continue
        width = 4 * cap_gap_budget(order)
        previous = [fibonacci[order - 2] - sequence[cap - gap] for gap in range(width + 1)]
        lower = [fibonacci[order - 3] - sequence[fibonacci[order - 2] - gap]
                 for gap in range(width + 1)]
        for gap in allowed:
            if gap < 2:
                continue
            index = anchor - gap
            trajectory, transient, period = full_orbit(sequence, index)
            entrance = next(position for position, point in enumerate(trajectory)
                            if cap - gap <= point <= cap)
            start_gap = cap - trajectory[entrance]
            distance = interval_distance(index - 1, cap - gap, cap)
            pairs = capture_pair_budget(distance)
            assert entrance <= 2 * pairs
            next_defect = cap - sequence[index - 1]
            assert 0 <= next_defect <= 2 * (gap + 1) // 3 <= gap
            depth = cap - next_defect
            assert depth >= entrance
            selected_gap, local_transient, local_period = local_cap_endpoint(
                gap, start_gap, depth - entrance, previous)
            split = cap - selected_gap
            assert split == splits[index] and local_period == period
            assert previous[selected_gap] + lower[gap - selected_gap] == profile[gap]
            assert period <= gap + 1 <= width + 1
            first_point = fibonacci[order - 2] - gap + next_defect
            second_point = cap + fibonacci[order - 4] - gap + lower[gap - next_defect]
            assert trajectory[1] == first_point and trajectory[2] == second_point
            assert second_point >= cap
            local_rows += 1
            exterior_trace_points += entrance
            if maximum_entrance is None or entrance > maximum_entrance['clock']:
                maximum_entrance = dict(order=order, gap=gap, clock=entrance,
                                       pair_bound=2 * pairs, start_gap=start_gap)
            if order == 24 and gap == 83:
                cycle = sorted(trajectory[transient:])
                assert cycle == [28578, 28582, 28583] and period == 3
                values = [cap - sequence[point] - sequence[index - point] for point in cycle]
                assert values == [8, 9, 4]
                assert [index - sequence[point] for point in cycle] == [28582, 28583, 28578]
                assert depth == 28648 and split == 28583 and sequence[index] == 28653
                same_parity = []
                for clock in (0, 2, 4):
                    point = cycle[0]
                    for iteration in range(clock):
                        point = index - sequence[point]
                    same_parity.append(cap - sequence[point] - sequence[index - point])
                assert same_parity == [8, 4, 9]
                cycle_witness = dict(order=order, gap=gap, index=index, cycle=cycle,
                                     cap_readouts=values, actual_depth=depth, actual_split=split,
                                     actual_value=sequence[index], entrance_clock=entrance,
                                     entrance_gap=start_gap, local_transient=local_transient,
                                     unrestricted_readout_classes=3, unrestricted_fixed_width_bits=2,
                                     even_clock_readouts=same_parity,
                                     qualified_cap4_readout_classes=1)
    literal_rows = []
    literal_updates = 0
    for order, gap in ((19, 50), (19, 54), (20, 55), (20, 57), (24, 83)):
        index = fibonacci[order] - gap
        point = index - 1
        depth = sequence[index - 1]
        for iteration in range(depth):
            point = index - sequence[point]
        assert point == splits[index]
        literal_updates += depth
        literal_rows.append(dict(order=order, gap=gap, index=index, depth=depth,
                                 selected_split=point, value=sequence[index]))
    five_gaps = [0, 10, 20, 40, 54]
    first_defects, second_defects, shifts = [], [], []
    decoded_first_gaps = []
    parent_parameters, first_parameters, second_parameters = [], [], []
    symbolic_profile = [fibonacci[17] - sequence[fibonacci[18] - gap]
                        for gap in range(max(five_gaps) + 1)]
    for row, gap in enumerate(five_gaps):
        index = fibonacci[19] - gap
        split = splits[index]
        shifts.append(split - (fibonacci[18] - gap))
        first_defects.append(fibonacci[17] - sequence[split])
        second_defects.append(fibonacci[16] - sequence[index - split])
        if gap <= 1:
            selected_gap = gap
        else:
            trajectory, transient, period = full_orbit(sequence, index)
            entrance = next(position for position, point in enumerate(trajectory)
                            if fibonacci[18] - gap <= point <= fibonacci[18])
            decoded = symbolic_cap_selector(19, gap, fibonacci[18] - trajectory[entrance], entrance,
                                           fibonacci[18] - sequence[index - 1], symbolic_profile)
            selected_gap = decoded['selected_gap']
        assert selected_gap == fibonacci[18] - split
        decoded_first_gaps.append(selected_gap)
    for row, gap in enumerate(five_gaps):
        following = (row + 1) % 5
        defect = first_defects[row] + second_defects[row]
        index = fibonacci[19] - gap
        split = splits[index]
        assert split - fibonacci[17] == fibonacci[16] - gap + shifts[row]
        assert index - split - fibonacci[16] == fibonacci[15] - shifts[row]
        first_profile = sequence[split] - fibonacci[16]
        second_profile = sequence[index - split] - fibonacci[15]
        assert first_profile == fibonacci[15] - first_defects[row]
        assert second_profile == fibonacci[14] - second_defects[row]
        parent_parameter = fibonacci[18] - five_gaps[following] - defect
        first_parameter = (fibonacci[17] - five_gaps[following] + shifts[following]
                           - first_defects[row])
        second_parameter = fibonacci[16] - shifts[following] - second_defects[row]
        assert first_parameter == fibonacci[17] - decoded_first_gaps[following] - first_defects[row]
        assert second_parameter == (fibonacci[16] - five_gaps[following]
                                    + decoded_first_gaps[following] - second_defects[row])
        assert first_parameter + second_parameter == parent_parameter
        assert fibonacci[16] - five_gaps[following] + shifts[following] + first_profile == first_parameter
        assert fibonacci[15] - shifts[following] + second_profile == second_parameter
        parent_parameters.append(parent_parameter)
        first_parameters.append(first_parameter)
        second_parameters.append(second_parameter)
    assert first_defects[-1] == 8 and second_defects[-1] == 1
    return dict(budget_formula='P9=13; Pk=floor((k-2)^2/3)-3k+30 for k>=10',
                no_new_sequence_premise=True, arithmetic_orders_inclusive=[11, 1000],
                sufficient_local_thresholds=thresholds, full_block_orders_inclusive=[9, 30],
                sufficient_quartic_dispersion_thresholds=dispersion_thresholds,
                geometric_cubic_orders_inclusive=[21, 40],
                geometric_cubic_variance_checks=geometric_variance_checks,
                maximum_arithmetic_cubic_gap=maximum_cubic_gap,
                actual_cubic_basin_phase_orders_inclusive=[21, 30],
                actual_cubic_basin_phase_checks=actual_cubic_phase_checks,
                cubic_quartic_constant='1/25',
                block_positions=block_positions, actual_conservation_checks=conservation_checks,
                child_budget_branch_counts=branch_counts,
                actual_cap4_supports=support_rows, actual_local_selector_rows=local_rows,
                exterior_trace_points=exterior_trace_points, maximum_entrance=maximum_entrance,
                three_phase_witness=cycle_witness, literal_endpoint_rows=literal_rows,
                literal_selected_updates=literal_updates,
                five_row_witness=dict(order=19, gaps=five_gaps, shifts=shifts,
                                      first_cap_defects=first_defects, second_cap_defects=second_defects,
                                      parent_parameters=parent_parameters, first_parameters=first_parameters,
                                      second_parameters=second_parameters,
                                      decoded_first_gaps=decoded_first_gaps,
                                      parent_symbolic_gaps=[five_gaps[(row + 1) % 5] + first_defects[row] + second_defects[row]
                                                            for row in range(5)],
                                      first_symbolic_gaps=[decoded_first_gaps[(row + 1) % 5] + first_defects[row]
                                                           for row in range(5)],
                                      second_symbolic_gaps=[five_gaps[(row + 1) % 5] - decoded_first_gaps[(row + 1) % 5]
                                                            + second_defects[row] for row in range(5)]),
                modular_symbolic_selector=modular_selector_audit(sequence, splits, fibonacci),
                cap_adaptive_dispersion=cap_adaptive_dispersion_audit(sequence, splits, fibonacci),
                logarithmic_cap_dispersion=logarithmic_cap_dispersion_audit(sequence, splits, fibonacci),
                scope='General full-block cap-budget induction uses the proved zero plateau and actual two-child conservation, without a new finite sequence premise. Fixed-cap sublevels have polynomial gap enclosure and a conditional local-table/entrance decoder. The independent Diophantine proof gives phase-free quartic dispersion on cube-root collars, hence eventually on every fixed cap level; large arithmetic checks do not evaluate C. Finite level4 support holes are not an infinite support law. Tables, predecessor/exterior qualification, exact Fibonacci arithmetic and autonomous memory are separate costs; cap4 qualification already collapses the displayed scalar phase fiber. Global dispersion/convergence remain open.')


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
                higher_cap_closure=higher_cap_closure_audit(sequence, splits, fibonacci),
                bounded_cap_interface=cap_budget_interface_audit(sequence, splits, fibonacci),
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


def unit_first_spine_gap(initial_order, initial_gap, target_order):
    assert 19 <= target_order <= initial_order
    assert 0 <= initial_gap <= unit_defect_width(initial_order)
    if initial_gap <= negative_plateau_width(initial_order):
        return min(initial_gap, negative_plateau_width(target_order))
    return max(negative_plateau_width(target_order) + 1,
               min(initial_gap - initial_order + target_order,
                   unit_defect_width(target_order)))


def canonical_additive_carry_audit():
    legal_words = []
    for digits in product((0, 1), repeat=4):
        if any(first * second for first, second in zip(digits, digits[1:])):
            continue
        offset = sum(digit * weight for digit, weight in zip(digits, (1, 2, 3, 5)))
        legal_words.append((offset, digits))
    legal_words.sort()
    assert [offset for offset, digits in legal_words] == list(range(8))
    interpolated_tables = 0
    for values in product((0, 1), repeat=8):
        baseline = values[0]
        singleton = [values[offset] - baseline for offset in (1, 2, 3, 5)]
        interactions = [values[4] - values[1] - values[3] + baseline,
                        values[6] - values[1] - values[5] + baseline,
                        values[7] - values[2] - values[5] + baseline]
        coefficients = [baseline, *singleton, *interactions]
        for offset, digits in legal_words:
            unit, first, middle, last = digits
            features = (1, *digits, unit * middle, unit * last, first * last)
            assert sum(coefficient * feature for coefficient, feature
                       in zip(coefficients, features)) == values[offset]
        interpolated_tables += 1
    jump_cases = 0
    for initial_order in range(20, 181):
        for initial_gap in range(unit_defect_width(initial_order) + 1):
            gap = initial_gap
            for target_order in range(initial_order, 18, -1):
                assert gap == unit_first_spine_gap(initial_order, initial_gap, target_order)
                if target_order > 19:
                    gap -= unit_defect_shift(target_order, gap)
                jump_cases += 1
    fibonacci = fibonacci_values(1000)
    context_orders = range(8, 15)
    anchor_orders = [(3 * (fibonacci[order] - 3) + 1) // 2 for order in context_orders]
    while len(fibonacci) <= max(anchor_orders) + 1:
        fibonacci.append(fibonacci[-1] + fibonacci[-2])
    arithmetic_rows = []
    canonical_words = 0
    for context_order, anchor_order in zip(context_orders, anchor_orders):
        gap = fibonacci[context_order]
        context = fibonacci[anchor_order] - gap
        assert negative_plateau_width(anchor_order) == gap - 6
        assert negative_plateau_width(anchor_order - 1) == gap - 7 >= 14
        assert negative_plateau_width(anchor_order + 1) < gap <= unit_defect_width(anchor_order + 1)
        assert unit_defect_shift(anchor_order + 1, gap) == 1
        high = canonical_fibonacci_indices(context, fibonacci)
        assert min(high) >= 7
        for offset, digits in legal_words:
            indices = canonical_fibonacci_indices(context + offset, fibonacci)
            low = tuple(order for order in range(5, 1, -1) if digits[order - 2])
            assert indices == high + low
            assert unit_defect_shift(anchor_order, gap - offset) == int(offset < 7)
            unit, first, middle, last = digits
            assert unit * last + first * last == int(offset >= 6)
            canonical_words += 1
        exit_depth = 2 if gap % 2 else 3
        joint_offsets = [gap - unit_first_spine_gap(anchor_order, gap - 7, anchor_order - depth)
                         for depth in range(exit_depth + 1)]
        assert joint_offsets == [7] * exit_depth + [8]
        root = fibonacci[anchor_order + 1] - gap
        scalar = fibonacci[anchor_order] - 1
        defect = scalar - g_closed(root)
        split = fibonacci[anchor_order] - gap
        complement = fibonacci[anchor_order - 1]
        numerator = complement * root - fibonacci[anchor_order] * split
        assert 2 * numerator * numerator >= split * complement * defect * defect
        arithmetic_rows.append(dict(context_order=context_order, anchor_order=anchor_order,
                                    root_gap=gap, first_exit_depth=exit_depth,
                                    joint_offsets=joint_offsets, predicted_golden_defect=defect,
                                    scalar_valid_alternative_half_quadratic_bound=True))
    witness_order = anchor_orders[0]
    initial_gap = fibonacci[8]
    root = fibonacci[witness_order + 1] - initial_gap
    sequence, _, _, splits = generate(root)
    assert sequence == brent_generate(root)
    context = fibonacci[witness_order] - initial_gap
    cap = fibonacci[witness_order]
    assert sequence[root] == cap - 1 and splits[root] == context + 1
    literal_updates = 0
    for index in [root] + [context + offset for offset in range(8)]:
        endpoint = index - 1
        depth = sequence[index - 1]
        for iteration in range(depth):
            endpoint = index - sequence[endpoint]
        assert endpoint == splits[index]
        literal_updates += depth
    table_rows = []
    spine_rows = []
    for offset, digits in legal_words:
        index = context + offset
        complement = root - index
        readout = sequence[index] + sequence[complement]
        assert readout == cap - 1 + int(offset >= 6)
        assert splits[index] - (fibonacci[witness_order - 1] - initial_gap) == min(offset + 1, 7)
        table_rows.append(dict(offset=offset, digits=''.join(map(str, digits)), index=index,
                               complement=complement, readout=readout, selected=splits[index]))
        inherited_defect = int(offset < 6)
        current = index
        for order in range(witness_order, 18, -1):
            gap = unit_first_spine_gap(witness_order, initial_gap - offset, order)
            assert current == fibonacci[order] - gap
            assert fibonacci[order - 1] - sequence[current] == inherited_defect
            spine_rows.append(dict(root_offset=offset, anchor_order=order, index=current,
                                   gap=gap, cap_defect=inherited_defect))
            if order > 19:
                next_gap = unit_first_spine_gap(witness_order, initial_gap - offset, order - 1)
                delta = gap - next_gap
                assert splits[current] == fibonacci[order - 1] - next_gap
                assert current - splits[current] == fibonacci[order - 2] - delta
                assert sequence[current - splits[current]] == fibonacci[order - 3]
                current = splits[current]
    joint_chain = [row['index'] for row in spine_rows if row['root_offset'] == 7][:3]
    assert joint_chain == [196404, 121379, 75012]
    seam_base = fibonacci[25] - fibonacci[8]
    assert min(canonical_fibonacci_indices(seam_base, fibonacci)) == 7
    assert min(canonical_fibonacci_indices(seam_base + 8, fibonacci)) == 8
    defect = sequence[root] - g_closed(root)
    numerator = fibonacci[witness_order - 1] * root - cap * context
    quadratic_ratio = Fraction(numerator * numerator,
                               context * fibonacci[witness_order - 1] * defect * defect)
    assert quadratic_ratio == Fraction(155142242161, 214570989189)
    offsets = {0, 2, 3, 5, 7}
    assert offsets | {min(offset + 1, 7) for offset in offsets} == set(range(8))
    return dict(legal_unit_extended_words=[''.join(map(str, digits)) for offset, digits in legal_words],
                exact_boolean_tables_reconstructed=interpolated_tables,
                arithmetic_jump_orders_inclusive=[20, 180], arithmetic_jump_cases=jump_cases,
                arithmetic_context_orders_inclusive=[8, 14], canonical_words_checked=canonical_words,
                arithmetic_context_rows=arithmetic_rows,
                actual_prefix_limit=root, full_orbit_and_brent_agree=True,
                prefix_sha256=hashlib.sha256(','.join(map(str, sequence[1:])).encode('ascii')).hexdigest(),
                parent=dict(index=root, value=sequence[root], selected=splits[root], depth=sequence[root - 1]),
                actual_additive_table=table_rows, literal_selected_endpoint_updates=literal_updates,
                actual_first_spine_rows=spine_rows, joint_seam_chain=joint_chain,
                scalar_valid_dispersion=dict(inherited_order=witness_order, split=context,
                                              complement=fibonacci[witness_order - 1],
                                              golden_defect=defect, quadratic_ratio=str(quadratic_ratio),
                                              proved_uniform_constant='1/2 on this canonical family'),
                direct_decoder='Q=0: min(v,L_s); Q=1: max(L_s+1,min(v-K+s,R_s)), 19<=s<=K',
                scope='Infinite additive-window qualification, unit completion and direct actual first-spine formulas follow from the proved unit-sublevel theorem. Five labels plus one-edge images need exactly eight offset labels, not stationary recursive closure or an extra memory-bit lower bound. Higher contexts change by canonical carry. Supplied order/gap/depth derives all residual selector/carry labels; wide-block minimum and uniform dispersion remain open.')


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
                canonical_additive_carry=canonical_additive_carry_audit(),
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

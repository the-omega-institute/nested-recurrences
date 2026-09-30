"""Corroborate the proved Fibonacci collar consequences by exact computation."""

import bisect
import hashlib
import json
from pathlib import Path

from conway_explore import brent_generate, full_orbit, generate, literal_generate
from golden_check import fibonacci_values


def all_cycles(sequence, index):
    completed = bytearray(index)
    cycles = []
    for start in range(1, index):
        if completed[start]:
            continue
        positions = {}
        path = []
        point = start
        while not completed[point] and point not in positions:
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


def main():
    if not __debug__:
        raise SystemExit('Run without -O; assertions perform the checks.')
    limit = 131071
    sequence, preperiods, periods, splits = generate(limit)
    assert sequence == brent_generate(limit)
    literal, updates = literal_generate(4096)
    assert sequence[:len(literal)] == literal
    fibonacci = fibonacci_values(limit + 2)
    selected_cycle_points = 0
    for index in range(8, limit + 1):
        order = bisect.bisect_right(fibonacci, index) - 1
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
            actual_cycles = all_cycles(sequence, index + offset)
            lower = anchor + min(0, offset)
            upper = anchor + max(0, offset)
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
    report = dict(
        status='Finite corroboration of the written collar theorems; universal proof in fibonacci-collars.md depends only on golden-proof.md.',
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
        full_ratio_convergence='open; sublinear-neighborhood convergence is proved separately',
    )
    print(json.dumps(report, indent=2) + '\n', end='')


if __name__ == '__main__':
    main()

"""Exact all-start period-five closure certificate in the first arch block."""

from collections import Counter
import hashlib
import json
from pathlib import Path

from conway_explore import brent_generate, full_orbit, generate


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
        if point in positions:
            cycles.append(tuple(path[positions[point]:]))
        for point in path:
            completed[point] = 1
    assert all(completed[1:])
    return sorted(cycles)


def canonical_cycle(cycle):
    rotations = [cycle[index:] + cycle[:index] for index in range(len(cycle))]
    return min(rotations)


def main():
    if not __debug__:
        raise SystemExit("Run without -O; assertions perform the checks.")
    limit = 232
    first_anchor = 144
    next_anchor = 233
    anchor = 89
    lower_anchor = 55
    sequence, _, _, splits = generate(limit)
    assert sequence == brent_generate(limit)
    histogram = Counter()
    graph_count = 0
    vertex_count = 0
    period_five = []
    for index in range(first_anchor, next_anchor):
        offset = index - first_anchor
        cycles = all_cycles(sequence, index)
        graph_count += 1
        vertex_count += index - 1
        for cycle in cycles:
            period = len(cycle)
            histogram[period] += 1
            assert all(anchor <= point <= anchor + offset for point in cycle)
            assert period <= offset + 1
            if period == 5:
                normalized = canonical_cycle(tuple(point - anchor for point in cycle))
                defects = tuple(sequence[anchor + point] - lower_anchor - point
                                for point in normalized)
                child_splits = tuple(splits[anchor + point] - lower_anchor
                                     for point in normalized)
                child_offsets = tuple(point - split for point, split in zip(normalized, child_splits))
                period_five.append(dict(
                    index=index,
                    block_offset=offset,
                    cycle_offsets=list(normalized),
                    defects=list(defects),
                    child_splits=list(child_splits),
                    child_offsets=list(child_offsets),
                ))
    assert graph_count == 89
    assert vertex_count == sum(range(first_anchor - 1, next_anchor - 1))
    assert dict(sorted(histogram.items())) == {1: 55, 2: 111, 3: 5, 4: 5, 5: 1}
    assert [row["index"] for row in period_five] == [196]
    assert period_five[0] == dict(
        index=196,
        block_offset=52,
        cycle_offsets=[26, 31, 27, 28, 29],
        defects=[-5, -6, -3, -5, -3],
        child_splits=[10, 20, 16, 12, 18],
        child_offsets=[16, 11, 11, 16, 11],
    )
    trajectory, preperiod, period = full_orbit(sequence, 196)
    depth = sequence[195]
    assert (preperiod, period, depth, (depth - preperiod) % period) == (8, 5, 131, 3)
    assert sequence[196] == 134 and splits[196] == 118
    report = dict(
        status="Exact finite all-start closure certificate; no global finite alphabet claimed.",
        source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        evaluator_source_sha256=hashlib.sha256(Path(__file__).with_name("conway_explore.py").read_bytes()).hexdigest(),
        block=[first_anchor, next_anchor - 1],
        fibonacci_anchor=anchor,
        all_start_graphs_checked=graph_count,
        all_start_vertices_checked=vertex_count,
        cycle_histogram=dict(sorted(histogram.items())),
        period_five_payloads=period_five,
        selected_n_196=dict(
            value=sequence[196],
            selected_split=splits[196],
            depth=depth,
            preperiod=preperiod,
            period=period,
            selected_phase=(depth - preperiod) % period,
            cycle=list(trajectory[preperiod:preperiod + period]),
        ),
    )
    print(json.dumps(report, indent=2) + "\n", end="")


if __name__ == "__main__":
    main()

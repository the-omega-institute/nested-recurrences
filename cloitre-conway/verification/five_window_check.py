"""Exact all-start five-window certificates in the first three arch blocks."""

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


def fibonacci_values(limit):
    values = [0, 1]
    while values[-1] <= limit:
        values.append(values[-1] + values[-2])
    return values


def main():
    if not __debug__:
        raise SystemExit("Run without -O; assertions perform the checks.")
    limit = 609
    fibonacci = fibonacci_values(limit + 1)
    sequence, _, _, splits = generate(limit)
    assert sequence == brent_generate(limit)
    expected_histograms = {
        12: {1: 55, 2: 111, 3: 5, 4: 5, 5: 1},
        13: {1: 89, 2: 203, 3: 12, 4: 6, 5: 5, 6: 1},
        14: {1: 144, 2: 359, 3: 19, 4: 24, 5: 7, 6: 5, 7: 1},
    }
    expected_period_five = {
        12: [196],
        13: [304, 307, 310, 313, 316],
        14: [431, 500, 507, 513, 523, 535, 550],
    }
    blocks = []
    for order in (12, 13, 14):
        first_anchor = fibonacci[order]
        next_anchor = fibonacci[order + 1]
        anchor = fibonacci[order - 1]
        lower_anchor = fibonacci[order - 2]
        child_anchor = fibonacci[order - 3]
        child_lower_anchor = fibonacci[order - 4]
        histogram = Counter()
        graph_count = 0
        vertex_count = 0
        period_five = []
        compressed_closure_count = 0
        child_split_ambiguity_count = 0
        max_child_split_candidates = 0
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
                    positive_defects = tuple(-defect for defect in defects)
                    reconstructed = [normalized[0]]
                    for defect in positive_defects[:4]:
                        reconstructed.append(offset - reconstructed[-1] + defect)
                    assert tuple(reconstructed) == normalized
                    assert (2 * normalized[0] == offset + positive_defects[0]
                            - positive_defects[1] + positive_defects[2]
                            - positive_defects[3] + positive_defects[4])
                    compressed_closure_count += 1
                    candidate_sets = []
                    for point, parent_defect in zip(normalized, defects):
                        candidates = []
                        for candidate in range(point + 1):
                            complement = point - candidate
                            first = sequence[lower_anchor + candidate] - child_anchor - max(0, candidate)
                            second = (sequence[child_anchor + complement] - child_lower_anchor
                                      - max(0, complement))
                            if first + second == parent_defect:
                                candidates.append(candidate)
                        assert candidates
                        candidate_sets.append(tuple(candidates))
                        max_child_split_candidates = max(max_child_split_candidates, len(candidates))
                        if len(candidates) > 1:
                            child_split_ambiguity_count += 1
                    child_splits = tuple(splits[anchor + point] - lower_anchor
                                         for point in normalized)
                    assert all(child_split in candidates
                               for child_split, candidates in zip(child_splits, candidate_sets))
                    child_offsets = tuple(point - split for point, split in
                                          zip(normalized, child_splits))
                    period_five.append(dict(
                        index=index,
                        block_offset=offset,
                        cycle_offsets=list(normalized),
                        defects=list(defects),
                        child_splits=list(child_splits),
                        child_offsets=list(child_offsets),
                    ))
        assert graph_count == next_anchor - first_anchor
        assert dict(sorted(histogram.items())) == expected_histograms[order]
        assert [row["index"] for row in period_five] == expected_period_five[order]
        blocks.append(dict(
            order=order,
            index_range=[first_anchor, next_anchor - 1],
            fibonacci_anchor=anchor,
            all_start_graphs_checked=graph_count,
            all_start_vertices_checked=vertex_count,
            compressed_closure_checked=compressed_closure_count,
            child_split_ambiguity_checked=child_split_ambiguity_count,
            max_child_split_candidates=max_child_split_candidates,
            cycle_histogram=dict(sorted(histogram.items())),
            period_five_payloads=period_five,
        ))
    trajectory, preperiod, period = full_orbit(sequence, 196)
    depth = sequence[195]
    assert (preperiod, period, depth, (depth - preperiod) % period) == (8, 5, 131, 3)
    assert sequence[196] == 134 and splits[196] == 118
    report = dict(
        status="Exact finite all-start closure certificates; no global finite alphabet claimed.",
        source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        evaluator_source_sha256=hashlib.sha256(Path(__file__).with_name("conway_explore.py").read_bytes()).hexdigest(),
        compressed_closure_checked=sum(block["compressed_closure_checked"] for block in blocks),
        child_split_ambiguity_checked=sum(block["child_split_ambiguity_checked"] for block in blocks),
        blocks=blocks,
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

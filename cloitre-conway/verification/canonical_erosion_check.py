"""Check canonical contact gates and clock-residue bounds using full orbits."""

import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from conway_explore import full_orbit, generate


def main():
    limit = 131072
    values, preperiods, periods, selected = generate(limit)
    fibonacci = [0, 1]
    while fibonacci[-1] <= limit:
        fibonacci.append(sum(fibonacci[-2:]))
    gates_checked = 0
    aligned_pairs = 0
    positive_pairs = 0
    long_cycles_checked = 0
    marked_cycles_checked = 0
    noninitial_gates = 0
    examples = []
    for level in range(10, len(fibonacci) - 1):
        anchor = fibonacci[level]
        if anchor > limit:
            break
        first_child = fibonacci[level - 1]
        second_child = fibonacci[level - 2]
        third_child = fibonacci[level - 3]
        source = [values[first_child + offset] - second_child
                  for offset in range(second_child + 1)]
        suffix_minimum = source[:]
        for offset in range(second_child - 1, -1, -1):
            suffix_minimum[offset] = min(source[offset], suffix_minimum[offset + 1])
        gates = set()
        first_source_defect = next((offset for offset, value in enumerate(source)
                                    if value != offset), second_child + 1)
        for offset in range(1, min(third_child, limit - anchor) + 1):
            if source[offset] != offset or suffix_minimum[offset] < offset:
                continue
            gates.add(offset)
            gates_checked += 1
            noninitial_gates += offset > first_source_defect
            parent = anchor + offset
            depth = values[parent - 1]
            expected_split = first_child + (0 if depth % 2 else offset)
            lower_defect = third_child + offset - values[second_child + offset]
            defect = first_child + offset - values[parent]
            assert selected[parent] == expected_split
            assert periods[parent] == 2
            assert defect == (lower_defect if depth % 2 else 0)
            assert parent - selected[parent] - values[selected[parent]] == (offset if depth % 2 else -offset)
            for later in range(offset + 1, min(2 * offset - 2, second_child - 1) + 1):
                assert source[later] >= offset
            if parent in (58, 59, 62):
                examples.append(dict(n=parent, depth=depth, g=selected[parent], C=values[parent], E=defect))
        for offset in sorted(gates):
            if offset + 1 not in gates or (first_child + offset) % 2 != 1:
                continue
            aligned_pairs += 1
            lower_defects = [third_child + position - values[second_child + position]
                             for position in (offset, offset + 1)]
            parent_defects = [first_child + position - values[anchor + position]
                              for position in (offset, offset + 1)]
            assert sum(parent_defects) >= min(lower_defects)
            assert any(parent == lower for parent, lower in zip(parent_defects, lower_defects))
            positive_pairs += min(lower_defects) > 0
        first_frontier = max(offset for offset in range(second_child + 1)
                             if source[offset] == offset)
        second_frontier = max(offset for offset in range(third_child + 1)
                              if values[second_child + offset] == third_child + offset)
        for offset in range(1, min(first_child - 1, limit - anchor) + 1):
            parent = anchor + offset
            if periods[parent] <= 2:
                continue
            long_cycles_checked += 1
            trajectory, preperiod, period = full_orbit(values, parent)
            assert preperiod == preperiods[parent] and period == periods[parent]
            cycle = [point - first_child for point in trajectory[preperiod:]]
            marks = [0 <= point <= second_child and 0 <= offset - point <= third_child
                     and values[first_child + point] == second_child + point
                     and values[second_child + offset - point] == third_child + offset - point
                     for point in cycle]
            canonical_rank = (values[parent - 1] - preperiod) % period
            assert marks[canonical_rank] == (values[parent] == first_child + offset)
            if offset <= 2 * second_frontier or not any(marks):
                continue
            marked_cycles_checked += 1
            slack = first_frontier + second_frontier - offset
            count = sum(marks)
            assert slack >= 0 and count <= slack + 1
            assert (2 * slack + 3) * count <= (slack + 1) * period
            assert period >= 2 * count + 1
            for rank in range(period):
                assert not (marks[rank] and marks[(rank + 1) % period])
                if marks[rank] and marks[(rank + 2) % period]:
                    assert cycle[(rank + 2) % period] > cycle[rank]
    assert values[42] - 21 == 8 and values[43] - 21 == 7
    assert selected[63] == 35
    print(json.dumps(dict(limit=limit, evaluator='full visited-state orbits',
                          gates_checked=gates_checked,
                          gates_after_first_source_defect=noninitial_gates,
                          aligned_pairs_checked=aligned_pairs,
                          pairs_with_positive_lower_defects=positive_pairs,
                          long_cycles_checked=long_cycles_checked,
                          marked_long_cycles_in_separation_range=marked_cycles_checked,
                          gate_counterexample=dict(n=63, t=8, source_contact=True,
                                                   later_offset=9, later_source_value=7, g=35),
                          examples=examples), indent=2))


if __name__ == '__main__':
    main()

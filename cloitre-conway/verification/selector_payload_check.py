"""Audit ordinal encodings of the five Fibonacci child-split selectors."""

from collections import Counter
import json
import math
import sys

from conway_explore import generate
from five_window_check import all_cycles, canonical_cycle, fibonacci_values


def candidate_sets(sequence, anchor, lower_anchor, child_anchor,
                   child_lower_anchor, offsets):
    result = []
    for offset in offsets:
        parent_defect = sequence[anchor + offset] - lower_anchor - offset
        candidates = []
        for split in range(offset + 1):
            complement = offset - split
            first = (sequence[lower_anchor + split] - child_anchor
                     - max(0, split))
            second = (sequence[child_anchor + complement] - child_lower_anchor
                      - max(0, complement))
            if first + second == parent_defect:
                candidates.append(split)
        assert candidates
        result.append(tuple(candidates))
    return result


def is_contiguous(values):
    return list(values) == list(range(values[0], values[-1] + 1))


def main():
    limit = 609
    fibonacci = fibonacci_values(limit + 1)
    sequence, _, _, selected_splits = generate(limit)
    payloads = []
    candidate_lengths = Counter()
    ambiguous_rows = 0
    noncontiguous_sets = 0
    parent_rows = 0
    reconstructed_selector_positions = 0
    reconstructed_parent_transitions = 0
    for order in (12, 13, 14):
        anchor = fibonacci[order - 1]
        lower_anchor = fibonacci[order - 2]
        child_anchor = fibonacci[order - 3]
        child_lower_anchor = fibonacci[order - 4]
        for index in range(fibonacci[order], fibonacci[order + 1]):
            for cycle in all_cycles(sequence, index):
                if len(cycle) != 5:
                    continue
                offsets = canonical_cycle(tuple(point - anchor for point in cycle))
                sets = candidate_sets(sequence, anchor, lower_anchor,
                                      child_anchor, child_lower_anchor, offsets)
                parent_rows += len(sets)
                lengths = [len(values) for values in sets]
                candidate_lengths.update(lengths)
                ambiguous_rows += sum(length > 1 for length in lengths)
                noncontiguous_sets += sum(not is_contiguous(values) for values in sets)
                selected = [selected_splits[anchor + offset] - lower_anchor
                            for offset in offsets]
                ranks = [values.index(split) for values, split in zip(sets, selected)]
                recovered = [values[rank] for values, rank in zip(sets, ranks)]
                assert recovered == selected
                for position, (offset, split) in enumerate(zip(offsets, recovered)):
                    complement = offset - split
                    first = (sequence[lower_anchor + split] - child_anchor
                             - max(0, split))
                    second = (sequence[child_anchor + complement] - child_lower_anchor
                              - max(0, complement))
                    parent_defect = sequence[anchor + offset] - lower_anchor - offset
                    assert first + second == parent_defect
                    next_offset = offsets[(position + 1) % 5]
                    defect = -parent_defect
                    assert next_offset == (index - fibonacci[order]) - offset + defect
                    reconstructed_selector_positions += 1
                    reconstructed_parent_transitions += 1
                payloads.append({
                    "index": index,
                    "candidate_lengths": lengths,
                    "selected_ranks": ranks,
                    "cartesian_candidate_count": math.prod(lengths),
                })
    largest = max(payloads, key=lambda row: row["cartesian_candidate_count"])
    assert len(payloads) == 13
    assert parent_rows == 65
    assert ambiguous_rows == 57
    assert max(candidate_lengths) == 29
    assert noncontiguous_sets == 56
    assert reconstructed_selector_positions == 65
    assert reconstructed_parent_transitions == 65
    assert largest["index"] == 431
    assert largest["cartesian_candidate_count"] == 45696
    print(json.dumps({
        "status": "passed",
        "scope": "Exact public three-block selector audit; no independence of Cartesian choices is claimed.",
        "period_five_payloads": len(payloads),
        "parent_rows": parent_rows,
        "ambiguous_parent_rows": ambiguous_rows,
        "candidate_length_histogram": dict(sorted(candidate_lengths.items())),
        "noncontiguous_candidate_sets": noncontiguous_sets,
        "reconstructed_selector_positions": reconstructed_selector_positions,
        "reconstructed_parent_transitions": reconstructed_parent_transitions,
        "max_candidate_count": max(candidate_lengths),
        "largest_cartesian_candidate_space": largest,
        "ordinal_encoding": {
            "semantic_payload": "five selector ordinals relative to lower-profile candidate sets",
            "numeric_split_recovered": "candidate_set[ordinal]",
            "fixed_width_bits_for_largest_cartesian_space": math.ceil(math.log2(largest["cartesian_candidate_count"])),
            "qualification": "The bit count is an encoding capacity before any cross-row relation; the semantic necessity is five selector positions."
        },
        "payloads": payloads,
    }, indent=2))


if __name__ == "__main__":
    main()

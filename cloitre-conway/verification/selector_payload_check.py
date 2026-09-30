"""Audit ordinal encodings of the five Fibonacci child-split selectors."""

from collections import Counter
from fractions import Fraction
import json
from itertools import product
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


def affine_rank(matrix):
    rows = [[Fraction(value) for value in row] for row in matrix]
    pivot = 0
    for column in range(len(rows[0])):
        candidate = next((row for row in range(pivot, len(rows))
                          if rows[row][column]), None)
        if candidate is None:
            continue
        rows[pivot], rows[candidate] = rows[candidate], rows[pivot]
        factor = rows[pivot][column]
        rows[pivot] = [value / factor for value in rows[pivot]]
        for row in range(len(rows)):
            if row == pivot or not rows[row][column]:
                continue
            factor = rows[row][column]
            rows[row] = [left - factor * right
                         for left, right in zip(rows[row], rows[pivot])]
        pivot += 1
    return pivot


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
    complementary_lower_map_rows = 0
    row_local_combinations_checked = 0
    affine_parent_features = []
    affine_split_features = []
    affine_alpha_features = []
    affine_beta_features = []
    affine_both_parameter_features = []
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
                for combination in product(*sets):
                    for offset, split in zip(offsets, combination):
                        complement = offset - split
                        first = (sequence[lower_anchor + split] - child_anchor
                                 - max(0, split))
                        second = (sequence[child_anchor + complement] - child_lower_anchor
                                  - max(0, complement))
                        parent_defect = sequence[anchor + offset] - lower_anchor - offset
                        assert first + second == parent_defect
                    row_local_combinations_checked += 1
                selected = [selected_splits[anchor + offset] - lower_anchor
                            for offset in offsets]
                ranks = [values.index(split) for values, split in zip(sets, selected)]
                recovered = [values[rank] for values, rank in zip(sets, ranks)]
                assert recovered == selected
                parent_features = [index - fibonacci[order],
                                   *offsets,
                                   *[-defect for defect in
                                     [sequence[anchor + offset]
                                      - lower_anchor - offset
                                      for offset in offsets]],
                                   1]
                alpha_values = []
                beta_values = []
                for position, (offset, split) in enumerate(zip(offsets, recovered)):
                    complement = offset - split
                    next_offset = offsets[(position + 1) % 5]
                    next_split = recovered[(position + 1) % 5]
                    next_complement = next_offset - next_split
                    alpha = (next_split
                             + sequence[lower_anchor + split] - child_anchor)
                    beta = (next_complement
                            + sequence[child_anchor + complement]
                            - child_lower_anchor)
                    parent_scale = index - fibonacci[order]
                    assert alpha + beta == parent_scale
                    complementary_lower_map_rows += 1
                    alpha_values.append(alpha)
                    beta_values.append(beta)
                    first = (sequence[lower_anchor + split] - child_anchor
                             - max(0, split))
                    second = (sequence[child_anchor + complement] - child_lower_anchor
                              - max(0, complement))
                    parent_defect = sequence[anchor + offset] - lower_anchor - offset
                    assert first + second == parent_defect
                    defect = -parent_defect
                    assert next_offset == (index - fibonacci[order]) - offset + defect
                    reconstructed_selector_positions += 1
                    reconstructed_parent_transitions += 1
                affine_parent_features.append(parent_features)
                affine_split_features.append([*parent_features[:-1], *recovered, 1])
                affine_alpha_features.append([*parent_features[:-1], *alpha_values, 1])
                affine_beta_features.append([*parent_features[:-1], *beta_values, 1])
                affine_both_parameter_features.append(
                    [*parent_features[:-1], *alpha_values, *beta_values, 1])
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
    assert complementary_lower_map_rows == 65
    assert row_local_combinations_checked == 69064
    parent_rank = affine_rank(affine_parent_features)
    split_rank = affine_rank(affine_split_features)
    alpha_rank = affine_rank(affine_alpha_features)
    beta_rank = affine_rank(affine_beta_features)
    both_parameter_rank = affine_rank(affine_both_parameter_features)
    assert (parent_rank, split_rank, alpha_rank, beta_rank,
            both_parameter_rank) == (7, 12, 12, 12, 12)
    assert largest["index"] == 431
    assert largest["cartesian_candidate_count"] == 45696
    print(json.dumps({
        "status": "passed",
        "scope": "Exact public three-block selector audit; row-local Cartesian independence is checked, while lower-window closure constraints remain separate.",
        "period_five_payloads": len(payloads),
        "parent_rows": parent_rows,
        "ambiguous_parent_rows": ambiguous_rows,
        "candidate_length_histogram": dict(sorted(candidate_lengths.items())),
        "noncontiguous_candidate_sets": noncontiguous_sets,
        "reconstructed_selector_positions": reconstructed_selector_positions,
        "reconstructed_parent_transitions": reconstructed_parent_transitions,
        "complementary_lower_map_rows": complementary_lower_map_rows,
        "complementary_lower_map_identity": {
            "formula": "(r_(i+1) + P_(k-2)(r_i)) + (q_(i+1) + P_(k-3)(q_i)) = t",
            "scope": "all 65 public parent rows; q_i = u_i - r_i and t = n - F_(k-1)",
            "interpretation": "The two lower-map parameters are exact complements at the parent scale; this is not a lower five-cycle closure theorem."
        },
        "affine_parameter_rank": {
            "payload_rows": len(payloads),
            "parent_features": "(t, five offsets, five nonnegative defects, 1)",
            "parent_rank": parent_rank,
            "child_split_rank": split_rank,
            "alpha_rank": alpha_rank,
            "beta_rank": beta_rank,
            "alpha_beta_rank": both_parameter_rank,
            "rank_increment_for_each_parameterization": split_rank - parent_rank,
            "qualification": "Finite exact diagnostic on the 13 public payloads; it shows that the complement identity does not reduce the five affine directions, but is not a global lower bound."
        },
        "row_local_combinations_checked": row_local_combinations_checked,
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

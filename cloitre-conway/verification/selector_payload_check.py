"""Audit ordinal encodings of the five Fibonacci child-split selectors."""

from collections import Counter
from fractions import Fraction
import json
from itertools import product
import math
import sys

from conway_explore import brent_generate, full_orbit, generate
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


def seed_fiber(sets, profile, alpha):
    result = []
    for seed in sets[0]:
        word = [seed]
        for position, parameter in enumerate(alpha):
            next_split = parameter - profile[word[-1]]
            if next_split not in sets[(position + 1) % len(sets)]:
                break
            word.append(next_split)
        if len(word) == len(sets) + 1 and word[-1] == seed:
            result.append(tuple(word[:-1]))
    return result


def defect_seed_interval(alpha, defects):
    if len(alpha) != len(defects) or len(alpha) % 2 != 1:
        raise ValueError("The defect seed interval requires an odd window.")
    assert all(defect >= 0 for defect in defects)
    alternating_alpha = sum((-1) ** position * parameter
                            for position, parameter in enumerate(alpha))
    lower = (alternating_alpha - sum(defects[1::2]) + 1) // 2
    upper = (alternating_alpha + sum(defects[::2])) // 2
    return lower, upper


def decode_defect_residue(sets, profile, alpha, defects, residue):
    lower, upper = defect_seed_interval(alpha, defects)
    modulus = sum(defects) // 2 + 1
    assert 0 <= residue < modulus
    seed = lower + (residue - lower) % modulus
    if seed > upper or seed not in sets[0]:
        return None
    word = [seed]
    for position, parameter in enumerate(alpha):
        next_split = parameter - profile[word[-1]]
        if next_split not in sets[(position + 1) % len(sets)]:
            return None
        word.append(next_split)
    return tuple(word[:-1]) if word[-1] == seed else None


def defect_monotone_cover(values, profile, defect):
    parts = {}
    for split in values:
        child_defect = split - profile[split]
        assert 0 <= child_defect <= defect
        parts.setdefault(child_defect // 2, []).append(split)
    assert len(parts) <= defect // 2 + 1
    for part in parts.values():
        assert all(profile[first] <= profile[second]
                   for first, second in zip(part, part[1:]))
    return tuple(tuple(part) for part in parts.values())


def periodic_profile_candidates(values, profile, scale):
    retained = []
    for seed in values:
        point = seed
        visited = set()
        while point not in visited:
            assert 0 <= point <= scale
            visited.add(point)
            point = scale - profile[point]
        if point == seed:
            retained.append(seed)
    return tuple(retained)


def abstract_periodic_collision():
    scale = 100
    offsets = (60, 66, 72, 78, 84)
    first = (35, 43, 55, 65, 50)
    second = tuple(split + 1 for split in first)
    defects = tuple(offset + offsets[(position + 1) % 5] - scale
                    for position, offset in enumerate(offsets))
    parent_profile = {point: point for point in range(scale + 1)}
    for offset, defect in zip(offsets, defects):
        parent_profile[offset] = offset - defect
    assert len(set(offsets)) == 5
    assert all(0 <= value <= point for point, value in parent_profile.items())
    assert all(scale - parent_profile[offset] == offsets[(position + 1) % 5]
               for position, offset in enumerate(offsets))
    profile = {split: split for split in range(scale + 1)}
    complement_profile = dict(profile)
    for offset, defect, split in zip(offsets, defects, first):
        complement = offset - split
        profile[split] = complement
        profile[split + 1] = complement - 1
        complement_profile[complement] = split - defect
        complement_profile[complement - 1] = split + 1 - defect
    assert all(0 <= value <= split for split, value in profile.items())
    assert all(0 <= value <= split for split, value in complement_profile.items())
    sets = [tuple(split for split in range(offset + 1)
                  if profile[split] + complement_profile[offset - split] == offset - defect)
            for offset, defect in zip(offsets, defects)]
    periodic_sets = [periodic_profile_candidates(values, profile, offset)
                     for values, offset in zip(sets, offsets)]
    alpha = tuple(first[(position + 1) % 5] + profile[first[position]]
                  for position in range(5))
    fiber = seed_fiber(periodic_sets, profile, alpha)
    assert first in fiber and second in fiber
    assert all(offset - profile[split] == split
               for word in (first, second) for offset, split in zip(offsets, word))
    return {"scale": scale, "parent_offsets": list(offsets), "parent_defects": list(defects),
            "alpha": list(alpha), "two_periodic_words": [list(first), list(second)],
            "complete_periodic_fiber": [list(word) for word in fiber],
            "profile_overrides": {split: value for split, value in profile.items() if split != value},
            "complement_profile_overrides": {split: value for split, value in complement_profile.items()
                                             if split != value},
            "scope": "Abstract shared nonnegative capped profiles and a genuine five-step parent word. Both inverse words are locally fixed points; periodicity alone does not imply general alpha injectivity. Not a C example."}


def phase_alignment_witness():
    sequence, _, _, selected_splits = generate(196)
    trajectory, transient, period = full_orbit(sequence, 196)
    cycle = canonical_cycle(tuple(trajectory[transient:]))
    entry = trajectory[transient]
    entry_position = cycle.index(entry)
    depth = sequence[195]
    assert depth >= transient
    relative_phase = (depth - transient) % period
    selected_position = (entry_position + relative_phase) % period
    correct_split = cycle[selected_position]
    wrong_split = cycle[relative_phase]
    assert cycle == (115, 120, 116, 117, 118)
    assert correct_split == selected_splits[196] == 118
    assert wrong_split == 117
    correct_value = sequence[correct_split] + sequence[196 - correct_split]
    wrong_value = sequence[wrong_split] + sequence[196 - wrong_split]
    assert correct_value == sequence[196] == 134
    assert wrong_value == 131
    return {"index": 196, "canonical_cycle": list(cycle), "entry_point": entry,
            "entry_position": entry_position, "depth": depth, "transient": transient,
            "phase_from_entry": relative_phase, "phase_from_canonical_start": selected_position,
            "correct_split": correct_split, "wrong_split_without_alignment": wrong_split,
            "correct_value": correct_value, "wrong_value_without_alignment": wrong_value,
            "scope": "A stored canonical cycle needs entry alignment. One total selected-phase residue suffices once the prescribed basin and phase certificate are verified."}


def defect_box_examples():
    sharp_contexts = 0
    for length in (1, 3, 5, 7):
        for half_budget in range(1, 13):
            values = tuple(range(half_budget, 2 * half_budget + 1))
            profiles = [{split: 2 * half_budget - split for split in values},
                        *[{split: split for split in values}
                          for _ in range(length - 1)]]
            alpha = (2 * half_budget, *([3 * half_budget] * (length - 1)))
            words = []
            for seed in values:
                word = [seed]
                for position, parameter in enumerate(alpha):
                    word.append(parameter - profiles[position][word[-1]])
                assert word[-1] == seed
                assert all(split in values for split in word)
                words.append(tuple(word[:-1]))
            for extra in (0, 1):
                defects = (2 * half_budget + extra, *([0] * (length - 1)))
                lower, upper = defect_seed_interval(alpha, defects)
                modulus = sum(defects) // 2 + 1
                assert len(words) == modulus == half_budget + 1
                assert len({word[0] % modulus for word in words}) == modulus
                for word in words:
                    assert lower <= word[0] <= upper
                    assert lower + (word[0] % modulus - lower) % modulus == word[0]
                    assert all(0 <= split - profiles[position][split] <= defects[position]
                               for position, split in enumerate(word))
                sharp_contexts += 1
    even_contexts = 0
    for scale in range(13):
        values = tuple(range(scale + 1))
        profile = {split: split for split in values}
        assert seed_fiber((values, values), profile, (scale, scale)) == [
            (split, scale - split) for split in values]
        even_contexts += 1
    return {"sharp_odd_defect_box_contexts": sharp_contexts,
            "odd_lengths": [1, 3, 5, 7],
            "even_zero_defect_contexts": even_contexts,
            "scope": "Abstract position-dependent profiles, not C parent-cycle examples; odd bound is attained and even zero-defect fibers grow with the domain."}


def higher_order_seed_witness():
    index = 7739
    order = 20
    sequence, _, _, selected_splits = generate(index)
    assert sequence == brent_generate(index)
    fibonacci = fibonacci_values(index + 1)
    anchor, lower, child, child_lower = [fibonacci[order - shift]
                                        for shift in range(1, 5)]
    offsets = (498, 512, 500, 503, 513)
    for position, offset in enumerate(offsets):
        assert index - sequence[anchor + offset] == anchor + offsets[(position + 1) % 5]
    sets = candidate_sets(sequence, anchor, lower, child, child_lower, offsets)
    profile = {split: sequence[lower + split] - child
               for values in sets for split in values}
    alpha = (605, 678, 576, 520, 518)
    words = seed_fiber(sets, profile, alpha)
    assert words == [(255, 368, 344, 255, 283), (260, 364, 341, 258, 274)]
    delta = tuple(right - left for left, right in zip(*words))
    profile_delta = tuple(profile[right] - profile[left]
                          for left, right in zip(*words))
    assert all(delta[(position + 1) % 5] == -profile_delta[position]
               for position in range(5))
    negative = sum(difference * value < 0
                   for difference, value in zip(delta, profile_delta))
    assert negative % 2 == 1
    assert math.prod(profile_delta) == -math.prod(delta)
    assert words[0][0] % 5 == words[1][0] % 5
    defects = [lower + offset - sequence[anchor + offset] for offset in offsets]
    for values, defect in zip(sets, defects):
        defect_monotone_cover(values, profile, defect)
    interval = defect_seed_interval(alpha, defects)
    modulus = sum(defects) // 2 + 1
    assert all(interval[0] <= word[0] <= interval[1] for word in words)
    assert len({word[0] % modulus for word in words}) == len(words)
    for word in words:
        assert decode_defect_residue(sets, profile, alpha, defects, word[0] % modulus) == word
    full_profile = {split: sequence[lower + split] - child
                    for split in range(max(offsets) + 1)}
    periodic_sets = [periodic_profile_candidates(values, full_profile, offset)
                     for values, offset in zip(sets, offsets)]
    periodic_membership = [[split in values for split, values in zip(word, periodic_sets)]
                           for word in words]
    filtered_fiber = seed_fiber(periodic_sets, full_profile, alpha)
    assert filtered_fiber == []
    for offset, candidates, values in zip(offsets, sets, periodic_sets):
        cyclic_nodes = {point for cycle in all_cycles(sequence, anchor + offset) for point in cycle}
        assert values == tuple(split for split in candidates if lower + split in cyclic_nodes)
    selected = tuple(selected_splits[anchor + offset] - lower for offset in offsets)
    selected_alpha = tuple(selected[(position + 1) % 5] + full_profile[selected[position]]
                           for position in range(5))
    assert seed_fiber(periodic_sets, full_profile, selected_alpha) == [selected]
    terminal_periods = []
    for offset, split in zip(offsets, selected):
        trajectory, transient, period = full_orbit(sequence, anchor + offset)
        assert lower + split in trajectory[transient:]
        terminal_periods.append(period)
    return {
        "index": index,
        "order": order,
        "cycle_offsets": list(offsets),
        "alpha": list(alpha),
        "complete_fiber": [list(word) for word in words],
        "seed_candidates_checked": len(sets[0]),
        "split_difference": list(delta),
        "profile_difference": list(profile_delta),
        "negative_secants": negative,
        "same_seed_mod5": True,
        "defects": defects,
        "defect_seed_interval": list(interval),
        "adaptive_seed_modulus": modulus,
        "local_cycle_refinement": {"periodic_membership_by_word": periodic_membership,
                                   "periodic_candidate_lengths": [len(values) for values in periodic_sets],
                                   "original_alpha_filtered_fiber": [],
                                   "actually_selected_word": list(selected),
                                   "actually_selected_alpha": list(selected_alpha),
                                   "lower_terminal_periods": terminal_periods},
        "scope": "Complete fiber for this fixed alpha and these five candidate sets; a counterexample to global alpha injectivity and to the r_0 mod 5 refinement.",
    }


def higher_order_cover_witness():
    index, order, offset = 12898, 21, 1013
    sequence, _, _, _ = generate(index)
    assert sequence == brent_generate(index)
    fibonacci = fibonacci_values(index + 1)
    anchor, lower, child, child_lower = [fibonacci[order - shift]
                                        for shift in range(1, 5)]
    cycles = [canonical_cycle(tuple(point - anchor for point in cycle))
              for cycle in all_cycles(sequence, index)
              if len(cycle) == 5 and anchor + offset in cycle]
    assert len(cycles) == 1
    values = candidate_sets(sequence, anchor, lower, child, child_lower, (offset,))[0]
    profile = {split: sequence[lower + split] - child for split in values}
    descending = (659, 660, 661, 662)
    assert all(split in values for split in descending)
    assert tuple(profile[split] for split in descending) == (599, 597, 595, 589)
    parts = [tuple(split for split in values if split not in descending[1:]),
             *((split,) for split in descending[1:])]
    assert sorted(split for part in parts for split in part) == list(values)
    assert all(all(profile[first] <= profile[second]
                   for first, second in zip(part, part[1:])) for part in parts)
    defect = lower + offset - sequence[anchor + offset]
    defect_monotone_cover(values, profile, defect)
    return {"index": index, "order": order, "cycle_offsets": list(cycles[0]),
            "parent_offset": offset, "parent_defect": defect,
            "candidates_checked": len(values), "minimum_nondecreasing_cover": len(parts),
            "descending_splits": list(descending),
            "descending_profile_values": [profile[split] for split in descending],
            "nondecreasing_partition": [list(part) for part in parts],
            "scope": "Exact four-class lower and upper certificates for one C candidate set; refutes a universal three-class cover but does not establish a four-class uniform bound."}


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
    alpha_image_counts = []
    selected_seed_reconstructions = 0
    defect_cover_rows_checked = 0
    local_cycle_candidate_count = 0
    periodic_cartesian_combinations = 0
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
                row_profile = {split: sequence[lower_anchor + split] - child_anchor
                               for split in range(max(offsets) + 1)}
                periodic_sets = [periodic_profile_candidates(values, row_profile, offset)
                                 for values, offset in zip(sets, offsets)]
                local_cycle_candidate_count += sum(map(len, periodic_sets))
                periodic_cartesian_combinations += math.prod(map(len, periodic_sets))
                for offset, values in zip(offsets, sets):
                    defect = lower_anchor + offset - sequence[anchor + offset]
                    defect_monotone_cover(values, row_profile, defect)
                    defect_cover_rows_checked += 1
                alpha_images = set()
                for combination in product(*sets):
                    alpha_vector = []
                    for position, (offset, split) in enumerate(zip(offsets, combination)):
                        complement = offset - split
                        first = (sequence[lower_anchor + split] - child_anchor
                                 - max(0, split))
                        second = (sequence[child_anchor + complement] - child_lower_anchor
                                  - max(0, complement))
                        parent_defect = sequence[anchor + offset] - lower_anchor - offset
                        assert first + second == parent_defect
                        assert first <= 0 and second <= 0
                        next_split = combination[(position + 1) % 5]
                        next_offset = offsets[(position + 1) % 5]
                        alpha = (next_split
                                 + sequence[lower_anchor + split] - child_anchor)
                        next_complement = next_offset - next_split
                        beta = (next_complement
                                + sequence[child_anchor + complement]
                                - child_lower_anchor)
                        assert alpha + beta == index - fibonacci[order]
                        alpha_vector.append(alpha)
                    alpha_images.add(tuple(alpha_vector))
                    defects = [lower_anchor + offset - sequence[anchor + offset]
                               for offset in offsets]
                    seed_lower, seed_upper = defect_seed_interval(alpha_vector, defects)
                    assert seed_lower <= combination[0] <= seed_upper
                    assert seed_upper - seed_lower < sum(defects) // 2 + 1
                    row_local_combinations_checked += 1
                product_size = math.prod(lengths)
                assert len(alpha_images) == product_size
                alpha_image_counts.append(len(alpha_images))
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
                profile = {split: sequence[lower_anchor + split] - child_anchor
                           for values in sets for split in values}
                assert seed_fiber(sets, profile, alpha_values) == [tuple(recovered)]
                assert seed_fiber(periodic_sets, row_profile, alpha_values) == [tuple(recovered)]
                defects = [lower_anchor + offset - sequence[anchor + offset]
                           for offset in offsets]
                modulus = sum(defects) // 2 + 1
                assert decode_defect_residue(sets, profile, alpha_values, defects,
                                             recovered[0] % modulus) == tuple(recovered)
                selected_seed_reconstructions += 1
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
    assert selected_seed_reconstructions == 13
    assert parent_rows == 65
    assert ambiguous_rows == 57
    assert max(candidate_lengths) == 29
    assert noncontiguous_sets == 56
    assert reconstructed_selector_positions == 65
    assert reconstructed_parent_transitions == 65
    assert complementary_lower_map_rows == 65
    assert row_local_combinations_checked == 69064
    assert alpha_image_counts == [math.prod(row["candidate_lengths"])
                                  for row in payloads]
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
        "alpha_parameter_injectivity": {
            "payloads": len(alpha_image_counts),
            "row_local_combinations": row_local_combinations_checked,
            "distinct_alpha_vectors": sum(alpha_image_counts),
            "collisions": row_local_combinations_checked - sum(alpha_image_counts),
            "maximum_fiber": 1,
            "formula": "alpha_i = r_(i+1) + P_(k-2)(r_i)",
            "qualification": "Exact finite injectivity over every public row-local Cartesian product; alpha is a lossless reparameterization of the five selectors on this certificate, not a global theorem."
        },
        "seed_reconstruction": {
            "selected_public_fibers_checked": selected_seed_reconstructions,
            "formula": "r_(i+1) = alpha_i - P_(k-2)(r_i)",
            "qualification": "Given alpha and the lower profiles, one seed determines the complete selector word; uniqueness of the seed is a separate condition.",
        },
        "defect_seed_budget": {
            "row_local_combinations_checked": row_local_combinations_checked,
            "interval_formula": "ceil((alternating(alpha)-sum_odd(e))/2) <= r_0 <= floor((alternating(alpha)+sum_even(e))/2)",
            "adaptive_modulus": "B = floor(sum(e)/2)+1",
            "defect_monotone_cover_rows_checked": defect_cover_rows_checked,
            "nondecreasing_cover_bound": "floor(e_i/2)+1, by grouping floor((r-H_i(r))/2)",
            "qualification": "Exact odd-window argument; the interval is checked on all public row-local combinations. The modulus is a sufficient arithmetic label, not the minimum fiber cardinality.",
        },
        "abstract_defect_box_examples": defect_box_examples(),
        "local_cycle_refinement": {
            "retained_candidate_positions": local_cycle_candidate_count,
            "periodic_cartesian_combinations": periodic_cartesian_combinations,
            "actually_selected_words_preserved": selected_seed_reconstructions,
            "qualification": "Periodicity is necessary by the cycle-entry theorem; finite public injectivity follows also from the larger unfiltered audit. Whole captured lower profiles are required.",
            "abstract_periodic_collision": abstract_periodic_collision(),
        },
        "phase_alignment_witness": phase_alignment_witness(),
        "higher_order_seed_witness": higher_order_seed_witness(),
        "higher_order_profile_cover_witness": higher_order_cover_witness(),
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

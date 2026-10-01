"""Audit ordinal encodings of the five Fibonacci child-split selectors."""

from collections import Counter, defaultdict
from fractions import Fraction
import hashlib
import json
from itertools import combinations, product
import math
from pathlib import Path
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


def alpha_collision_fibers(sets, profile):
    difference_indices = []
    for values in sets:
        by_difference = defaultdict(list)
        for first in values:
            for second in values:
                if first != second:
                    by_difference[first - second].append((first, second))
        difference_indices.append(by_difference)
    fibers = defaultdict(set)
    for values in difference_indices[0].values():
        for start in values:
            if start[0] >= start[1]:
                continue
            paths = [(start,)]
            for position in range(len(sets) - 1):
                extended = []
                for path in paths:
                    first, second = path[-1]
                    difference = profile[first] - profile[second]
                    for following in difference_indices[position + 1].get(-difference, ()):
                        extended.append((*path, following))
                paths = extended
            for path in paths:
                first, second = path[-1]
                if start[0] - start[1] != -(profile[first] - profile[second]):
                    continue
                left = tuple(pair[0] for pair in path)
                right = tuple(pair[1] for pair in path)
                alpha = tuple(left[(position + 1) % len(sets)] + profile[left[position]]
                              for position in range(len(sets)))
                assert alpha == tuple(right[(position + 1) % len(sets)] + profile[right[position]]
                                      for position in range(len(sets)))
                fibers[alpha].update((left, right))
    return dict(fibers)


def collision_pair_completeness_examples():
    contexts = 0
    words_checked = 0
    for scale in range(4):
        values = tuple(range(scale + 1))
        for profile in product(*(range(point + 1) for point in values)):
            for length in (1, 2, 3, 5):
                sets = (values,) * length
                direct = defaultdict(set)
                for word in product(*sets):
                    alpha = tuple(word[(position + 1) % length] + profile[word[position]]
                                  for position in range(length))
                    direct[alpha].add(word)
                    words_checked += 1
                direct = {alpha: words for alpha, words in direct.items() if len(words) > 1}
                assert alpha_collision_fibers(sets, profile) == direct
                allowed = [tuple(value for value in values if (value + phase) % 2 == 0)
                           for phase in range(length)]
                assert minimum_gap_tests(sets, profile, allowed, scale) == minimum_periodicity_tests(
                    direct, allowed)
                contexts += 1
    return dict(contexts=contexts, cartesian_words=words_checked, gap_qualification_contexts=contexts,
                window_lengths=[1, 2, 3, 5],
                scope='Exhaustive small shared capped profiles: direct Cartesian fibers match pair paths, and the two gap-quotient qualification minima match collision-mask minima for alternating-value qualifications.')


def minimum_periodicity_tests(fibers, periodic):
    assert all(len(words) > 1 for words in fibers.values())
    word_masks = []
    pair_masks = []
    for words in fibers.values():
        masks = [tuple(split in values for split, values in zip(word, periodic)) for word in words]
        word_masks.extend(masks)
        pair_masks.extend(tuple(first and second for first, second in zip(left, right))
                          for left, right in combinations(masks, 2))
    result = {}
    for label, masks in (('raw_unique', word_masks), ('restricted_injective', pair_masks)):
        result[label] = dict(minimum=None, coordinates=[])
        for size in range(len(periodic) + 1):
            good = [subset for subset in combinations(range(len(periodic)), size)
                    if all(any(not mask[phase] for phase in subset) for mask in masks)]
            if good:
                result[label] = dict(minimum=size, coordinates=[list(subset) for subset in good])
                break
    return result


def gap_transitions(values, profile, bound, allowed=(), mode='raw'):
    admitted = set(allowed)
    transitions = defaultdict(set)
    for first in values:
        if mode != 'raw' and first not in admitted:
            continue
        for second in values:
            if mode == 'both' and second not in admitted:
                continue
            gap = second - first
            following = profile[first] - profile[second]
            if 0 < abs(gap) <= bound and 0 < abs(following) <= bound:
                transitions[gap].add(following)
    return dict(transitions)


def closed_gap_paths(transitions, bound):
    result = {}
    for start in sorted(transitions[0]):
        if not start or abs(start) > bound:
            continue
        paths = {start: (start,)}
        for relation in transitions:
            following_paths = {}
            for point, path in sorted(paths.items()):
                for following in sorted(relation.get(point, ())):
                    following_paths.setdefault(following, (*path, following))
            paths = following_paths
        if start in paths:
            result[start] = paths[start]
    return result


def minimum_gap_tests(sets, profile, periodic, bound):
    raw = [gap_transitions(values, profile, bound) for values in sets]
    result = {}
    for label, mode in (('raw_unique', 'first'), ('restricted_injective', 'both')):
        qualified = [gap_transitions(values, profile, bound, allowed, mode)
                     for values, allowed in zip(sets, periodic)]
        result[label] = dict(minimum=None, coordinates=[])
        for size in range(len(sets) + 1):
            good = []
            for coordinates in combinations(range(len(sets)), size):
                relations = [qualified[phase] if phase in coordinates else relation
                             for phase, relation in enumerate(raw)]
                if not closed_gap_paths(relations, bound):
                    good.append(list(coordinates))
            if good:
                result[label] = dict(minimum=size, coordinates=good)
                break
    return result


def gap_automaton_certificate(sets, profile, periodic, defects, expected):
    bound = sum(defects) // 2
    assert all(0 <= split - profile[split] <= defect
               for values, defect in zip(sets, defects) for split in values)
    assert minimum_gap_tests(sets, profile, periodic, bound) == expected
    raw = [gap_transitions(values, profile, bound) for values in sets]
    both = [gap_transitions(values, profile, bound, allowed, 'both')
            for values, allowed in zip(sets, periodic)]
    first = [gap_transitions(values, profile, bound, allowed, 'first')
             for values, allowed in zip(sets, periodic)]
    paths = closed_gap_paths(raw, bound)
    certificates = []
    for label, qualified in (('raw_unique', first), ('restricted_injective', both)):
        for coordinates in expected[label]['coordinates']:
            relations = [qualified[phase] if phase in coordinates else relation
                         for phase, relation in enumerate(raw)]
            assert closed_gap_paths(relations, bound) == {}
            certificates.append(dict(claim=label, coordinates=coordinates, closed_paths=0))
    start = next(point for point in sorted(paths) if point > 0)
    gap_path = paths[start]
    left, right = [], []
    for values, gap, following in zip(sets, gap_path, gap_path[1:]):
        pair = next((first, second) for first in values for second in values
                    if second - first == gap and profile[first] - profile[second] == following)
        left.append(pair[0])
        right.append(pair[1])
    alpha = tuple(left[(phase + 1) % len(sets)] + profile[left[phase]]
                  for phase in range(len(sets)))
    assert alpha == tuple(right[(phase + 1) % len(sets)] + profile[right[phase]]
                          for phase in range(len(sets)))
    return dict(defect_sum=sum(defects), absolute_gap_bound=bound,
                signed_state_capacity=2 * bound,
                raw_edge_counts=[sum(map(len, relation.values())) for relation in raw],
                both_periodic_edge_counts=[sum(map(len, relation.values())) for relation in both],
                first_periodic_edge_counts=[sum(map(len, relation.values())) for relation in first],
                raw_closed_start_gaps=sorted(paths), qualification_certificates=certificates,
                reconstructed_collision=dict(gap_path=list(gap_path), left=left, right=right,
                                              alpha=list(alpha)),
                scope='Exact signed-gap quotient and reverse reconstruction. Odd defect boxes bound every collision gap; qualified matrix products have empty diagonal. This certifies inverse properties without enumerating alpha fibers, but its state budget is context-dependent.')


def primitive_cycle_defect_cost(sequence):
    sharp_examples = []
    for length in range(3, 13):
        half = length // 2
        for parity in (0, 1):
            scale = 4 * length + parity
            if length % 2 and parity:
                centred = [value for positive in range(1, length, 2)
                           for value in (positive, -positive)] + [length]
            elif length % 2:
                centred = [value for positive in range(2 * half, 0, -2)
                           for value in (-positive, positive)] + [2 * half + 2]
            else:
                centred = [value for positive in range(length - 1, 1, -2)
                           for value in (-positive, positive)] + [-1, length + 1]
                if not parity:
                    centred = [value + (1 if value > 0 else -1) for value in centred]
            offsets = [(scale + value) // 2 for value in centred]
            assert len(offsets) == length and len(set(offsets)) == length
            assert all((scale + value) % 2 == 0 for value in centred)
            profile = list(range(scale + 1))
            for phase, offset in enumerate(offsets):
                profile[offset] = scale - offsets[(phase + 1) % length]
            assert all(0 <= value <= point for point, value in enumerate(profile))
            defects = [offset - profile[offset] for offset in offsets]
            expected = length + (length % 2 and not parity)
            assert sum(defects) == expected
            ordered = sorted(offsets)
            assert all(ordered[position - 1] + ordered[length - position - 1] >= scale
                       for position in range(1, (length - 1) // 2 + 1))
            assert all(scale - profile[offset] == offsets[(phase + 1) % length]
                       for phase, offset in enumerate(offsets))
            sharp_examples.append(dict(period=length, scale_parity=parity,
                                       attained_defect_sum=sum(defects)))
    checked = 0
    period_histogram = Counter()
    minimum = None
    fibonacci = fibonacci_values(len(sequence) + 1)
    order = 6
    for index in range(8, len(sequence)):
        while fibonacci[order + 1] <= index:
            order += 1
        trajectory, transient, period = full_orbit(sequence, index)
        if period < 3:
            continue
        scale = index - fibonacci[order]
        anchor = fibonacci[order - 1]
        offsets = [point - anchor for point in trajectory[transient:]]
        defects = [offset + offsets[(phase + 1) % period] - scale
                   for phase, offset in enumerate(offsets)]
        assert min(defects) >= 0
        total = sum(defects)
        assert total >= period + (period % 2 and scale % 2 == 0)
        ordered = sorted(offsets)
        assert all(ordered[position - 1] + ordered[period - position - 1] >= scale
                   for position in range(1, (period - 1) // 2 + 1))
        checked += 1
        period_histogram[period] += 1
        ratio = Fraction(total, period)
        if minimum is None or ratio < Fraction(minimum['defect_sum'], minimum['period']):
            minimum = dict(index=index, period=period, offset=scale,
                           cycle_offsets=offsets, defect_sum=total)
    return dict(abstract_sharp_contexts=sharp_examples,
                selected_conway_indices=[8, len(sequence) - 1],
                selected_cycles_of_period_at_least_three=checked,
                period_histogram=dict(sorted(period_histogram.items())),
                minimum_observed_mean_defect=minimum,
                bound='sum(e_i)>=period for every proper cycle of period>=3; odd period and even offset require at least period+1',
                scope='General sorted-vertex cut proof. Sharpness examples are capped abstract profiles, not C instances; selected C cycles are finite corroboration.')


def periodic_pivot_witnesses():
    sequence, _, _, selected_splits = generate(28996)
    assert sequence == brent_generate(28996)
    fibonacci = fibonacci_values(28997)
    result = []
    for index, order, offsets, sample_alpha in (
            (11342, 21, (197, 202, 201, 198, 206), (181, 186, 130, 161, 191)),
            (28996, 23, (166, 174, 169, 170, 173), (105, 94, 68, 96, 133))):
        anchor, lower, child, child_lower = [fibonacci[order - shift] for shift in range(1, 5)]
        assert all(index - sequence[anchor + offset] == anchor + offsets[(phase + 1) % 5]
                   for phase, offset in enumerate(offsets))
        sets = candidate_sets(sequence, anchor, lower, child, child_lower, offsets)
        profile = {split: sequence[lower + split] - child
                   for split in range(max(offsets) + 1)}
        periodic = [periodic_profile_candidates(values, profile, offset)
                    for values, offset in zip(sets, offsets)]
        for offset, values, retained in zip(offsets, sets, periodic):
            nodes = {point - lower for cycle in all_cycles(sequence, anchor + offset)
                     for point in cycle}
            assert retained == tuple(point for point in values if point in nodes)
        fibers = alpha_collision_fibers(sets, profile)
        assert len(fibers) == (279 if index == 11342 else 5472)
        assert all(len(words) == 2 for words in fibers.values())
        for alpha, words in fibers.items():
            assert set(seed_fiber(sets, profile, alpha)) == words
        projections = [set() for _ in range(5)]
        for words in fibers.values():
            for word in words:
                for phase, split in enumerate(word):
                    projections[phase].add(split)
        pivots = [phase for phase in range(5)
                  if projections[phase].isdisjoint(periodic[phase])]
        assert pivots == ([3] if index == 11342 else [])
        tests = minimum_periodicity_tests(fibers, periodic)
        defects = [lower + offset - sequence[anchor + offset] for offset in offsets]
        gap_certificate = gap_automaton_certificate(sets, profile, periodic, defects, tests)
        if index == 11342:
            assert tests['raw_unique'] == dict(minimum=1, coordinates=[[3]])
            assert tests['restricted_injective'] == dict(minimum=1, coordinates=[[3], [4]])
        else:
            assert tests['raw_unique'] == dict(minimum=2, coordinates=[[1, 3]])
            assert tests['restricted_injective'] == dict(minimum=1, coordinates=[[1]])
            assert periodic[1] == (17, 24, 25)
            pivot_relation = gap_transitions(sets[1], profile, 4, periodic[1], 'both')
            assert pivot_relation == {-1: {1}, 1: {-1}}
            unit_relations = []
            for phase in (2, 3, 4):
                relation = gap_transitions(sets[phase], profile, 4)
                assert relation[-1] == {1} and relation[1] == {-1}
                unit_relations.append(dict(position=phase, negative_gap_outputs=[1],
                                           positive_gap_outputs=[-1]))
            first_relation = gap_transitions(sets[0], profile, 4)
            assert first_relation[1] == {-2, -1} and first_relation[-1] == {1, 2}
            gap_certificate['hand_check'] = dict(pivot=1, periodic_candidates=list(periodic[1]),
                                                 qualified_pivot_edges=[[-1, 1], [1, -1]],
                                                 successor_unit_edges=unit_relations,
                                                 final_positive_gap_outputs=[-2, -1],
                                                 final_negative_gap_outputs=[1, 2])
        selected = tuple(selected_splits[anchor + offset] - lower for offset in offsets)
        selected_alpha = tuple(selected[(phase + 1) % 5] + profile[selected[phase]]
                               for phase in range(5))
        assert all(split in values for split, values in zip(selected, periodic))
        for condition in tests.values():
            for coordinates in condition['coordinates']:
                restricted = [periodic[phase] if phase in coordinates else values
                              for phase, values in enumerate(sets)]
                assert alpha_collision_fibers(restricted, profile) == {}
                assert seed_fiber(restricted, profile, selected_alpha) == [selected]
        sample = sorted(fibers[sample_alpha])
        flags = [[split in values for split, values in zip(word, periodic)] for word in sample]
        raw_competitor = None
        if index == 11342:
            assert sample == [(78, 105, 87, 43, 118), (82, 101, 86, 46, 115)]
            assert flags == [[False, True, True, False, False],
                             [True, True, True, False, True]]
        else:
            assert sample == [(57, 49, 48, 20, 76), (58, 47, 47, 21, 75)]
            assert flags == [[True, False, True, True, True]] * 2
            competitor_alpha = (81, 113, 133, 98, 113)
            competitor_words = sorted(fibers[competitor_alpha])
            assert competitor_words == [(57, 25, 88, 45, 56), (58, 23, 90, 43, 55)]
            competitor_flags = [[split in values for split, values in zip(word, periodic)]
                                for word in competitor_words]
            assert competitor_flags == [[True, True, True, False, False],
                                        [True, False, True, False, True]]
            raw_competitor = dict(alpha=list(competitor_alpha),
                                  words=[list(word) for word in competitor_words],
                                  periodicity=competitor_flags)
        serialized = [{'alpha': list(alpha), 'words': [list(word) for word in sorted(words)]}
                      for alpha, words in sorted(fibers.items())]
        digest = hashlib.sha256(json.dumps(serialized, sort_keys=True,
                                           separators=(',', ':')).encode()).hexdigest()
        result.append(dict(index=index, order=order, cycle_offsets=list(offsets),
                           candidate_sizes=list(map(len, sets)),
                           raw_cartesian_words=math.prod(map(len, sets)),
                           complete_nontrivial_fibers=len(fibers), maximum_fiber=2,
                           complete_nontrivial_fibers_sha256=digest,
                           periodic_pivots=pivots, minimum_periodicity_tests=tests,
                           actual_word=list(selected),
                           selected_alpha=list(selected_alpha), sample_alpha=list(sample_alpha),
                           sample_fiber=[list(word) for word in sample], sample_periodicity=flags,
                           one_test_raw_competitor=raw_competitor,
                           gap_automaton=gap_certificate))
    return dict(contexts=result, primitive_cycle_defect_cost=primitive_cycle_defect_cost(sequence),
                qualification='Minimum coordinate counts distinguish injectivity after the periodicity restrictions from the stronger raw-image uniqueness. The n=28996 context needs one check for the former and two for the latter; four other periodic coordinates still leave a collision. The two contexts together rule out any single fixed coordinate for restricted injectivity. Universal bounded adaptive-test existence for C remains open.')


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
    tests = minimum_periodicity_tests({alpha: set(fiber)}, periodic_sets)
    assert tests == {'raw_unique': dict(minimum=None, coordinates=[]),
                     'restricted_injective': dict(minimum=None, coordinates=[])}
    return {"scale": scale, "parent_offsets": list(offsets), "parent_defects": list(defects),
            "alpha": list(alpha), "two_periodic_words": [list(first), list(second)],
            "complete_periodic_fiber": [list(word) for word in fiber],
            "minimum_periodicity_tests": tests,
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


def recursive_window_audit(sequence, selected_splits, fibonacci, roots):
    assert sequence == brent_generate(len(sequence) - 1)
    boundary_rows = 0
    for order in range(6, len(fibonacci) - 1):
        for offset in range(fibonacci[order - 1] + 1):
            index = fibonacci[order] + offset
            if index >= len(sequence):
                break
            split = selected_splits[index] - fibonacci[order - 1]
            assert max(0, offset - fibonacci[order - 3]) <= split
            assert split <= min(offset, fibonacci[order - 2])
            boundary_rows += 1
    artificial_roots = []
    for order in range(6, 14):
        values = (0, 1, fibonacci[order - 3], fibonacci[order - 2],
                  fibonacci[order - 1])
        for length in (1, 2, 3, 5, 6):
            offsets = tuple(values[phase % len(values)] for phase in range(length))
            parameters = tuple(offsets[(phase + 1) % length]
                               + sequence[fibonacci[order] + offset] - fibonacci[order - 1]
                               for phase, offset in enumerate(offsets))
            artificial_roots.append((order, offsets, parameters))
    nodes_by_order = Counter()
    leaf_orders = Counter()
    literal_selected_indices = set()
    child_parameter_words = 0
    nonconstant_child_words = 0
    maximum_depth = 0
    first_example = None
    inverse_decodings = 0
    root_budgets = []
    for root_number, root in enumerate([*roots, *artificial_roots]):
        root_order, root_offsets, root_parameters = root
        root_cost = sum(offset - sequence[fibonacci[root_order] + offset] + fibonacci[root_order - 1]
                        for offset in root_offsets)
        frontier_costs = Counter()
        frontier_bits = Counter()
        frontier_ambiguous = Counter()
        stack = [(*root, 0)]
        while stack:
            order, offsets, parameters, depth = stack.pop()
            maximum_depth = max(maximum_depth, depth)
            nodes_by_order[order] += 1
            assert all(0 <= offset <= fibonacci[order - 1] for offset in offsets)
            profile = tuple(sequence[fibonacci[order] + offset] - fibonacci[order - 1]
                            for offset in offsets)
            assert all(0 <= value <= offset for offset, value in zip(offsets, profile))
            node_cost = sum(offset - value for offset, value in zip(offsets, profile))
            frontier_costs[depth] += node_cost
            assert all(offsets[(phase + 1) % len(offsets)] == parameter - value
                       for phase, (parameter, value) in enumerate(zip(parameters, profile)))
            if order <= 5:
                assert all(fibonacci[order] + offset <= 8 for offset in offsets)
                leaf_orders[order] += 1
                continue
            splits = tuple(selected_splits[fibonacci[order] + offset] - fibonacci[order - 1]
                           for offset in offsets)
            complements = tuple(offset - split for offset, split in zip(offsets, splits))
            assert all(0 <= split <= fibonacci[order - 2] for split in splits)
            assert all(0 <= complement <= fibonacci[order - 3] for complement in complements)
            first_values = tuple(sequence[fibonacci[order - 1] + split] - fibonacci[order - 2]
                                 for split in splits)
            second_values = tuple(sequence[fibonacci[order - 2] + complement] - fibonacci[order - 3]
                                  for complement in complements)
            assert all(value == first + second
                       for value, first, second in zip(profile, first_values, second_values))
            first_parameters = tuple(splits[(phase + 1) % len(splits)] + value
                                     for phase, value in enumerate(first_values))
            second_parameters = tuple(complements[(phase + 1) % len(complements)] + value
                                      for phase, value in enumerate(second_values))
            assert all(parameter == first + second for parameter, first, second
                       in zip(parameters, first_parameters, second_parameters))
            parent_cost = sum(offset - value for offset, value in zip(offsets, profile))
            first_cost = sum(split - value for split, value in zip(splits, first_values))
            second_cost = sum(complement - value
                              for complement, value in zip(complements, second_values))
            assert min(parent_cost, first_cost, second_cost) >= 0
            assert parent_cost == first_cost + second_cost
            assert all(0 <= value <= split for split, value in zip(splits, first_values))
            assert all(0 <= value <= complement for complement, value
                       in zip(complements, second_values))
            if len(offsets) % 2:
                defects = tuple(offset - value for offset, value in zip(offsets, profile))
                sets = candidate_sets(sequence, fibonacci[order], fibonacci[order - 1],
                                      fibonacci[order - 2], fibonacci[order - 3], offsets)
                geometric_sets = [tuple(split for split in values
                                        if max(0, offset - fibonacci[order - 3]) <= split
                                        <= min(offset, fibonacci[order - 2]))
                                  for offset, values in zip(offsets, sets)]
                lower_profile = {split: sequence[fibonacci[order - 1] + split] - fibonacci[order - 2]
                                 for values in geometric_sets for split in values}
                modulus = parent_cost // 2 + 1
                assert decode_defect_residue(geometric_sets, lower_profile, first_parameters,
                                             defects, splits[0] % modulus) == splits
                inverse_decodings += 1
                frontier_bits[depth] += (parent_cost // 2).bit_length()
                frontier_ambiguous[depth] += parent_cost >= 2
            for offset in offsets:
                index = fibonacci[order] + offset
                if index in literal_selected_indices:
                    continue
                point = index - 1
                for iteration in range(sequence[index - 1]):
                    point = index - sequence[point]
                assert point == selected_splits[index]
                literal_selected_indices.add(index)
            child_parameter_words += 2
            nonconstant_child_words += sum(len(set(word)) > 1
                                           for word in (first_parameters, second_parameters))
            if root_number == 0 and depth == 0:
                first_example = dict(profile_order=order, offsets=list(offsets),
                                     parameters=list(parameters), first_offsets=list(splits),
                                     second_offsets=list(complements),
                                     first_parameters=list(first_parameters),
                                     second_parameters=list(second_parameters))
            stack.extend(((order - 1, splits, first_parameters, depth + 1),
                          (order - 2, complements, second_parameters, depth + 1)))
        assert all(cost <= root_cost for cost in frontier_costs.values())
        if len(root_offsets) % 2:
            assert all(bits <= root_cost // 2 for bits in frontier_bits.values())
            assert all(count <= root_cost // 2 for count in frontier_ambiguous.values())
            bit_bound = (root_order - 5) * (root_cost // 2)
            assert sum(frontier_bits.values()) <= bit_bound
            assert sum(frontier_ambiguous.values()) <= bit_bound
            root_budgets.append(dict(root_kind='selected_five_window' if root_number < len(roots)
                                    else 'boundary_word', profile_order=root_order,
                                     window_length=len(root_offsets), root_defect_sum=root_cost,
                                     total_adaptive_seed_bits=sum(frontier_bits.values()),
                                     total_seed_bit_upper_bound=bit_bound,
                                     potential_ambiguous_nodes=sum(frontier_ambiguous.values()),
                                     maximum_frontier_seed_bits=max(frontier_bits.values(), default=0)))
    return dict(selected_five_window_roots=len(roots), boundary_test_roots=len(artificial_roots),
                geometric_selected_rows=boundary_rows, nodes_by_profile_order=dict(sorted(nodes_by_order.items())),
                leaf_orders=dict(sorted(leaf_orders.items())), maximum_depth=maximum_depth,
                literal_selected_points=len(literal_selected_indices), child_parameter_words=child_parameter_words,
                nonconstant_child_parameter_words=nonconstant_child_words,
                first_five_window_descent=first_example,
                odd_node_inverse_decodings=inverse_decodings, odd_root_seed_budgets=root_budgets,
                scope='Exact recursive nonautonomous windows with inherited row alignment. Child parameters add to the parent row parameter; all selected offsets stay in the two natural lower Fibonacci blocks, including endpoints. Leaf evaluations use indices at most eight. This certifies the recursive representation, not a uniform branch alphabet, minimal total certificate size, or an independent algorithm for choosing the splits.')


def terminal_orders(order):
    if order <= 5:
        return (order,)
    return terminal_orders(order - 2) + terminal_orders(order - 1)


def terminal_tables(orders):
    tables = [None] * (len(orders) + 1)
    tables[-1] = {(0, 0): 1}
    for position in range(len(orders) - 1, -1, -1):
        capacity = orders[position] - 2
        counts = defaultdict(int)
        for (offset, defect), count in tables[position + 1].items():
            for value in range(capacity + 1):
                counts[(offset + value, defect + (value == capacity))] += count
        tables[position] = dict(counts)
    return tables


def rank_terminal_word(orders, tables, word):
    offset = sum(word)
    defect = sum(value == order - 2 for order, value in zip(orders, word))
    ordinal = 0
    for position, (order, value) in enumerate(zip(orders, word)):
        capacity = order - 2
        assert 0 <= value <= capacity
        for smaller in range(value):
            ordinal += tables[position + 1].get((offset - smaller,
                                                 defect - (smaller == capacity)), 0)
        offset -= value
        defect -= value == capacity
    assert (offset, defect) == (0, 0)
    return ordinal


def unrank_terminal_word(orders, tables, offset, defect, ordinal):
    assert 0 <= ordinal < tables[0].get((offset, defect), 0)
    word = []
    for position, order in enumerate(orders):
        capacity = order - 2
        for value in range(capacity + 1):
            count = tables[position + 1].get((offset - value,
                                             defect - (value == capacity)), 0)
            if ordinal < count:
                word.append(value)
                offset -= value
                defect -= value == capacity
                break
            ordinal -= count
        else:
            raise AssertionError('Terminal ordinal has no continuation.')
    assert (offset, defect, ordinal) == (0, 0, 0)
    return tuple(word)


def terminal_tree(order, word, fibonacci):
    position = 0
    records = []

    def rebuild(height):
        nonlocal position
        if height <= 5:
            offset = word[position]
            position += 1
            assert 0 <= offset <= height - 2
            return offset, int(offset == height - 2)
        complement, second_defect = rebuild(height - 2)
        split, first_defect = rebuild(height - 1)
        offset = split + complement
        defect = first_defect + second_defect
        assert 0 <= offset <= fibonacci[height - 1]
        assert max(0, offset - fibonacci[height - 3]) <= split <= min(offset, fibonacci[height - 2])
        records.append((height, offset, defect, split))
        return offset, defect

    root = rebuild(order)
    assert position == len(word)
    return root, records


def terminal_code_audit(sequence, selected_splits, fibonacci, roots):
    table_cache = {order: (terminal_orders(order), terminal_tables(terminal_orders(order)))
                   for order in range(6, 14)}
    exhaustive_words = 0
    support_pairs = 0
    histogram_contexts = 0
    histogram_constraints = [[1, 1, 1, 0, 0, 0, 0], [0, 0, 0, 1, 1, 1, 1],
                             [0, 1, 2, 0, 1, 2, 3], [0, 0, 1, 0, 0, 0, 1]]
    assert affine_rank(histogram_constraints) == 4
    for order, (orders, tables) in table_cache.items():
        first_count, second_count = fibonacci[order - 5], fibonacci[order - 4]
        assert orders.count(4) == first_count and orders.count(5) == second_count
        assert len(orders) == fibonacci[order - 3]
        assert sum(tables[0].values()) == 3 ** first_count * 4 ** second_count
        for offset in range(fibonacci[order - 1] + 1):
            lower = max(0, offset - fibonacci[order - 2])
            upper = min(fibonacci[order - 3], offset // 2, (offset + first_count) // 3)
            assert {defect for (value, defect) in tables[0] if value == offset} == set(range(lower, upper + 1))
        support_pairs += len(tables[0])
        if order > 9:
            continue
        direct = Counter()
        for word in product(*(range(height - 1) for height in orders)):
            key = (sum(word), sum(value == height - 2 for height, value in zip(orders, word)))
            ordinal = rank_terminal_word(orders, tables, word)
            assert ordinal == direct[key]
            assert unrank_terminal_word(orders, tables, *key, ordinal) == word
            assert terminal_tree(order, word, fibonacci)[0] == key
            direct[key] += 1
            exhaustive_words += 1
        assert direct == tables[0]
        by_histogram = Counter()
        for first_marked in range(first_count + 1):
            for first_single in range(first_count - first_marked + 1):
                first_zero = first_count - first_marked - first_single
                for second_marked in range(second_count + 1):
                    for second_double in range(second_count - second_marked + 1):
                        for second_single in range(second_count - second_marked - second_double + 1):
                            second_zero = second_count - second_marked - second_double - second_single
                            counts = (first_zero, first_single, first_marked,
                                      second_zero, second_single, second_double, second_marked)
                            offset = first_single + 2 * first_marked + second_single + 2 * second_double + 3 * second_marked
                            defect = first_marked + second_marked
                            assert first_marked == defect - second_marked
                            assert first_single == offset - 2 * defect - second_marked - second_single - 2 * second_double
                            assert first_zero == first_count - offset + defect + 2 * second_marked + second_single + 2 * second_double
                            ways = math.factorial(first_count) * math.factorial(second_count)
                            ways //= math.prod(math.factorial(count) for count in counts)
                            by_histogram[(offset, defect)] += ways
                            histogram_contexts += 1
        assert by_histogram == tables[0]
    actual_rows = 0
    reconstructed_internal_rows = 0
    examples = []
    for order, offsets, parameters in roots:
        orders, tables = table_cache[order]
        choices = []
        ordinals = []
        histograms = []
        for offset in offsets:
            stack = [(order, offset)]
            word = []
            while stack:
                height, value = stack.pop()
                if height <= 5:
                    word.append(value)
                    continue
                split = selected_splits[fibonacci[height] + value] - fibonacci[height - 1]
                stack.extend(((height - 1, split), (height - 2, value - split)))
            defect = offset - sequence[fibonacci[order] + offset] + fibonacci[order - 1]
            assert defect == sum(value == height - 2 for height, value in zip(orders, word))
            assert sum(word) == offset
            ordinal = rank_terminal_word(orders, tables, word)
            decoded = unrank_terminal_word(orders, tables, offset, defect, ordinal)
            assert decoded == tuple(word)
            recovered, records = terminal_tree(order, decoded, fibonacci)
            assert recovered == (offset, defect)
            for height, value, cost, split in records:
                assert value - cost == sequence[fibonacci[height] + value] - fibonacci[height - 1]
                assert split == selected_splits[fibonacci[height] + value] - fibonacci[height - 1]
                reconstructed_internal_rows += 1
            actual_rows += 1
            choices.append(tables[0][(offset, defect)])
            ordinals.append(ordinal)
            counts = Counter(zip(orders, word))
            histograms.append([counts[(height, value)] for height in (4, 5)
                               for value in range(height - 1)])
        examples.append(dict(profile_order=order, offsets=list(offsets),
                             leaf_order_counts=[orders.count(4), orders.count(5)],
                             geometric_tree_counts=choices, tree_ordinals=ordinals,
                             joint_fixed_width_bits=(math.prod(choices) - 1).bit_length(),
                             terminal_histograms=histograms))
    shared_histogram_words = ((2, 0, 0), (0, 0, 2))
    assert terminal_orders(7) == (5, 4, 5)
    assert len({tuple(sorted(zip(terminal_orders(7), word))) for word in shared_histogram_words}) == 1
    assert {terminal_tree(7, word, fibonacci)[0] for word in shared_histogram_words} == {(2, 0)}
    alternatives = []
    for word in shared_histogram_words:
        _, records = terminal_tree(7, word, fibonacci)
        assert all(value - cost == sequence[fibonacci[height] + value] - fibonacci[height - 1]
                   for height, value, cost, split in records)
        assert all(split == selected_splits[fibonacci[height] + value] - fibonacci[height - 1]
                   for height, value, cost, split in records[:-1])
        alternatives.append(fibonacci[6] + records[-1][3])
    assert alternatives == [8, 10] and selected_splits[15] == 8
    trajectory, transient, period = full_orbit(sequence, 15)
    assert trajectory[transient:] == [8, 10] and transient == 3 and period == 2
    assert sequence[14] == 9
    return dict(leaf_alphabet=['4:0', '4:1', '4:2', '5:0', '5:1', '5:2', '5:3'],
                generating_function='(1+z+z^2*w)^F_(j-5) * (1+z+z^2+z^3*w)^F_(j-4)',
                support_interval='max(0,u-F_(j-2)) <= E <= min(F_(j-3),floor(u/2),floor((u+F_(j-5))/3))',
                coefficient_support_pairs_checked=support_pairs, exhaustive_geometric_words=exhaustive_words,
                histogram_constraint_rank=4, free_histogram_coordinates=3,
                histogram_multiplicities_checked=histogram_contexts,
                actual_selected_tree_rows=actual_rows, reconstructed_internal_rows=reconstructed_internal_rows,
                five_window_codes=examples,
                histogram_phase_witness=dict(index=15, words=[list(word) for word in shared_histogram_words],
                                             admissible_splits=alternatives, actually_selected_split=8,
                                             child_parameters=[0, 4], cycle=[8, 10], transient=3, depth=9,
                                             common_value=sequence[15]),
                scope='Exact seven-symbol coding of full geometric selector trees. Coefficient ordinals recover all internal offsets and formal profile values; actual codes are checked against C and its selected splits. Geometric multiplicities exclude shared-profile consistency and prescribed-orbit validity; they are not minimum code sizes for the narrower C family.')


def unbounded_defect_audit():
    sequence, _, _, _ = generate(131071)
    assert sequence == brent_generate(131071)
    fibonacci = fibonacci_values(131072)
    knees = []
    for order in range(22, 26):
        index = fibonacci[order] + fibonacci[order - 2]
        cost = fibonacci[order] - sequence[index]
        lower = (fibonacci[order - 3] + 2) // 3
        assert sequence[index] * 3 <= 2 * index
        assert cost >= lower
        knees.append(dict(profile_order=order, index=index, defect=cost, lower_bound=lower))
    centres = []
    for order in range(23, 26):
        anchor, width = fibonacci[order - 1], fibonacci[order - 3]
        index = 2 * anchor
        cycles = all_cycles(sequence, index)
        minimum = None
        histogram = Counter()
        for cycle in cycles:
            assert all(anchor <= point <= anchor + width for point in cycle)
            assert all(sequence[point] * 3 <= 2 * point for point in cycle)
            cost = 2 * sum(point - anchor for point in cycle) - len(cycle) * width
            assert 5 * cost >= len(cycle) * (2 * anchor - 5 * width)
            histogram[len(cycle)] += 1
            mean = Fraction(cost, len(cycle))
            minimum = mean if minimum is None else min(minimum, mean)
        centres.append(dict(index=index, cycles=len(cycles), period_histogram=dict(sorted(histogram.items())),
                            minimum_mean_defect=str(minimum),
                            lower_bound_mean=str(Fraction(2 * anchor - 5 * width, 5))))
    for order in range(6, 15):
        for offset in range(fibonacci[order - 1] + 1):
            split = min(fibonacci[order - 2], max(0, offset - fibonacci[order - 4]))
            complement = offset - split
            assert max(0, offset - fibonacci[order - 3]) <= split <= min(offset, fibonacci[order - 2])
            assert min(split, fibonacci[order - 3]) + min(complement, fibonacci[order - 4]) == min(offset, fibonacci[order - 2])
    assert sequence[11] == 7
    upper_values = [0, 1]
    for index in range(2, 12):
        height = 3
        while fibonacci[height + 1] <= index:
            height += 1
        upper_values.append(min(index - fibonacci[height - 2], fibonacci[height]))
    assert upper_values[:11] == sequence[:11] and upper_values[11] == 8
    upper_selected = None
    upper_nested_value = None
    for index in range(3, 12):
        point = index - 1
        for iteration in range(upper_values[index - 1]):
            point = index - upper_values[point]
        value = upper_values[point] + upper_values[index - point]
        if index < 11:
            assert value == upper_values[index]
        else:
            upper_selected, upper_nested_value = point, value
    assert (upper_selected, upper_nested_value) == (6, 7)
    return dict(knee_examples=knees, all_cycle_centre_examples=centres,
                uniform_bounds=dict(knee='lambda_j(F_(j-2)) >= ceil(F_(j-3)/3) once F_j+F_(j-2)>=16384',
                                    centre='E/p >= 2*F_(k-1)/5-F_(k-3) at n=2*F_(k-1), F_(k-1)>=16384'),
                upper_cap_geometric_family=dict(profile='Q_j(u)=min(u,F_(j-2))',
                                                 split='r=min(F_(j-2),max(0,u-F_(j-4)))',
                                                 first_recurrence_failure=11, claimed_value=8,
                                                 actual_nested_value=7, prescribed_split=6),
                scope='General lower bounds follow from the previously proved C(m)<=2m/3 envelope and cycle capture. Actual profile defects grow linearly along Fibonacci knees; every centre cycle has linearly growing mean defect. The upper-cap family has consistent geometric descent and the same small leaves but fails prescribed nested selection; no global convergence follows from geometric closure alone.')


def main():
    limit = 609
    fibonacci = fibonacci_values(limit + 1)
    sequence, _, _, selected_splits = generate(limit)
    payloads = []
    recursive_roots = []
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
                recursive_roots.append((order - 1, tuple(offsets),
                                        (index - fibonacci[order],) * 5))
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
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "scope": "Exact public three-block selector audit, recursive nonautonomous window descent and conserved conditional seed-label budgets. Row-local Cartesian decompositions remain distinct from actual selected splits and their proof costs.",
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
            "scope": "all 65 public parent rows; q_i = u_i - r_i and t = n - F_k",
            "interpretation": "The two lower-map parameters are exact complements at the parent scale. They close nonautonomous child windows, not necessarily autonomous lower C five-cycles."
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
        "collision_pair_completeness": collision_pair_completeness_examples(),
        "periodic_pivot_witnesses": periodic_pivot_witnesses(),
        "recursive_parameter_windows": recursive_window_audit(sequence, selected_splits, fibonacci,
                                                               recursive_roots),
        "terminal_selector_codes": terminal_code_audit(sequence, selected_splits, fibonacci, recursive_roots),
        "unbounded_profile_defects": unbounded_defect_audit(),
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

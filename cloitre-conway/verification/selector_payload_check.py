"""Audit ordinal encodings of the five Fibonacci child-split selectors."""

from collections import Counter, defaultdict
from bisect import bisect_right
from fractions import Fraction
from functools import lru_cache
import hashlib
import json
from itertools import combinations, product
import math
from pathlib import Path
import sys

from conway_explore import brent_generate, full_orbit, generate, g_closed
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


def shared_word(word, labels):
    representatives = {}
    for label, value in zip(labels, word):
        if label in representatives and representatives[label] != value:
            return False
        representatives[label] = value
    return True


def shared_gap_classes(labels):
    length = len(labels)
    classes = list(range(length))

    def representative(position):
        while classes[position] != position:
            position = classes[position]
        return position

    for position in range(length):
        for earlier in range(position):
            if labels[position] != labels[earlier]:
                continue
            for first, second in ((position, earlier),
                                  ((position + 1) % length, (earlier + 1) % length)):
                classes[representative(first)] = representative(second)
    return tuple(representative(position) for position in range(length))


def shared_monotone_obstruction(sets, profile, labels):
    classes = shared_gap_classes(labels)
    edges = set()
    for phase, values in enumerate(sets):
        if all(profile[first] <= profile[second] for first, second in zip(values, values[1:])):
            edges.add(tuple(sorted((classes[phase], classes[(phase + 1) % len(labels)]))))
    neighbours = defaultdict(set)
    for first, second in edges:
        neighbours[first].add(second)
        neighbours[second].add(first)
    colours = {}
    for start in neighbours:
        if start in colours:
            continue
        colours[start] = 0
        stack = [start]
        while stack:
            point = stack.pop()
            for following in neighbours[point]:
                if following in colours:
                    if colours[following] == colours[point]:
                        return True
                else:
                    colours[following] = 1 - colours[point]
                    stack.append(following)
    return False


def shared_gap_words(sets, profile, labels, bound):
    length = len(labels)
    classes = shared_gap_classes(labels)
    assert all(sets[position] == sets[earlier]
               for position in range(length) for earlier in range(position)
               if labels[position] == labels[earlier])
    transitions = [gap_transitions(values, profile, bound) for values in sets]
    result = {}

    def extend(path, assigned):
        position = len(path) - 1
        for following in sorted(transitions[position].get(path[-1], ())):
            if position == length - 1:
                if following != path[0]:
                    continue
                left, right = [], []
                pairs = {}
                for phase, values in enumerate(sets):
                    label = labels[phase]
                    if label not in pairs:
                        pairs[label] = next((first, second) for first in values for second in values
                                            if second - first == path[phase]
                                            and profile[first] - profile[second]
                                            == path[(phase + 1) % length])
                    first, second = pairs[label]
                    left.append(first)
                    right.append(second)
                result[tuple(path)] = (tuple(left), tuple(right))
                continue
            group = classes[position + 1]
            if group in assigned and assigned[group] != following:
                continue
            extend((*path, following), {**assigned, group: following})

    for start in sorted(transitions[0]):
        extend((start,), {classes[0]: start})
    return result


def row_partitions(length):
    if length == 0:
        yield ()
        return
    for prefix in row_partitions(length - 1):
        for label in range(max(prefix, default=-1) + 2):
            yield (*prefix, label)


def shared_row_completeness_examples():
    contexts = 0
    direct_words = 0
    binary_contexts = 0
    patterns = tuple(row_partitions(5))
    assert len(patterns) == 52
    for scale in range(4):
        values = tuple(range(scale + 1))
        for profile in product(*(range(point + 1) for point in values)):
            self_gaps = {second - first for first in values for second in values
                         if first != second and profile[first] - profile[second] == second - first}
            for labels in patterns:
                classes = max(labels) + 1
                images = defaultdict(list)
                for choices in product(values, repeat=classes):
                    word = tuple(choices[label] for label in labels)
                    alpha = tuple(word[(phase + 1) % 5] + profile[word[phase]]
                                  for phase in range(5))
                    images[alpha].append(word)
                    direct_words += 1
                gaps = set()
                for words in images.values():
                    for left, right in combinations(words, 2):
                        difference = tuple(second - first for first, second in zip(left, right))
                        gaps.update((difference, tuple(-value for value in difference)))
                graph = shared_gap_words((values,) * 5, profile, labels, scale)
                assert set(graph) == gaps
                if shared_monotone_obstruction((values,) * 5, profile, labels):
                    assert not graph
                for left, right in graph.values():
                    assert shared_word(left, labels) and shared_word(right, labels)
                    assert tuple(left[(phase + 1) % 5] + profile[left[phase]] for phase in range(5)) == tuple(
                        right[(phase + 1) % 5] + profile[right[phase]] for phase in range(5))
                if classes <= 2:
                    assert set(graph) == {(gap,) * 5 for gap in self_gaps}
                    binary_contexts += 1
                contexts += 1
    return dict(partitions=52, contexts=contexts, direct_consistent_words=direct_words,
                binary_contexts=binary_contexts,
                scope='Every five-row equality partition and every shared capped profile on widths zero through three: complete consistent alpha fibers match all constrained gap words, with independently reconstructed collision witnesses. Binary rows reduce exactly to common self-loop gaps.')


def shared_selector_audit():
    limit = 4096
    sequence, _, periods, selected_splits = generate(limit)
    assert sequence == brent_generate(limit)
    fibonacci = fibonacci_values(limit + 1)
    seen = set()
    counts = Counter()
    examples = {}
    network_parameters = {}
    root_windows = []
    for index in range(3, limit + 1):
        if periods[index] != 5:
            continue
        counts['selected_five_roots'] += 1
        order = max(height for height, anchor in enumerate(fibonacci) if anchor <= index) - 1
        trajectory, transient, _ = full_orbit(sequence, index)
        root = canonical_cycle(tuple(point - fibonacci[order] for point in trajectory[transient:]))
        root_windows.append((index, order, root))
        stack = [(order, root)]
        while stack:
            order, offsets = stack.pop()
            if order <= 5 or (order, offsets) in seen:
                continue
            seen.add((order, offsets))
            actual = tuple(selected_splits[fibonacci[order] + offset] - fibonacci[order - 1]
                           for offset in offsets)
            assert shared_word(actual, offsets)
            actual_profile = tuple(sequence[fibonacci[order - 1] + split] - fibonacci[order - 2]
                                   for split in actual)
            actual_alpha = tuple(actual[(phase + 1) % 5] + actual_profile[phase]
                                 for phase in range(5))
            edge_parameters = {}
            for phase, parameter in enumerate(actual_alpha):
                edge = (offsets[phase], offsets[(phase + 1) % 5])
                assert edge_parameters.setdefault(edge, parameter) == parameter
                physical_edge = tuple(fibonacci[order] + offset for offset in edge)
                absolute_parameter = parameter + fibonacci[order]
                assert absolute_parameter == (selected_splits[physical_edge[1]]
                                               + sequence[selected_splits[physical_edge[0]]])
                assert network_parameters.setdefault(physical_edge, absolute_parameter) == absolute_parameter
            counts['parameter_entries_before_sharing'] += 5
            counts['parameter_entries_after_edge_sharing'] += len(edge_parameters)
            stack.extend(((order - 1, actual),
                          (order - 2, tuple(offset - split for offset, split in zip(offsets, actual)))))
            if len(set(offsets)) == 5:
                continue
            sets = candidate_sets(sequence, fibonacci[order], fibonacci[order - 1],
                                  fibonacci[order - 2], fibonacci[order - 3], offsets)
            sets = [tuple(split for split in values
                          if max(0, offset - fibonacci[order - 3]) <= split
                          <= min(offset, fibonacci[order - 2]))
                    for offset, values in zip(offsets, sets)]
            profile = {split: sequence[fibonacci[order - 1] + split] - fibonacci[order - 2]
                       for split in range(max(offsets) + 1)}
            defects = tuple(offset - sequence[fibonacci[order] + offset] + fibonacci[order - 1]
                            for offset in offsets)
            binary_certificate = len(set(offsets)) <= 2 and min(defects) <= 1
            counts['binary_small_defect_certificates'] += binary_certificate
            sign_certificate = shared_monotone_obstruction(sets, profile, offsets)
            counts['monotone_sign_certificates'] += sign_certificate
            counts['sign_certificates_with_a_descending_candidate_row'] += sign_certificate and any(
                profile[first] > profile[second] for values in sets
                for first, second in zip(values, values[1:]))
            fibers = alpha_collision_fibers(sets, profile)
            counts['repeated_contexts'] += 1
            counts['raw_collision_contexts'] += bool(fibers)
            counts['raw_collision_fibers'] += len(fibers)
            counts['raw_collision_pairs'] += sum(math.comb(len(words), 2) for words in fibers.values())
            shared_context = False
            for alpha, words in sorted(fibers.items()):
                retained = [word for word in sorted(words) if shared_word(word, offsets)]
                if binary_certificate or sign_certificate:
                    assert len(retained) <= 1
                counts['consistent_collision_fibers'] += len(retained) > 1
                counts['consistent_collision_pairs'] += math.comb(len(retained), 2)
                shared_context |= len(retained) > 1
                category = str(min(len(retained), 2))
                if category not in examples:
                    graph = shared_gap_words(sets, profile, offsets, sum(defects) // 2)
                    expected_gaps = set()
                    for collision_words in fibers.values():
                        consistent = [word for word in collision_words if shared_word(word, offsets)]
                        for left, right in combinations(consistent, 2):
                            gap = tuple(second - first for first, second in zip(left, right))
                            expected_gaps.update((gap, tuple(-value for value in gap)))
                    assert set(graph) == expected_gaps
                    periodic = [periodic_profile_candidates(values, profile, offset)
                                for values, offset in zip(sets, offsets)]
                    examples[category] = dict(root_index=index, profile_order=order, offsets=list(offsets),
                                              candidate_sets=[list(values) for values in sets],
                                              alpha=list(alpha), raw_fiber=[list(word) for word in sorted(words)],
                                              consistent_fiber=[list(word) for word in retained],
                                              periodic_candidates=[list(values) for values in periodic],
                                              actually_selected_word=list(actual),
                                              complete_consistent_gap_words=[list(word) for word in sorted(graph)])
            counts['consistent_collision_contexts'] += shared_context
    assert counts['raw_collision_pairs'] == 437 and counts['consistent_collision_pairs'] == 3
    assert counts['selected_five_roots'] == 147 and counts['consistent_collision_contexts'] == 2
    offsets = (16, 11, 11, 16, 11)
    order = 9
    sets = candidate_sets(sequence, fibonacci[order], fibonacci[order - 1],
                          fibonacci[order - 2], fibonacci[order - 3], offsets)
    sets = [tuple(split for split in values
                  if max(0, offset - fibonacci[order - 3]) <= split
                  <= min(offset, fibonacci[order - 2]))
            for offset, values in zip(offsets, sets)]
    assert all(len(values) == 4 for values in sets)
    profile = {split: sequence[fibonacci[order - 1] + split] - fibonacci[order - 2]
               for split in range(max(offsets) + 1)}
    assert all(profile[first] <= profile[second] for first, second in zip(sets[1], sets[1][1:]))
    assert shared_gap_words(sets, profile, offsets, 5) == {}
    assert seed_fiber(sets, profile, (15, 15, 16, 15, 16)) == [(9, 8, 8, 9, 8)]
    return dict(prefix_limit=limit, distinct_internal_contexts=len(seen), counts=dict(sorted(counts.items())),
                exhaustive_abstract_check=shared_row_completeness_examples(), witnesses=examples,
                binary_child_at_196=dict(profile_order=order, offsets=list(offsets), defects=[4, 1, 1, 4, 1],
                                         first_child_alpha=[15, 15, 16, 15, 16],
                                         distinct_parent_edges=[[16, 11], [11, 11], [11, 16]],
                                         edge_parameters=[15, 15, 16],
                                         actual_first_child_offsets=[9, 8, 8, 9, 8],
                                         independent_cartesian_words=1024, consistent_words=16,
                                         defect_residue_sufficient_bits=3, consistent_inverse_seed_bits=0),
                cross_window_network=cross_window_network_audit(sequence, selected_splits, fibonacci,
                                                                network_parameters, len(seen)),
                generated_shared_descent=generative_descent_audit(sequence, selected_splits, fibonacci,
                                                                  root_windows),
                scope='Actual recursive descendants of every prescribed period-five orbit through 4096, deduplicated by profile order and aligned offsets. Sharing removes 434 of 437 collision pairs, but three survive in two contexts; none of these counts is an order-uniform theorem or a basin/phase certificate.')


def connected_components(neighbours):
    unseen = set(neighbours)
    result = []
    while unseen:
        start = min(unseen)
        reached = {start}
        stack = [start]
        while stack:
            point = stack.pop()
            for following in neighbours[point] - reached:
                reached.add(following)
                stack.append(following)
        unseen -= reached
        result.append(tuple(sorted(reached)))
    return result


def geometric_split_choices(index, fibonacci, root_cycles):
    order = bisect_right(fibonacci, index) - 1
    offset = index - fibonacci[order]
    lower = fibonacci[order - 1] + max(0, offset - fibonacci[order - 3])
    upper = fibonacci[order - 1] + min(offset, fibonacci[order - 2])
    assert 2 * lower >= index and 11 * (index - upper) >= 3 * index
    choices = range(lower, upper + 1)
    if index in root_cycles:
        choices = tuple(root_cycles[index])
        assert choices and len(set(choices)) == len(choices)
        assert all(lower <= point <= upper for point in choices)
    return choices


def check_generated_cycles(roots, root_cycles, values, splits):
    assert set(root_cycles) <= set(roots)
    for index, cycle in root_cycles.items():
        assert index >= 9 and set(cycle) <= set(roots)
        assert splits[index] in cycle
        assert all(index - values[point] == cycle[(phase + 1) % len(cycle)]
                   for phase, point in enumerate(cycle))


def encode_shared_descent(roots, selectors, fibonacci, root_cycles=None):
    root_cycles = root_cycles or {}
    values = dict(enumerate((0, 1, 1, 2, 3, 3, 4, 5, 5)))
    splits = {}
    chunks = []
    maximum_depth = 0

    def visit(index, depth):
        nonlocal maximum_depth
        maximum_depth = max(maximum_depth, depth)
        assert index >= 1
        if index in values:
            return values[index]
        choices = geometric_split_choices(index, fibonacci, root_cycles)
        split = selectors[index]
        ordinal = choices.index(split)
        width = (len(choices) - 1).bit_length()
        if width:
            chunks.append(format(ordinal, f'0{width}b'))
        splits[index] = split
        values[index] = visit(index - split, depth + 1) + visit(split, depth + 1)
        return values[index]

    for root in roots:
        visit(root, 0)
    check_generated_cycles(roots, root_cycles, values, splits)
    return dict(bits=''.join(chunks), splits=splits, values=values, maximum_depth=maximum_depth)


def decode_shared_descent(roots, bits, fibonacci, root_cycles=None):
    assert set(bits) <= {'0', '1'}
    root_cycles = root_cycles or {}
    values = dict(enumerate((0, 1, 1, 2, 3, 3, 4, 5, 5)))
    splits = {}
    position = 0

    def visit(index):
        nonlocal position
        assert index >= 1
        if index in values:
            return values[index]
        choices = geometric_split_choices(index, fibonacci, root_cycles)
        width = (len(choices) - 1).bit_length()
        assert position + width <= len(bits)
        ordinal = int(bits[position:position + width], 2) if width else 0
        position += width
        assert ordinal < len(choices)
        split = choices[ordinal]
        splits[index] = split
        values[index] = visit(index - split) + visit(split)
        return values[index]

    for root in roots:
        visit(root)
    assert position == len(bits)
    check_generated_cycles(roots, root_cycles, values, splits)
    return dict(splits=splits, values=values)


def unpack_descent_stream(packet):
    width = packet['stream_bits']
    encoded = packet['stream_hex']
    assert len(encoded) == 2 * ((width + 7) // 8)
    value = int(encoded or '0', 16)
    assert value.bit_length() <= width
    return format(value, f'0{width}b') if width else ''


def replay_descent_packet(packet):
    if 'root_cycle_header' in packet:
        root_cycles = {}
        for line in packet['root_cycle_header'].splitlines():
            index, points = line.split(':')
            assert int(index) not in root_cycles
            root_cycles[int(index)] = tuple(map(int, points.split(',')))
        roots = tuple(point for cycle in root_cycles.values() for point in cycle) + tuple(root_cycles)
    else:
        roots = tuple(packet['root_indices'])
        root_cycles = {record[0]: tuple(record[1:]) for record in packet['qualified_root_cycles']}
    fibonacci = fibonacci_values(max(roots) + 1)
    bits = unpack_descent_stream(packet)
    assert hashlib.sha256(bits.encode('ascii')).hexdigest() == packet['stream_sha256']
    return decode_shared_descent(roots, bits, fibonacci, root_cycles)


def shared_descent_bound(roots):
    mass = sum(set(roots))
    threshold = max(8, math.isqrt(11 * mass // 3))
    if 3 * threshold * threshold < 11 * mass:
        threshold += 1
    node_bound = threshold - 8 + 11 * mass // (3 * threshold)
    return dict(total_distinct_root_mass=mass, cutoff=threshold, distinct_internal_bound=node_bound,
                sufficient_bit_bound=node_bound * (max(roots) - 1).bit_length())


def generated_profile_histograms(profile_roots, decoded, fibonacci):
    cache = {}

    def histogram(order, index):
        key = (order, index)
        if key in cache:
            return cache[key]
        offset = index - fibonacci[order]
        assert 0 <= offset <= fibonacci[order - 1]
        if order <= 5:
            counts = [0] * 7
            counts[offset if order == 4 else offset + 3] = 1
        else:
            split = decoded['splits'][index] if index >= 9 else 5
            first = histogram(order - 1, split)
            second = histogram(order - 2, index - split)
            counts = [left + right for left, right in zip(first, second)]
        marked = counts[2] + counts[6]
        assert decoded['values'][index] == fibonacci[order - 1] + offset - marked
        assert sum(counts[:3]) == (1 if order == 4 else fibonacci[order - 5])
        assert sum(counts[3:]) == (0 if order == 4 else fibonacci[order - 4])
        cache[key] = tuple(counts)
        return cache[key]

    roots = [histogram(order, index) for order, index in profile_roots]
    assert len(cache) <= 2 * (len(decoded['splits']) + 6)
    return roots, len(cache)


def complete_shared_layouts(roots, fibonacci):
    def extend(pending, selectors):
        if not pending:
            yield selectors
            return
        index, remainder = pending[-1], pending[:-1]
        if index <= 8 or index in selectors:
            yield from extend(remainder, selectors)
            return
        for split in geometric_split_choices(index, fibonacci, {}):
            yield from extend((*remainder, split, index - split), {**selectors, index: split})

    yield from extend(tuple(reversed(roots)), {})


def generative_descent_completeness(fibonacci):
    root_sets = [(index,) for index in range(9, 31)]
    root_sets.extend(((14, 17, 19, 17, 14), (21, 22, 24, 22, 21), (28, 25, 29, 25, 28)))
    layouts = 0
    profile_cache_nodes = 0
    for roots in root_sets:
        codes = set()
        for selectors in complete_shared_layouts(roots, fibonacci):
            encoded = encode_shared_descent(roots, selectors, fibonacci)
            decoded = decode_shared_descent(roots, encoded['bits'], fibonacci)
            assert decoded['splits'] == selectors == encoded['splits']
            assert decoded['values'] == encoded['values']
            assert encoded['bits'] not in codes
            codes.add(encoded['bits'])
            assert len(selectors) <= shared_descent_bound(roots)['distinct_internal_bound']

            def literal_value(index):
                if index <= 8:
                    return (0, 1, 1, 2, 3, 3, 4, 5, 5)[index]
                split = selectors[index]
                return literal_value(split) + literal_value(index - split)

            assert all(decoded['values'][index] == literal_value(index) for index in roots)
            profile_roots = [(bisect_right(fibonacci, index) - 1, index) for index in roots]
            for order, index in tuple(profile_roots):
                if index == fibonacci[order] and order >= 5:
                    profile_roots.append((order - 1, index))
            _, cache_nodes = generated_profile_histograms(profile_roots, decoded, fibonacci)
            profile_cache_nodes += cache_nodes
            if encoded['bits']:
                try:
                    decode_shared_descent(roots, encoded['bits'][:-1], fibonacci)
                except AssertionError:
                    pass
                else:
                    raise AssertionError('A proper code prefix decoded as a complete layout.')
            try:
                decode_shared_descent(roots, encoded['bits'] + '0', fibonacci)
            except AssertionError:
                pass
            else:
                raise AssertionError('Trailing layout bits were accepted.')
            layouts += 1
        ordered = sorted(codes)
        assert all(not following.startswith(previous) for previous, following in zip(ordered, ordered[1:]))
    return dict(root_sets=len(root_sets), exhaustive_shared_layouts=layouts,
                profile_cache_nodes_checked=profile_cache_nodes,
                scope='Independent iterative enumeration of every reachable shared geometric selector dictionary for roots9..30 and three repeated five-row root sets. Key-free bitstreams biject with dictionaries, agree with literal expanded value trees, reconstruct boundary-alias histograms, are prefix-free and reject truncation/trailing bits.')


def shared_descent_case(roots, selectors, sequence, fibonacci, root_cycles=None):
    encoded = encode_shared_descent(roots, selectors, fibonacci, root_cycles)
    decoded = decode_shared_descent(roots, encoded['bits'], fibonacci, root_cycles)
    assert decoded['values'] == encoded['values'] and decoded['splits'] == encoded['splits']
    assert all(value == sequence[index] for index, value in decoded['values'].items())
    assert all(split == selectors[index] for index, split in decoded['splits'].items())
    bound = shared_descent_bound(roots)
    assert len(decoded['splits']) <= bound['distinct_internal_bound']
    assert len(encoded['bits']) <= bound['sufficient_bit_bound']
    profile_roots = [(bisect_right(fibonacci, index) - 1, index) for index in roots]
    histograms, histogram_nodes = generated_profile_histograms(profile_roots, decoded, fibonacci)
    packet = dict(root_indices=list(roots), root_values=[decoded['values'][index] for index in roots],
                  distinct_internal_indices=len(decoded['splits']), stream_bits=len(encoded['bits']),
                  stream_hex=int(encoded['bits'] or '0', 2).to_bytes((len(encoded['bits']) + 7) // 8, 'big').hex(),
                  stream_sha256=hashlib.sha256(encoded['bits'].encode('ascii')).hexdigest(),
                  maximum_encoding_stack_depth=encoded['maximum_depth'], bound=bound,
                  profile_histogram_nodes=histogram_nodes,
                  marked_counts=[counts[2] + counts[6] for counts in histograms],
                  root_cycle_qualifications=len(root_cycles or {}),
                  qualified_root_cycles=[[index, *cycle] for index, cycle in (root_cycles or {}).items()])
    assert replay_descent_packet(packet) == decoded
    return decoded, packet


def generative_descent_audit(sequence, selectors, fibonacci, root_windows):
    first_index, first_order, first_offsets = root_windows[0]
    first_cycle = tuple(fibonacci[first_order] + offset for offset in first_offsets)
    assert first_index == 196
    _, window_code = shared_descent_case(first_cycle, selectors, sequence, fibonacci)
    _, outer_code = shared_descent_case((*first_cycle, first_index), selectors, sequence, fibonacci,
                                        {first_index: first_cycle})
    root_cycles = {index: tuple(fibonacci[order] + offset for offset in offsets)
                   for index, order, offsets in root_windows}
    roots = tuple(point for cycle in root_cycles.values() for point in cycle) + tuple(root_cycles)
    decoded, combined = shared_descent_case(roots, selectors, sequence, fibonacci, root_cycles)
    combined['root_count'] = len(roots)
    combined['distinct_root_count'] = len(set(roots))
    combined['root_indices_sha256'] = hashlib.sha256(json.dumps(combined.pop('root_indices')).encode()).hexdigest()
    combined['root_values_sha256'] = hashlib.sha256(json.dumps(combined.pop('root_values')).encode()).hexdigest()
    combined['marked_total'] = sum(combined.pop('marked_counts'))
    combined['root_cycle_header'] = '\n'.join(f'{index}:' + ','.join(map(str, cycle))
                                               for index, cycle in root_cycles.items())
    combined.pop('qualified_root_cycles')
    assert replay_descent_packet(combined) == decoded
    contexts = set()
    parameters = {}
    stack = [(order, offsets) for index, order, offsets in root_windows]
    while stack:
        order, offsets = stack.pop()
        if order <= 5 or (order, offsets) in contexts:
            continue
        contexts.add((order, offsets))
        physical = tuple(fibonacci[order] + offset for offset in offsets)
        selected = tuple(decoded['splits'][index] if index >= 9 else 5 for index in physical)
        first = tuple(split - fibonacci[order - 1] for split in selected)
        second = tuple(offset - split for offset, split in zip(offsets, first))
        for phase, index in enumerate(physical):
            target = physical[(phase + 1) % 5]
            value = selected[(phase + 1) % 5] + decoded['values'][selected[phase]]
            assert parameters.setdefault((index, target), value) == value
            assert decoded['values'][index] == (decoded['values'][selected[phase]]
                                                + decoded['values'][index - selected[phase]])
        stack.extend(((order - 1, first), (order - 2, second)))
    forest, _, _ = parameter_forest(parameters)
    assert len(contexts) == 12208 and len(parameters) == 6514 and len(forest) == 2308
    upper_selector = {11: 7}
    upper_payload = encode_shared_descent((11,), upper_selector, fibonacci)
    upper_decoded = decode_shared_descent((11,), upper_payload['bits'], fibonacci)
    assert upper_decoded['values'][11] == 8 != sequence[11]
    qualified_wrong = encode_shared_descent((6, 7, 11), upper_selector, fibonacci, {11: (6, 7)})
    assert qualified_wrong['bits'] == '1' and qualified_wrong['values'][11] == 8
    trajectory, transient, period = full_orbit(sequence, 11)
    assert trajectory[transient:] == [6, 7] and transient == 3 and period == 2
    assert selectors[11] == 6 and sequence[10] == 7
    return dict(small_class_completeness=generative_descent_completeness(fibonacci),
                five_window_at_196=window_code, selected_root_and_cycle_at_196=outer_code,
                combined_root_forest=combined, reconstructed_internal_windows=len(contexts),
                reconstructed_absolute_edges=len(parameters), derived_parameter_forest_entries=len(forest),
                geometry_only_counterexample=dict(index=11, stream=upper_payload['bits'], split=7,
                                                   qualified_cycle_stream=qualified_wrong['bits'],
                                                   decoded_value=8, actual_value=sequence[11],
                                                   actual_prescribed_split=6, actual_cycle=[6, 7],
                                                   transient=3, depth=7, same_prescribed_basin=True),
                scope='Root indices/cycles and first-visit choice bits alone generate the shared descent layout, all encountered values and the earlier parameter network. Decoder uses only Fibonacci arithmetic and the fixed values through8, not a supplied C table or child labels. The structural code includes numeric chosen endpoints; it does not certify their prescribed iteration, basin or phase. General O(sqrt(R)*log(N)) bound includes the generated layout but excludes selected-validity proof costs.')


def parameter_forest(parameters):
    neighbours = defaultdict(set)
    weights = {}
    for (source, target), parameter in sorted(parameters.items()):
        first, second = ('source', source), ('target', target)
        neighbours[first].add(second)
        neighbours[second].add(first)
        weights[first, second] = weights[second, first] = parameter
    potentials = {}
    forest = []
    components = connected_components(neighbours)
    for component in components:
        start = component[0]
        potentials[start] = 0
        stack = [start]
        while stack:
            point = stack.pop()
            for following in sorted(neighbours[point]):
                weight = weights[point, following]
                if following not in potentials:
                    potentials[following] = weight - potentials[point]
                    stack.append(following)
                    source, target = ((point[1], following[1]) if point[0] == 'source'
                                      else (following[1], point[1]))
                    forest.append((source, target, weight))
                else:
                    assert potentials[point] + potentials[following] == weight
    assert len(forest) == len(neighbours) - len(components)
    assert all(potentials['source', source] + potentials['target', target] == parameter
               for (source, target), parameter in parameters.items())
    return forest, potentials, len(components)


def network_gap_classes(successors):
    representatives = {point: point for point in successors}

    def representative(point):
        while representatives[point] != point:
            point = representatives[point]
        return point

    for targets in successors.values():
        target_list = sorted(targets)
        for target in target_list[1:]:
            representatives[representative(target)] = representative(target_list[0])
    return {point: representative(point) for point in representatives}


def network_gap_assignments(component, domains, profile, successors, classes):
    relations = []
    allowed = {}
    for point in component:
        source = classes[point]
        target = classes[min(successors[point])]
        relation = {(second - first, profile[first] - profile[second])
                    for first in domains[point] for second in domains[point]
                    if first != second and profile[first] != profile[second]}
        relations.append((source, target, relation))
        differences = {first for first, second in relation}
        allowed[source] = allowed.get(source, differences) & differences
    answers = []

    def search(candidate):
        candidate = {point: set(values) for point, values in candidate.items()}
        changed = True
        while changed:
            changed = False
            for source, target, relation in relations:
                retained = {(first, second) for first, second in relation
                            if first in candidate[source] and second in candidate[target]
                            and (source != target or first == second)}
                for point, values in ((source, {first for first, second in retained}),
                                      (target, {second for first, second in retained})):
                    following = candidate[point] & values
                    if not following:
                        return
                    changed |= following != candidate[point]
                    candidate[point] = following
        undecided = [point for point in candidate if len(candidate[point]) > 1]
        if not undecided:
            answers.append({point: next(iter(values)) for point, values in candidate.items()})
            return
        point = min(undecided, key=lambda item: (len(candidate[item]), item))
        for value in sorted(candidate[point]):
            search({**candidate, point: {value}})

    search(allowed)
    return answers


def decode_network_seed(component, domains, profile, successors, parameters, start, seed):
    if seed not in domains[start]:
        return None
    assignment = {start: seed}
    stack = [start]
    while stack:
        source = stack.pop()
        for target in sorted(successors[source]):
            value = parameters[source, target] - profile[assignment[source]]
            if value not in domains[target] or (target in assignment and assignment[target] != value):
                return None
            if target not in assignment:
                assignment[target] = value
                stack.append(target)
    assert set(assignment) == set(component)
    return assignment


def cross_window_completeness_examples():
    rank_contexts = 0
    for mask in range(1 << 9):
        edges = [(position // 3, position % 3) for position in range(9) if mask & (1 << position)]
        parameters = {(source, target): 7 * source + 3 * target + 2 for source, target in edges}
        forest, _, _ = parameter_forest(parameters)
        matrix = [[int(source == point) for point in range(3)]
                  + [int(target == point) for point in range(3)] for source, target in edges]
        assert (affine_rank(matrix) if matrix else 0) == len(forest)
        reconstructed = parameter_forest({(source, target): value for source, target, value in forest})[1]
        assert all(reconstructed['source', source] + reconstructed['target', target] == value
                   for (source, target), value in parameters.items())
        rank_contexts += 1
    gap_contexts = 0
    direct_words = 0
    for mask in range(1, 1 << 9):
        edges = [(position // 3, position % 3) for position in range(9) if mask & (1 << position)]
        vertices = sorted({point for edge in edges for point in edge})
        successors = {point: set() for point in vertices}
        for source, target in edges:
            successors[source].add(target)
        if any(not values for values in successors.values()):
            continue
        reached = {vertices[0]}
        stack = [vertices[0]]
        while stack:
            source = stack.pop()
            for target in successors[source] - reached:
                reached.add(target)
                stack.append(target)
        if reached != set(vertices):
            continue
        if any(not any(target == point for source, target in edges) for point in vertices):
            continue
        reverse = {point: {source for source, target in edges if target == point} for point in vertices}
        reverse_reached = {vertices[0]}
        stack = [vertices[0]]
        while stack:
            source = stack.pop()
            for target in reverse[source] - reverse_reached:
                reverse_reached.add(target)
                stack.append(target)
        if reverse_reached != set(vertices):
            continue
        classes = network_gap_classes(successors)
        for profile in product(range(1), range(2), range(3)):
            domains = {point: (0, 1, 2) for point in vertices}
            images = defaultdict(list)
            for values in product(range(3), repeat=len(vertices)):
                assignment = dict(zip(vertices, values))
                image = tuple(assignment[target] + profile[assignment[source]] for source, target in edges)
                images[image].append(assignment)
                direct_words += 1
            expected_gaps = set()
            for words in images.values():
                for left, right in combinations(words, 2):
                    gap = tuple(right[point] - left[point] for point in vertices)
                    assert all(gap)
                    expected_gaps.update((gap, tuple(-value for value in gap)))
            actual = network_gap_assignments(vertices, domains, profile, successors, classes)
            assert {tuple(answer[classes[point]] for point in vertices) for answer in actual} == expected_gaps
            for answer in actual:
                left, right = {}, {}
                for point in vertices:
                    gap, following = answer[classes[point]], answer[classes[min(successors[point])]]
                    left[point], right[point] = next((first, second) for first in domains[point]
                                                   for second in domains[point]
                                                   if second - first == gap
                                                   and profile[first] - profile[second] == following)
                assert all(left[target] + profile[left[source]] == right[target] + profile[right[source]]
                           for source, target in edges)
            for image, assignments in images.items():
                parameters = dict(zip(edges, image))
                decoded = [answer for seed in domains[vertices[0]]
                           if (answer := decode_network_seed(vertices, domains, profile, successors,
                                                              parameters, vertices[0], seed)) is not None]
                assert {tuple(answer[point] for point in vertices) for answer in decoded} == {
                    tuple(answer[point] for point in vertices) for answer in assignments}
            gap_contexts += 1
    return dict(bipartite_rank_contexts=rank_contexts, strongly_connected_profile_contexts=gap_contexts,
                direct_joint_words=direct_words,
                scope='Every subgraph of a 3-by-3 bipartite parameter graph has forest size equal to independently computed rational rank; every strongly connected directed graph on up to three named vertices with small shared capped profiles has exact gap reconstruction and seed decoding checked against complete Cartesian fibers.')


def cross_window_network_audit(sequence, selected_splits, fibonacci, parameters, window_count):
    successors = defaultdict(set)
    neighbours = defaultdict(set)
    for source, target in parameters:
        successors[source].add(target)
        neighbours[source].add(target)
        neighbours[target].add(source)
    components = connected_components(neighbours)
    classes = network_gap_classes(successors)
    domains = {}
    for point in sorted(successors):
        order = max(height for height, anchor in enumerate(fibonacci) if anchor <= point)
        offset = point - fibonacci[order]
        values = candidate_sets(sequence, fibonacci[order], fibonacci[order - 1],
                                fibonacci[order - 2], fibonacci[order - 3], (offset,))[0]
        domains[point] = tuple(fibonacci[order - 1] + value for value in values
                              if max(0, offset - fibonacci[order - 3]) <= value
                              <= min(offset, fibonacci[order - 2]))
        assert selected_splits[point] in domains[point]
    forest, potentials, bipartite_components = parameter_forest(parameters)
    shifts = {}
    for point in successors:
        shift = selected_splits[point] - potentials['target', point]
        assert shifts.setdefault(classes[point], shift) == shift
    assert all(sequence[selected_splits[point]]
               == potentials['source', point] - shifts[classes[min(successors[point])]]
               for point in successors)
    decoded_potentials = parameter_forest({(source, target): value for source, target, value in forest})[1]
    assert all(decoded_potentials['source', source] + decoded_potentials['target', target] == value
               for (source, target), value in parameters.items())
    sign_neighbours = defaultdict(set)
    for source, targets in successors.items():
        values = domains[source]
        if all(sequence[first] <= sequence[second] for first, second in zip(values, values[1:])):
            target = min(targets)
            first, second = classes[source], classes[target]
            sign_neighbours[first].add(second)
            sign_neighbours[second].add(first)
    certificates = []
    for component in components:
        start = min(component, key=lambda point: (len(domains[point]), point))
        reached = {start}
        stack = [start]
        while stack:
            source = stack.pop()
            for target in successors[source] - reached:
                reached.add(target)
                stack.append(target)
        assert reached == set(component)
        fixed = len(domains[start]) == 1
        colours = {}
        odd = False
        for point in sorted({classes[point] for point in component}):
            if point in colours:
                continue
            colours[point] = 0
            stack = [point]
            while stack:
                source = stack.pop()
                for target in sign_neighbours[source]:
                    if target in colours:
                        odd |= colours[source] == colours[target]
                    else:
                        colours[target] = 1 - colours[source]
                        stack.append(target)
        method = 'singleton_domain' if fixed else 'odd_sign_graph' if odd else 'complete_gap_relations'
        if not fixed and not odd:
            assert network_gap_assignments(component, domains, sequence, successors, classes) == []
        fibers = [decoded for seed in domains[start]
                  if (decoded := decode_network_seed(component, domains, sequence, successors,
                                                     parameters, start, seed)) is not None]
        assert len(fibers) == 1
        assert all(fibers[0][point] == selected_splits[point] for point in component)
        certificates.append(dict(minimum_index=min(component), maximum_index=max(component),
                                 physical_indices=len(component), gap_classes=len({classes[point] for point in component}),
                                 method=method, seed_index=start, seed_candidates=len(domains[start]),
                                 actual_parameter_fiber_size=1))
    assert domains[489] == (292,) and parameters[489, 476] == 483
    assert sequence[292] == 197 and selected_splits[476] == 286
    assert len(successors) == 1300 and len(parameters) == 6514 and len(forest) == 2308
    assert len(components) == 37 and bipartite_components == 292
    return dict(aligned_internal_windows=window_count, physical_indices=len(successors),
                alpha_entries_before_sharing=5 * window_count, distinct_absolute_edge_parameters=len(parameters),
                bipartite_components=bipartite_components, forest_parameter_entries=len(forest),
                reconstructed_edge_parameters=len(parameters), reconstructed_row_parameters=5 * window_count,
                gap_classes=len(set(classes.values())), selector_components=len(components),
                component_certificate_methods=dict(Counter(item['method'] for item in certificates)),
                component_certificates=certificates, conditional_joint_inverse_branch_bits=0,
                cross_node_witness=dict(source_index=489, singleton_source_split=292, source_split_value=197,
                                        target_index=476, edge_parameter=483, recovered_target_split=286,
                                        recovered_normalized_offset=53, excluded_local_offsets=[64, 62]),
                independent_completeness=cross_window_completeness_examples(),
                scope='A fixed physical-label layout of the 147 selected five-cycle roots through 4096 and their internal descendants. All 37 joint selector components are injective on the supplied independent canonical geometric/value domains: singleton, sign or complete finite gap certificates cover every parameter image. Forest size is the universal linear parameter rank, not C-specific minimum code size. Layout, profile/domain, basin/phase and validity proof costs remain excluded.')


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


def cyclic_readout_summary(outputs):
    length = len(outputs)
    output_period = next(shift for shift in range(1, length + 1)
                         if length % shift == 0 and all(
                             outputs[position] == outputs[(position + shift) % length]
                             for position in range(length)))
    classes = len(set(outputs))
    horizon = next(depth for depth in range(length) if len({
        tuple(outputs[(position + step) % length] for step in range(depth + 1))
        for position in range(length)}) == output_period)
    assert horizon <= output_period - classes
    labels = tuple(outputs)
    for depth in range(horizon + 1):
        residuals = {tuple(outputs[(position + step) % length] for step in range(depth + 1))
                     for position in range(length)}
        assert len(set(labels)) == len(residuals)
        following = {}
        labels = tuple(following.setdefault((labels[position], labels[(position + 1) % length]),
                                            len(following)) for position in range(length))
    assert len(set(labels)) == output_period
    return output_period, classes, horizon


def split_variance(order, index, split, fibonacci):
    complement = index - split
    mismatch = fibonacci[order - 1] * complement - fibonacci[order - 2] * split
    return Fraction(mismatch * mismatch, index * index * split * complement)


def variance_fiber_audit():
    contexts = 0
    paired_indices = 0
    for first_anchor in range(1, 9):
        for second_anchor in range(1, 9):
            for index in range(3, 26):
                fibers = defaultdict(list)
                for split in range(1, index):
                    complement = index - split
                    mismatch = first_anchor * complement - second_anchor * split
                    value = Fraction(mismatch * mismatch, index * index * split * complement)
                    fibers[value].append(split)
                    partner = Fraction(first_anchor ** 2 * index * complement,
                                       first_anchor ** 2 * complement + second_anchor ** 2 * split)
                    partner_complement = index - partner
                    partner_mismatch = first_anchor * partner_complement - second_anchor * partner
                    assert partner_mismatch ** 2 / (index ** 2 * partner * partner_complement) == value
                assert max(map(len, fibers.values())) <= 2
                for fiber in fibers.values():
                    if len(fiber) == 2:
                        first, second = fiber
                        assert (first_anchor ** 2 * index * (first + second - index)
                                == (first_anchor ** 2 - second_anchor ** 2) * first * second)
                        paired_indices += 1
                contexts += 1
    return dict(positive_anchor_contexts=contexts, equal_variance_pairs=paired_indices,
                scope='Exact integer fibers and rational involution checks; the general two-point fiber bound is proved separately.')


def phase_readout_audit(sequence, selected_splits, fibonacci):
    abstract_words = 0
    for length in range(1, 9):
        for outputs in product(range(3), repeat=length):
            cyclic_readout_summary(outputs)
            abstract_words += 1
    census = Counter()
    variance_census = Counter()
    witnesses = []
    for index in range(3, len(sequence)):
        trajectory, transient, period = full_orbit(sequence, index)
        cycle = canonical_cycle(tuple(trajectory[transient:]))
        outputs = tuple(sequence[point] + sequence[index - point] for point in cycle)
        output_period, classes, horizon = cyclic_readout_summary(outputs)
        census[(period, output_period, classes, horizon)] += 1
        order = bisect_right(fibonacci, index) - 1
        variances = tuple(split_variance(order, index, point, fibonacci) for point in cycle)
        variance_period, variance_classes, variance_horizon = cyclic_readout_summary(variances)
        assert max(Counter(variances).values()) <= 2
        assert variance_period in ({period} if period % 2 else {period, period // 2})
        variance_census[(period, variance_period, variance_classes, variance_horizon)] += 1
        phase = cycle.index(trajectory[transient]) + sequence[index - 1] - transient
        assert outputs[phase % output_period] == sequence[index]
        if index in (11, 196, 1354, 3054, 5980, 46401, 75067):
            point = index - 1
            for iteration in range(sequence[index - 1]):
                point = index - sequence[point]
            assert point == selected_splits[index]
            baseline = fibonacci[order - 1] + index - fibonacci[order]
            witnesses.append(dict(index=index, cycle=list(cycle), outputs=list(outputs),
                                  output_period=output_period, current_output_classes=classes,
                                  minimum_distinguishing_horizon=horizon,
                                  local_variances=[str(value) for value in variances],
                                  variance_output_period=variance_period,
                                  variance_output_classes=variance_classes,
                                  variance_distinguishing_horizon=variance_horizon,
                                  complementary_marked_counts=[baseline - value for value in outputs],
                                  selected_phase=phase % period, selected_value=sequence[index]))
    delayed = next(row for row in witnesses if row['index'] == 3054)
    assert delayed['outputs'] == [2016, 2018, 2018, 2016, 2018]
    assert (delayed['current_output_classes'], delayed['output_period'],
            delayed['minimum_distinguishing_horizon']) == (2, 5, 3)
    return dict(abstract_ternary_output_words=abstract_words,
                selected_indices_inclusive=[3, len(sequence) - 1], witnesses=witnesses,
                selected_cycles_checked=sum(census.values()),
                constant_readout_period_counts={str(period): sum(count for key, count in census.items()
                                                                 if key[:2] == (period, 1))
                                                for period in (1, 2, 3)},
                period_five_census=[dict(current_output_classes=key[2],
                                        distinguishing_horizon=key[3], count=count)
                                   for key, count in sorted(census.items()) if key[0] == 5],
                nonconstant_period_compressions=[dict(orbit_period=key[0], output_period=key[1],
                                                      current_output_classes=key[2], count=count)
                                                 for key, count in sorted(census.items())
                                                 if 1 < key[1] < key[0]],
                variance_fiber_checks=variance_fiber_audit(),
                variance_period_five_census=[dict(current_output_classes=key[2],
                                                 distinguishing_horizon=key[3], count=count)
                                            for key, count in sorted(variance_census.items()) if key[0] == 5],
                variance_period_compressions=[dict(orbit_period=key[0], output_period=key[1],
                                                  current_output_classes=key[2], count=count)
                                             for key, count in sorted(variance_census.items())
                                             if key[1] < key[0]],
                scope='Exact conditional cyclic-output minimum: one current readout has M classes, autonomous future readout has d states, and exact index readout has p states. These are distinct contracts; derived phase arithmetic can remove an independent label. Finite selected-cycle census does not prove that every C five-cycle is nonconstant.')


def phase_free_dispersion_audit(sequence, selected_splits, fibonacci):
    cycles = {}
    qualified = {}
    local_values = {}
    for index in range(fibonacci[6], len(sequence)):
        trajectory, transient, period = full_orbit(sequence, index)
        cycle = tuple(trajectory[transient:])
        assert len(cycle) == period and selected_splits[index] in cycle
        cycles[index] = cycle
        qualified[index] = tuple(point for point in cycle
                                 if sequence[point] + sequence[index - point] == sequence[index])
        assert selected_splits[index] in qualified[index]
    contexts = [(order, index) for order in range(6, len(fibonacci) - 1)
                for index in range(fibonacci[order], min(fibonacci[order + 1], len(sequence) - 1) + 1)]
    for order, index in contexts:
        assert all(fibonacci[order - 1] <= point <= fibonacci[order]
                   and fibonacci[order - 2] <= index - point <= fibonacci[order - 1]
                   for point in cycles[index])
        local_values[(order, index)] = tuple(split_variance(order, index, point, fibonacci)
                                             for point in cycles[index])
    previous = {}
    for steps in range(1, 5):
        current = {}
        for order, index in contexts:
            candidates = []
            value_candidates = []
            actual_value = None
            for point, local in zip(cycles[index], local_values[(order, index)]):
                complement = index - point
                first_values = previous.get((order - 1, point), (Fraction(0),) * 3)
                second_values = previous.get((order - 2, complement), (Fraction(0),) * 3)
                if steps > 1:
                    assert order - 1 <= 5 or (order - 1, point) in previous
                    assert order - 2 <= 5 or (order - 2, complement) in previous
                basin_value = local + Fraction(point, index) * first_values[0] + Fraction(complement, index) * second_values[0]
                candidates.append(basin_value)
                if point in qualified[index]:
                    value_candidates.append(local + Fraction(point, index) * first_values[1]
                                            + Fraction(complement, index) * second_values[1])
                if point == selected_splits[index]:
                    actual_value = (local + Fraction(point, index) * first_values[2]
                                    + Fraction(complement, index) * second_values[2])
            result = min(candidates), min(value_candidates), actual_value
            assert result[0] <= result[1] <= result[2]
            current[(order, index)] = result
        previous = current
    minima = {}
    tested = 0
    for index in range(fibonacci[12], len(sequence)):
        defect = sequence[index] - g_closed(index)
        if not defect:
            continue
        order = bisect_right(fibonacci, index) - 1
        scale = Fraction(defect, index) ** 4
        for name, total in zip(('basin', 'value_qualified', 'actual'), previous[(order, index)]):
            ratio = total / scale
            assert ratio >= 1
            for key in ((name, order), (name, None)):
                if key not in minima or ratio < Fraction(minima[key]['ratio']):
                    minima[key] = dict(index=index, order=order, defect=defect,
                                       variance=str(total), ratio=str(ratio))
        tested += 1
    periodic_limit = 4096
    periodic_points = {index: tuple(point for cycle in all_cycles(sequence, index) for point in cycle)
                       for index in range(fibonacci[6], periodic_limit + 1)}
    @lru_cache(None)
    def periodic_variance(order, index, steps):
        if not steps or order <= 5:
            return Fraction(0)
        return min(split_variance(order, index, point, fibonacci)
                   + Fraction(point, index) * periodic_variance(order - 1, point, steps - 1)
                   + Fraction(index - point, index) * periodic_variance(order - 2, index - point, steps - 1)
                   for point in periodic_points[index])
    comparison = {}
    for index in range(fibonacci[12], periodic_limit + 1):
        defect = sequence[index] - g_closed(index)
        if not defect:
            continue
        order = bisect_right(fibonacci, index) - 1
        scale = Fraction(defect, index) ** 4
        periodic_total = periodic_variance(order, index, 4)
        assert periodic_total <= previous[(order, index)][0]
        for name, total in (('basin', previous[(order, index)][0]), ('all_periodic', periodic_total)):
            ratio = total / scale
            if name not in comparison or ratio < Fraction(comparison[name]['ratio']):
                comparison[name] = dict(index=index, defect=defect, variance=str(total), ratio=str(ratio))
    return dict(indices_inclusive=[fibonacci[12], len(sequence) - 1], positive_defect_roots=tested,
                inherited_closed_block_contexts=len(contexts), generations_checked=4,
                finite_kappa_one_verified=True,
                global_minima={name: minima[(name, None)] for name in ('basin', 'value_qualified', 'actual')},
                per_order_minima=[dict(order=order, **{name: minima[(name, order)]
                                                     for name in ('basin', 'value_qualified', 'actual')})
                                  for order in sorted({key[1] for key in minima if key[1] is not None})],
                all_periodic_comparison=dict(indices_inclusive=[fibonacci[12], periodic_limit], minima=comparison),
                scope='Exact four-generation Bellman lower bounds with prescribed-start basin context supplied. Choices are relaxed per occurrence, not an exact globally shared minimum. All bounds are finite; no uniform dispersion theorem is claimed.')


def four_generation_dispersion_audit(sequence, selected_splits, fibonacci):
    @lru_cache(None)
    def variance(order, index, steps):
        if not steps or order <= 5:
            return Fraction(0)
        first = selected_splits[index]
        second = index - first
        local = split_variance(order, index, first, fibonacci)
        return (local + Fraction(first, index) * variance(order - 1, first, steps - 1)
                + Fraction(second, index) * variance(order - 2, second, steps - 1))

    tested = 0
    zero_defects = 0
    minimum = None
    minimum_row = None
    for index in range(fibonacci[12], len(sequence)):
        order = bisect_right(fibonacci, index) - 1
        defect = sequence[index] - g_closed(index)
        if not defect:
            zero_defects += 1
            continue
        total = variance(order, index, 4)
        ratio = total / Fraction(defect, index) ** 4
        assert ratio >= 1
        if minimum is None or ratio < minimum:
            minimum = ratio
            minimum_row = dict(index=index, order=order, defect=defect,
                               variance=str(total), ratio=str(ratio))
        tested += 1
    arithmetic_fibonacci = fibonacci_values(10 ** 100)

    def upper_value(order, index):
        return (arithmetic_fibonacci[order - 1]
                + min(index - arithmetic_fibonacci[order], arithmetic_fibonacci[order - 2]))

    def rounded_split(index):
        order = bisect_right(arithmetic_fibonacci, index) - 1
        offset = index - arithmetic_fibonacci[order]
        denominator = arithmetic_fibonacci[order]
        candidate = (2 * arithmetic_fibonacci[order - 1] * offset + denominator) // (2 * denominator)
        if (offset <= arithmetic_fibonacci[order - 2]
                and candidate <= arithmetic_fibonacci[order - 3]
                and offset - candidate <= arithmetic_fibonacci[order - 4]):
            split_offset = candidate
        else:
            split_offset = min(arithmetic_fibonacci[order - 2],
                               max(0, offset - arithmetic_fibonacci[order - 4]))
        return arithmetic_fibonacci[order - 1] + split_offset

    @lru_cache(None)
    def abstract_variance(order, index, steps):
        if not steps:
            return Fraction(0)
        first = rounded_split(index)
        second = index - first
        assert arithmetic_fibonacci[order - 1] <= first <= arithmetic_fibonacci[order]
        assert arithmetic_fibonacci[order - 2] <= second <= arithmetic_fibonacci[order - 1]
        assert upper_value(order, index) == upper_value(order - 1, first) + upper_value(order - 2, second)
        mismatch = arithmetic_fibonacci[order - 1] * second - arithmetic_fibonacci[order - 2] * first
        local = Fraction(mismatch * mismatch, index * index * first * second)
        return (local + Fraction(first, index) * abstract_variance(order - 1, first, steps - 1)
                + Fraction(second, index) * abstract_variance(order - 2, second, steps - 1))

    abstract_rows = []
    for order in (20, 30, 40, 60, 90):
        index = arithmetic_fibonacci[order] + arithmetic_fibonacci[order] // 10
        defect = upper_value(order, index) - g_closed(index)
        total = abstract_variance(order, index, 4)
        ratio = total / Fraction(defect, index) ** 4
        abstract_rows.append(dict(order=order, index=index, value=upper_value(order, index),
                                  defect=defect, relative_defect=str(Fraction(defect, index)),
                                  variance=str(total), quartic_ratio=str(ratio)))
    assert Fraction(abstract_rows[-1]['quartic_ratio']) < Fraction(1, 10 ** 29)
    basin_traces = []
    for order in (12, 13, 20, 30, 60, 90):
        anchor = arithmetic_fibonacci[order]
        first_anchor = arithmetic_fibonacci[order - 1]
        second_anchor = arithmetic_fibonacci[order - 2]
        third_anchor = arithmetic_fibonacci[order - 3]
        for offset in sorted({arithmetic_fibonacci[order - 5] + 1,
                              anchor // 10, arithmetic_fibonacci[order - 4]}):
            assert arithmetic_fibonacci[order - 5] + 1 <= offset <= arithmetic_fibonacci[order - 4]
            index = anchor + offset
            trace = [index - 1]
            for iteration in range(8):
                point = trace[-1]
                point_order = bisect_right(arithmetic_fibonacci, point) - 1
                trace.append(index - upper_value(point_order, point))
            assert trace == [index - 1, second_anchor + 1, 2 * second_anchor + offset - 1,
                             second_anchor + offset, 2 * second_anchor, 2 * third_anchor + offset,
                             first_anchor + offset, first_anchor, first_anchor + offset]
            depth = upper_value(order, index - 1)
            assert depth == first_anchor + offset - 1 and depth >= 6
            selected = first_anchor + offset if depth % 2 == 0 else first_anchor
            rounded = rounded_split(index)
            assert first_anchor < rounded < first_anchor + offset
            rounded_complement = first_anchor + offset - (rounded - first_anchor)
            rounded_order = bisect_right(arithmetic_fibonacci, rounded) - 1
            complement_order = bisect_right(arithmetic_fibonacci, rounded_complement) - 1
            assert index - upper_value(rounded_order, rounded) == rounded_complement
            assert index - upper_value(complement_order, rounded_complement) == rounded
            if offset == anchor // 10:
                basin_traces.append(dict(order=order, index=index, offset=offset, trace=trace,
                                         depth=depth, prescribed_split=selected, rounded_split=rounded,
                                         rounded_cycle=sorted({rounded, rounded_complement})))
    variance.cache_clear()
    return dict(actual_indices_inclusive=[fibonacci[12], len(sequence) - 1],
                positive_defect_roots_checked=tested, zero_defect_roots=zero_defects,
                exact_finite_kappa_one_verified=True, minimum_quartic_ratio=minimum_row,
                abstract_rounded_upper_cap_examples=abstract_rows,
                upper_cap_prescribed_basin_traces=basin_traces,
                one_step_formula='(F_(j-1)*(N-a)-F_(j-2)*a)^2/(N^2*a*(N-a))',
                scope='Exact finite support for the proposed actual-C quartic dispersion inequality, not a uniform proof or decay exponent. Rounded proportional upper-cap descent is an explicit geometric counterfamily with nonvanishing relative defect and vanishing four-generation variance; it is not the nested C recurrence.')


def additive_policy_audit(sequence, selected_splits, fibonacci):
    greedy = {}
    extremes = {}
    complete_domains = {}
    probes = 0
    complete_candidates = 0
    for index in range(fibonacci[6], len(sequence)):
        order = bisect_right(fibonacci, index) - 1
        lower = max(fibonacci[order - 1], index - fibonacci[order - 1])
        upper = min(fibonacci[order], index - fibonacci[order - 2])
        left = lower
        while left <= upper and sequence[left] + sequence[index - left] != sequence[index]:
            left += 1
        assert left <= upper
        right = upper
        while right >= lower and sequence[right] + sequence[index - right] != sequence[index]:
            right -= 1
        assert right >= lower
        assert left <= selected_splits[index] <= right
        probes += left - lower + upper - right + 2
        extremes[index] = left, right
        greedy[index] = max({left, right}, key=lambda point: (
            split_variance(order, index, point, fibonacci), point))
        if index <= 4096:
            candidates = tuple(point for point in range(lower, upper + 1)
                               if sequence[point] + sequence[index - point] == sequence[index])
            assert extremes[index] == (candidates[0], candidates[-1])
            assert split_variance(order, index, greedy[index], fibonacci) == max(
                split_variance(order, index, point, fibonacci) for point in candidates)
            complete_domains[index] = candidates
            complete_candidates += len(candidates)
    @lru_cache(None)
    def policy_variance(order, index, steps, optimal=False):
        if not steps or order <= 5:
            return Fraction(0)
        candidates = complete_domains[index] if optimal else (greedy[index],)
        assert all(fibonacci[order - 1] <= point <= fibonacci[order]
                   and fibonacci[order - 2] <= index - point <= fibonacci[order - 1]
                   and sequence[point] + sequence[index - point] == sequence[index]
                   for point in candidates)
        return max(split_variance(order, index, point, fibonacci)
                   + Fraction(point, index) * policy_variance(order - 1, point, steps - 1, optimal)
                   + Fraction(index - point, index) * policy_variance(order - 2, index - point, steps - 1, optimal)
                   for point in candidates)
    minima = {}
    tested = 0
    witnesses = []
    optimal_roots = 0
    for index in range(fibonacci[12], len(sequence)):
        defect = sequence[index] - g_closed(index)
        if not defect:
            continue
        order = bisect_right(fibonacci, index) - 1
        for steps in (1, 2, 3, 4):
            total = policy_variance(order, index, steps)
            for power in (2, 4):
                ratio = total / Fraction(defect, index) ** power
                key = steps, power
                if key not in minima or ratio < Fraction(minima[key]['ratio']):
                    minima[key] = dict(index=index, order=order, defect=defect,
                                       split=greedy[index], variance=str(total), ratio=str(ratio))
        if index <= 4096:
            optimal = policy_variance(order, index, 4, True)
            assert optimal >= policy_variance(order, index, 4)
            optimal_roots += 1
            ratio = optimal / Fraction(defect, index) ** 4
            key = 'optimal4', 4
            if key not in minima or ratio < Fraction(minima[key]['ratio']):
                minima[key] = dict(index=index, order=order, defect=defect,
                                   variance=str(optimal), ratio=str(ratio))
        if index in (185, 191, 3054, 4590, 5980, 18785, 125952):
            point = greedy[index]
            trajectory, transient, _ = full_orbit(sequence, index)
            periodic_points = {point for cycle in all_cycles(sequence, index) for point in cycle}
            witnesses.append(dict(index=index, value=sequence[index], defect=defect,
                                  extreme_candidates=list(extremes[index]), greedy_split=point,
                                  child_values=[sequence[point], sequence[index - point]],
                                  actual_split=selected_splits[index],
                                  in_prescribed_cycle=point in trajectory[transient:],
                                  is_periodic=point in periodic_points,
                                  one_step_variance=str(policy_variance(order, index, 1)),
                                  four_step_variance=str(policy_variance(order, index, 4))))
        tested += 1
    policy_variance.cache_clear()
    arithmetic_fibonacci = fibonacci_values(10 ** 100)
    unique_knees = []
    for order in range(6, 17):
        anchor = arithmetic_fibonacci[order]
        first_anchor = arithmetic_fibonacci[order - 1]
        second_anchor = arithmetic_fibonacci[order - 2]
        third_anchor = arithmetic_fibonacci[order - 3]
        fourth_anchor = arithmetic_fibonacci[order - 4]
        admitted = [offset for offset in range(max(0, second_anchor - third_anchor), second_anchor + 1)
                    if min(offset, third_anchor) + min(second_anchor - offset, fourth_anchor) == second_anchor]
        assert admitted == [third_anchor]
        unique_knees.append(dict(order=order, index=anchor + second_anchor,
                                 unique_split=first_anchor + third_anchor))
    @lru_cache(None)
    def upper_knee_variance(order, steps):
        if not steps:
            return Fraction(0)
        index = arithmetic_fibonacci[order] + arithmetic_fibonacci[order - 2]
        first = arithmetic_fibonacci[order - 1] + arithmetic_fibonacci[order - 3]
        second = arithmetic_fibonacci[order - 2] + arithmetic_fibonacci[order - 4]
        mismatch = arithmetic_fibonacci[order - 1] * second - arithmetic_fibonacci[order - 2] * first
        assert abs(mismatch) == 1 and first + second == index
        return (split_variance(order, index, first, arithmetic_fibonacci)
                + Fraction(first, index) * upper_knee_variance(order - 1, steps - 1)
                + Fraction(second, index) * upper_knee_variance(order - 2, steps - 1))
    counterexamples = []
    for order in (20, 30, 40, 60, 90):
        index = arithmetic_fibonacci[order] + arithmetic_fibonacci[order - 2]
        value = arithmetic_fibonacci[order]
        defect = value - g_closed(index)
        total = upper_knee_variance(order, 4)
        counterexamples.append(dict(order=order, index=index, value=value,
                                    relative_defect=str(Fraction(defect, index)),
                                    maximal_four_step_variance=str(total),
                                    quartic_ratio=str(total / Fraction(defect, index) ** 4)))
    assert Fraction(counterexamples[-1]['quartic_ratio']) < Fraction(1, 10 ** 60)
    return dict(indices_inclusive=[fibonacci[12], len(sequence) - 1], positive_defect_roots=tested,
                endpoint_probes=probes, greedy_generations=[1, 2, 3, 4],
                greedy_ratio_minima=[dict(generations=steps, defect_power=power, **minima[(steps, power)])
                                     for steps in (1, 2, 3, 4) for power in (2, 4)],
                finite_greedy_four_step_quadratic_kappa_one_verified=Fraction(minima[(4, 2)]['ratio']) >= 1,
                full_domain_audit=dict(indices_inclusive=[fibonacci[6], 4096],
                                       admissible_splits=complete_candidates,
                                       optimal_four_step_positive_roots=optimal_roots,
                                       minimum_optimal_quartic_ratio=minima[('optimal4', 4)]),
                witnesses=witnesses, upper_cap_unique_split_knees=unique_knees,
                upper_cap_maximal_dispersion_counterexamples=counterexamples,
                scope='Additive value-preserving policies need neither basin nor prescribed phase. Endpoint monotonicity certifies a greedy local maximum; full Bellman optimization is separate. Finite greedy quadratic support is not a global rate or an actual-selected dispersion theorem. Upper-cap knees refute automatic maximal dispersion from geometric and terminal premises alone.')


def proportional_guard_split(index, fibonacci, golden=None):
    order = bisect_right(fibonacci, index) - 1
    anchor = fibonacci[order]
    first_anchor = fibonacci[order - 1]
    lower = max(first_anchor, index - first_anchor)
    upper = min(anchor, index - fibonacci[order - 2])
    center = first_anchor * index // anchor
    candidates = {max(lower, min(upper, center)), max(lower, min(upper, center + 1))}
    golden_value = g_closed if golden is None else golden.__getitem__
    admitted = [point for point in candidates
                if golden_value(point) + golden_value(index - point) >= golden_value(index)]
    assert admitted
    split = min(admitted, key=lambda point: (abs(first_anchor * index - anchor * point), -point))
    assert abs(first_anchor * index - anchor * split) <= anchor
    return split


def collar_threshold(cutoff_order, offset, negative=False):
    width = 6 if negative else 29
    depth = 0
    while 2 ** depth * offset > width * 3 ** depth:
        depth += 1
    return cutoff_order + int(negative) + 2 * depth


def proportional_extension_audit(sequence):
    limit = 1048576
    fibonacci = fibonacci_values(limit + 1)
    golden = [g_closed(index) for index in range(limit + 1)]
    equality_set = {11, 24, 25, 59}
    for order in range(2, len(fibonacci)):
        equality_set.update((fibonacci[order], fibonacci[order] + 1))
        if order % 2:
            equality_set.add(fibonacci[order] - 1)
    carry_contexts = 0
    for index in range(3, 4097):
        for point in range(1, index - 1):
            first = golden[point] + golden[index - point] - golden[index]
            second = golden[point + 1] + golden[index - point - 1] - golden[index]
            assert first >= 0 or second >= 0
            carry_contexts += 1
    cases = []
    for cutoff_order in (25, 26):
        cutoff = fibonacci[cutoff_order]
        values = sequence[:cutoff + 1]
        first_difference = None
        for index in range(cutoff + 1, limit + 1):
            order = bisect_right(fibonacci, index) - 1
            anchor, first_anchor, second_anchor = fibonacci[order], fibonacci[order - 1], fibonacci[order - 2]
            split = proportional_guard_split(index, fibonacci, golden)
            complement = index - split
            assert first_anchor <= split <= anchor and second_anchor <= complement <= first_anchor
            offset = index - anchor
            first_offset, second_offset = split - first_anchor, complement - second_anchor
            assert first_offset + second_offset == offset
            assert 3 * first_offset <= 2 * offset + 3 and 3 * second_offset <= 2 * offset + 3
            gap = fibonacci[order + 1] - index
            first_gap, second_gap = anchor - split, first_anchor - complement
            assert first_gap + second_gap == gap
            assert 3 * first_gap <= 2 * gap + 6 and 3 * second_gap <= 2 * gap + 6
            value = values[split] + values[complement]
            values.append(value)
            assert golden[index] <= value <= first_anchor + min(offset, second_anchor)
            assert 22877 * value <= 15225 * index
            assert value - first_anchor >= min(offset, 32)
            assert (value == golden[index]) == (index in equality_set)
            if index < len(sequence) and first_difference is None and value != sequence[index]:
                first_difference = dict(index=index, extension_value=value, actual_value=sequence[index],
                                        extension_split=split, child_values=[values[split], values[complement]])
        positive_checks = 0
        negative_checks = 0
        for order in range(23, len(fibonacci)):
            for offset in range(65):
                index = fibonacci[order] + offset
                if index <= limit and (offset <= 32 or order >= collar_threshold(cutoff_order, offset)):
                    assert values[index] == fibonacci[order - 1] + offset
                    positive_checks += 1
            for gap in range(14):
                index = fibonacci[order] - gap
                if 1 <= index <= limit and (gap <= 12 or order >= collar_threshold(cutoff_order, gap, True)):
                    assert values[index] == fibonacci[order - 1]
                    negative_checks += 1
        index = first_difference['index']
        plateau_order = cutoff_order + 1
        outside_gap = 2 * plateau_order // 3 - 2
        plateau_index = fibonacci[plateau_order] - outside_gap
        plateau_split = proportional_guard_split(plateau_index, fibonacci)
        plateau_complement = plateau_index - plateau_split
        plateau_child_gaps = [fibonacci[cutoff_order] - plateau_split,
                             fibonacci[cutoff_order - 1] - plateau_complement]
        assert plateau_split <= cutoff and plateau_complement <= cutoff
        assert sum(plateau_child_gaps) == outside_gap
        assert all(0 <= gap <= 2 * (cutoff_order - 1) // 3 - 3 for gap in plateau_child_gaps)
        plateau_actual = sequence
        if plateau_index >= len(plateau_actual):
            plateau_actual, _, _, _ = generate(plateau_index)
            assert plateau_actual == brent_generate(plateau_index)
        assert values[plateau_index] == fibonacci[cutoff_order] > plateau_actual[plateau_index]
        moving_plateau_violation = dict(order=plateau_order, gap=outside_gap, index=plateau_index,
                                       extension_value=values[plateau_index], actual_value=plateau_actual[plateau_index],
                                       split=plateau_split, child_gaps=plateau_child_gaps)
        point = index - 1
        for iteration in range(values[index - 1]):
            point = index - values[point]
        nested_value = values[point] + values[index - point]
        assert nested_value == sequence[index] != values[index]
        trajectory, transient, period = full_orbit(values, index)
        alternative = first_difference['extension_split']
        alternative_points = []
        alternative_positions = {}
        cursor = alternative
        while cursor not in alternative_positions:
            alternative_positions[cursor] = len(alternative_points)
            alternative_points.append(cursor)
            cursor = index - values[cursor]
        first_difference.update(prescribed_depth=values[index - 1], prescribed_split=point,
                                nested_value=nested_value, prescribed_cycle=list(trajectory[transient:]),
                                transient=transient, period=period,
                                alternative_transient=alternative_positions[cursor],
                                alternative_cycle=alternative_points[alternative_positions[cursor]:],
                                alternative_in_prescribed_cycle=alternative in trajectory[transient:])
        large_fibonacci = fibonacci_values(10 ** 100)
        previous_order = cutoff_order - 2
        current_order = cutoff_order - 1
        previous_index = large_fibonacci[previous_order] + large_fibonacci[previous_order - 2]
        current_index = large_fibonacci[current_order] + large_fibonacci[current_order - 2]
        previous_value, current_value = values[previous_index], values[current_index]
        seed_values = [previous_value, current_value]
        seed_defects = [previous_value - golden[previous_index], current_value - golden[current_index]]
        assert min(seed_defects) > 0
        knees = []
        for order in range(cutoff_order, 91):
            previous_value, current_value = current_value, previous_value + current_value
            index = large_fibonacci[order] + large_fibonacci[order - 2]
            split = proportional_guard_split(index, large_fibonacci)
            assert split == large_fibonacci[order - 1] + large_fibonacci[order - 3]
            assert g_closed(index) == split
            if index <= limit:
                assert values[index] == current_value
            if order in (cutoff_order, cutoff_order + 1, 30, 40, 60, 90):
                knees.append(dict(order=order, index=index, value=current_value,
                                  defect=current_value - g_closed(index), ratio=str(Fraction(current_value, index))))
        cases.append(dict(cutoff_order=cutoff_order, identical_actual_prefix_inclusive=[1, cutoff],
                          extension_checked_inclusive=[cutoff + 1, limit], first_nested_failure=first_difference,
                          exact_zero_set_verified=True, saturated_width=32,
                          positive_collar_checks=positive_checks, negative_collar_checks=negative_checks,
                          moving_plateau_violation=moving_plateau_violation,
                          knee_seed_orders=[previous_order, current_order], knee_seed_indices=[previous_index, current_index],
                          knee_seed_values=seed_values, knee_seed_defects=seed_defects, arithmetic_knees=knees))
    moving_plateau_contexts = []
    for cutoff_order in range(26, 91):
        outside_gap = 2 * (cutoff_order + 1) // 3 - 2
        index = large_fibonacci[cutoff_order + 1] - outside_gap
        split = proportional_guard_split(index, large_fibonacci)
        child_gaps = [large_fibonacci[cutoff_order] - split,
                      large_fibonacci[cutoff_order - 1] - (index - split)]
        minimum_width = 2 * (cutoff_order - 1) // 3 - 3
        assert sum(child_gaps) == outside_gap
        assert 3 * max(child_gaps) <= 2 * outside_gap + 6
        assert max(child_gaps) <= minimum_width
        if cutoff_order in (26, 30, 40, 60, 90):
            moving_plateau_contexts.append(dict(cutoff_order=cutoff_order, index=index,
                                               gap=outside_gap, child_gaps=child_gaps,
                                               minimum_actual_seed_width=minimum_width))
    return dict(consecutive_carry_contexts=carry_contexts, concrete_extensions=cases,
                moving_plateau_exclusion_cutoff_orders_inclusive=[26, 90],
                moving_plateau_exclusion_arithmetic_witnesses=moving_plateau_contexts,
                upper_envelope='15225/22877 for N>=16384; any certified actual C envelope is inherited when F_(J-2) is beyond its threshold',
                scope='Written infinite extensions agree with arbitrarily late actual prefixes, have G/cap/zero-set/saturation/eventual-fixed-collar structure but positive knee defect density and nonconvergent ratios. The new exact moving top-plateau law excludes every cutoff J>=26 at the first subsequent complete block; arithmetic checks through order90 corroborate that infinite exclusion. Numeric cases J25/J26 corroborate through2^20. These are not the actual nested C sequence; excluding this counterfamily does not prove uniform dispersion.')


def unbounded_defect_audit():
    sequence, _, _, selected_splits = generate(131071)
    assert sequence == brent_generate(131071)
    fibonacci = fibonacci_values(131072)
    knees = []
    knee_codes = []
    for order in range(22, 26):
        index = fibonacci[order] + fibonacci[order - 2]
        cost = fibonacci[order] - sequence[index]
        lower = (fibonacci[order - 3] + 2) // 3
        assert sequence[index] * 3 <= 2 * index
        assert cost >= lower
        knees.append(dict(profile_order=order, index=index, defect=cost, lower_bound=lower))
        _, code = shared_descent_case((index,), selected_splits, sequence, fibonacci)
        assert code['marked_counts'] == [cost]
        knee_codes.append(code)
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
    return dict(knee_examples=knees, generated_knee_codes=knee_codes, all_cycle_centre_examples=centres,
                selected_phase_readouts=phase_readout_audit(sequence, selected_splits, fibonacci),
                four_generation_dispersion=four_generation_dispersion_audit(sequence, selected_splits, fibonacci),
                phase_free_dispersion=phase_free_dispersion_audit(sequence, selected_splits, fibonacci),
                additive_dispersion_policies=additive_policy_audit(sequence, selected_splits, fibonacci),
                proportional_extensions=proportional_extension_audit(sequence),
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
        "shared_physical_selector_consistency": shared_selector_audit(),
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

"""Exact checks for the generic reflection-window closure interface."""

from bisect import bisect_right
from fractions import Fraction
import hashlib
import json
from pathlib import Path

from conway_explore import brent_generate, generate


def zero(size):
    return (Fraction(0),) * size


def add(left, right):
    return tuple(a + b for a, b in zip(left, right))


def sub(left, right):
    return tuple(a - b for a, b in zip(left, right))


def scale(value, factor):
    return tuple(factor * a for a in value)


def variable(size, index):
    result = list(zero(size))
    result[index] = Fraction(1)
    return tuple(result)


def alternating(values):
    result = zero(len(values[0]))
    for index, value in enumerate(values):
        result = add(result, scale(value, Fraction(1 if index % 2 == 0 else -1)))
    return result


def rank(rows):
    if not rows:
        return 0
    matrix = [list(row) for row in rows]
    height, width = len(matrix), len(matrix[0])
    pivot = 0
    for column in range(width):
        candidate = next((row for row in range(pivot, height)
                          if matrix[row][column]), None)
        if candidate is None:
            continue
        matrix[pivot], matrix[candidate] = matrix[candidate], matrix[pivot]
        divisor = matrix[pivot][column]
        matrix[pivot] = [entry / divisor for entry in matrix[pivot]]
        for row in range(height):
            if row == pivot or not matrix[row][column]:
                continue
            factor = matrix[row][column]
            matrix[row] = [a - factor * b
                           for a, b in zip(matrix[row], matrix[pivot])]
        pivot += 1
        if pivot == height:
            break
    return pivot


def build_payload(period):
    size = period + 1
    t = variable(size, 0)
    start = variable(size, 1)
    defects = [variable(size, 2 + index) for index in range(period - 1)]
    offsets = [start]
    for index in range(period - 1):
        offsets.append(add(sub(t, offsets[-1]), defects[index]))
    last_defect = sub(add(start, offsets[-1]), t)
    defects.append(last_defect)
    closure = add(sub(t, offsets[-1]), last_defect)
    return t, offsets, defects, closure


def check_period(period):
    t, offsets, defects, closure = build_payload(period)
    size = period + 1
    assert closure == offsets[0]
    for index in range(period):
        next_offset = offsets[(index + 1) % period]
        transition = add(sub(t, offsets[index]), defects[index])
        assert transition == next_offset
    alternating_defects = alternating(defects)
    if period % 2:
        assert scale(offsets[0], 2) == add(t, alternating_defects)
    else:
        assert alternating_defects == zero(size)
    features = [t, *offsets, *defects]
    assert rank(features) == size
    return {
        "period": period,
        "payload_dimension_including_scale": size,
        "additional_coordinates_beyond_scale": period,
        "alternating_defect_identity": "fixed-point" if period % 2 else "translation",
        "feature_rank": rank(features),
    }


def canonical_fib_word(number):
    fibonacci = [0, 1]
    while fibonacci[-1] <= number:
        fibonacci.append(sum(fibonacci[-2:]))
    digits = {}
    remaining = number
    for order in range(len(fibonacci) - 1, 1, -1):
        if fibonacci[order] <= remaining:
            digits[order] = 1
            remaining -= fibonacci[order]
    assert remaining == 0
    assert all(order + 1 not in digits for order in digits)
    patterns = {(0, 0, 0): 0, (1, 0, 0): 1, (0, 1, 0): 2,
                (0, 0, 1): 3, (1, 0, 1): 4}
    windows = tuple(patterns[tuple(digits.get(3 * position + offset, 0)
                                  for offset in (3, 4, 5))]
                    for position in range(max(digits, default=0) // 3 - 1, -1, -1))
    return digits.get(2, 0), windows


def fib_horner(windows):
    digit_vectors = ((0, 0), (1, 0), (0, 1), (1, 1), (2, 1))
    first = second = 0
    for symbol in windows:
        digit = digit_vectors[symbol]
        first, second = first + 2 * second + digit[0], 2 * first + 3 * second + digit[1]
    return first, second


def ternary_level_number(number):
    if number <= 0 or number % 5:
        return False
    remaining = number // 5
    while remaining % 3 == 0:
        remaining //= 3
    return remaining == 1


def scale_memory_audit():
    def multiply(left, right):
        return (left[0] * right[0] + 5 * left[1] * right[1],
                left[0] * right[1] + left[1] * right[0])

    def inverse(value):
        norm = value[0] ** 2 - 5 * value[1] ** 2
        assert norm
        return value[0] / norm, -value[1] / norm

    def positive(value):
        real, radical = value
        if not radical:
            return real > 0
        if real >= 0 and radical > 0:
            return True
        if real <= 0 and radical < 0:
            return False
        return (real ** 2 > 5 * radical ** 2 if real > 0
                else 5 * radical ** 2 > real ** 2)

    def absolute(value):
        return value if positive(value) else scale(value, -1)

    def projection(vector, contracting=False):
        value = (Fraction(vector[0]) + Fraction(3, 2) * vector[1],
                 Fraction(2, 5) * vector[0] + Fraction(7, 10) * vector[1])
        return sub((Fraction(2 * vector[0] + 3 * vector[1]), Fraction(0)), value) if contracting else value

    unity = (Fraction(1), Fraction(0))
    expanding = [unity]
    contracting = [unity]
    for exponent in range(104):
        expanding.append(multiply(expanding[-1], (Fraction(2), Fraction(1))))
        contracting.append(multiply(contracting[-1], (Fraction(2), Fraction(-1))))
    for symbol in range(1, 5):
        vector = fib_horner((symbol,))
        assert not positive(sub(unity, projection(vector)))
        assert positive(sub(scale(unity, 8), projection(vector)))
        assert positive(sub(unity, absolute(projection(vector, True))))

    canonical_checks = 32768
    for number in range(canonical_checks):
        unit, windows = canonical_fib_word(number)
        first, second = fib_horner(windows)
        assert number == unit + 2 * first + 3 * second
        assert not windows or windows[0]

    literal_sequence = [0, 1]
    for number in range(2, 4097):
        point = number - 1
        for iteration in range(literal_sequence[number - 1]):
            point = number - literal_sequence[point]
        literal_sequence.append(point)
    assert all((5 * value == 2 * number) == ternary_level_number(number)
               for number, value in enumerate(literal_sequence[1:], 1))

    words = []
    number = 5
    while True:
        unit, windows = canonical_fib_word(number)
        if len(windows) > 24:
            break
        words.append((number, unit, windows))
        number *= 3
    assert {len(windows) for number, unit, windows in words} == set(range(1, 25))
    cuts = 0
    examples = []
    for number, unit, windows in words:
        for start in range(len(windows)):
            for length in range(1, len(windows) - start + 1):
                prefix = windows[:start]
                block = windows[start:start + length]
                suffix = windows[start + length:]
                suffix_length = len(suffix)
                prefix_vector, block_vector, suffix_vector = map(fib_horner, (prefix, block, suffix))
                expanding_block = multiply(projection(block_vector), inverse(sub(expanding[length], unity)))
                contracting_block = multiply(projection(block_vector, True), inverse(sub(contracting[length], unity)))
                leading = multiply(expanding[suffix_length], add(projection(prefix_vector), expanding_block))
                constant = sub(sub((Fraction(unit + 2 * suffix_vector[0] + 3 * suffix_vector[1]), Fraction(0)),
                                   multiply(expanding[suffix_length], expanding_block)),
                               multiply(contracting[suffix_length], contracting_block))
                alternating_term = multiply(contracting[suffix_length],
                                            add(projection(prefix_vector, True), contracting_block))
                assert positive(leading)
                assert not positive(sub(expanding[suffix_length], multiply(leading, expanding[1])))
                assert not positive(sub(absolute(constant), scale(expanding[suffix_length], 11)))
                assert positive(sub(scale(unity, 4), absolute(alternating_term)))
                assert not positive(sub(add(absolute(constant), absolute(alternating_term)), scale(leading, 64)))
                repetitions = 2 + (length + 5) // length
                pumped_values = []
                for count in (0, 1, repetitions, repetitions + 1):
                    pumped = prefix + block * count + suffix
                    first, second = fib_horner(pumped)
                    value = unit + 2 * first + 3 * second
                    spectral = add(add(multiply(leading, expanding[count * length]), constant),
                                   multiply(alternating_term, contracting[count * length]))
                    assert spectral == (Fraction(value), Fraction(0))
                    if count >= repetitions:
                        pumped_values.append(value)
                ratio = (Fraction(pumped_values[1], pumped_values[0]), Fraction(0))
                gap = absolute(sub(ratio, expanding[length]))
                assert positive(sub(scale(inverse(expanding[length]), Fraction(1, 16)), gap))
                assert not all(map(ternary_level_number, pumped_values))
                assert len(windows) + repetitions * length <= len(windows) + 3 * length + 5
                cuts += 1
                if number == 45 and start == 0:
                    examples.append(dict(number=number, block_length=length, repetitions=repetitions,
                                         pumped_values=pumped_values,
                                         pumped_window_lengths=[len(windows) + (repetitions - 1) * length,
                                                                len(windows) + repetitions * length]))

    tries = []
    for horizon in (1, 2, 4, 8, 16, 24):
        transitions = [{}]
        accepted = set()
        for number, unit, windows in words:
            if len(windows) > horizon:
                continue
            state = 0
            for symbol in (*windows, 5 + unit):
                if symbol not in transitions[state]:
                    transitions[state][symbol] = len(transitions)
                    transitions.append({})
                state = transitions[state][symbol]
            accepted.add(state)
        assert len(transitions) + 1 <= 2 * (horizon + 1) ** 2 + 2
        tries.append(dict(window_horizon=horizon, accepted_words=len(accepted),
                          trie_states_including_reject=len(transitions) + 1,
                          proved_state_lower_bound=max(1, (horizon - 1) // 4)))
        if horizon == 8:
            for number in range(canonical_checks):
                unit, windows = canonical_fib_word(number)
                state = 0
                for symbol in (*windows, 5 + unit):
                    state = transitions[state].get(symbol, -1) if state >= 0 else -1
                assert (state in accepted) == ternary_level_number(number)
    return dict(canonical_numbers_checked=canonical_checks,
                independent_literal_Campbell_level_set_inclusive=[1, 4096],
                power_words_checked=len(words), all_window_lengths_checked=[1, 24],
                all_window_block_cuts_checked=cuts,
                exact_spectral_and_ratio_checks=True, pumping_examples=examples, tries=tries,
                general_state_bound='L<=4K+4 for autonomous DFA or NFA recognition of canonical FIB words for5*3^k through L windows',
                memory_order='Theta(log L)=Theta(log log N) for the scalar diagnostic and nondeterministic Campbell graph recognition; context clocks and read-only table size are separate',
                scope='Written general proof supplies the infinite lower bound; exact finite arithmetic and canonical/trie checks corroborate it. No matching deterministic full-graph decoder or actual Cloitre graph lower bound is claimed.')


def cloitre_top_plateau_memory_audit():
    prefix = (4, 2)
    fooling_rows = []
    crossed_words = 0
    for count in (3, 4, 8, 16, 32, 64):
        base_windows = (8 * (count + 1) - 1).bit_length()
        base_order = 3 * base_windows + 3
        base_width = 2 * base_windows - 1
        fibonacci = [0, 1]
        while len(fibonacci) <= base_order + 6 * count:
            fibonacci.append(sum(fibonacci[-2:]))
        assert base_width + 4 * count < fibonacci[base_order - 2]
        suffixes = [canonical_fib_word(fibonacci[base_order] - base_width - 4 * column)
                    for column in range(count + 1)]
        assert all(len(windows) == base_windows for unit, windows in suffixes)
        for row in range(count + 1):
            for column, (unit, windows) in enumerate(suffixes):
                gap = base_width + 4 * column
                order = base_order + 6 * row
                number = fibonacci[order] - gap
                expected = prefix * row + windows
                assert canonical_fib_word(number) == (unit, expected)
                first, second = fib_horner(expected)
                assert unit + 2 * first + 3 * second == number
                assert (gap <= 2 * order // 3 - 3) == (row >= column)
                crossed_words += 1
        fooling_rows.append(dict(pairs=count + 1, base_order=base_order,
                                base_windows=base_windows, horizon_windows=base_windows + 2 * count))
    for horizon in range(12, 513):
        count = horizon // 4
        base_windows = (8 * (count + 1) - 1).bit_length()
        assert base_windows + 2 * count <= horizon
    fibonacci = [0, 1]
    while len(fibonacci) <= 27:
        fibonacci.append(sum(fibonacci[-2:]))
    actual, _, _, _ = generate(fibonacci[15] - 1)
    assert actual == brent_generate(fibonacci[15] - 1)
    trie_rows = []
    actual_contract_checks = 0
    for horizon in range(1, 9):
        numbers = {1, 4}
        for order in range(6, 3 * horizon + 4):
            numbers.update(fibonacci[order] - gap for gap in range(1, 2 * order // 3 - 2))
        words = set()
        prefixes = {()}
        for number in numbers:
            unit, windows = canonical_fib_word(number)
            assert len(windows) <= horizon
            word = windows + (5 + unit,)
            words.add(word)
            prefixes.update(word[:length] for length in range(1, len(word) + 1))
        assert len(numbers) <= (3 * horizon + 3) ** 2 + 2
        assert len(prefixes) + 1 <= (horizon + 1) * ((3 * horizon + 3) ** 2 + 2) + 2
        if horizon <= 4:
            for number in range(1, fibonacci[3 * horizon + 3]):
                unit, windows = canonical_fib_word(number)
                highest = max(order for order in range(2, len(fibonacci)) if fibonacci[order] <= number)
                assert ((windows + (5 + unit,)) in words) == (actual[number] == fibonacci[highest])
                actual_contract_checks += 1
        trie_rows.append(dict(horizon_windows=horizon, accepted_words=len(words), states_including_reject=len(prefixes) + 1))
    return dict(prefix_window_symbols=list(prefix), fooling_pair_cases=fooling_rows,
                exact_crossed_words=crossed_words, explicit_horizon_bounds_checked_inclusive=[12, 512],
                autonomous_DFA_NFA_state_bound='K>=floor(L/4)+1 for L>=12',
                minimum_nonuniform_state_bit_order='Theta(log L)=Theta(log log N); N=F_(3L+3)-1',
                prefix_trie_examples=trie_rows, small_actual_contract_checks=actual_contract_checks,
                small_actual_evaluators_agree_through=fibonacci[15] - 1,
                scope='Written moving-plateau theorem identifies the actual C cap language. Prefix (25,3) raises the anchor order by6 at a fixed gap; its triangular fooling set gives the general NFA/DFA lower bound. A polynomial-size finite-horizon trie matches the state-bit order, excluding table size and supplied clocks. The actual C full graph inherits a lower bound by a constant-state cap filter/projection; its matching upper bound and the complete recursive minimum remain open.')


def synchronous_fib_word(numbers):
    rows = [canonical_fib_word(number) for number in numbers]
    width = len(rows[0][1])
    assert all(len(windows) <= width for unit, windows in rows)
    padded = [(0,) * (width - len(windows)) + windows for unit, windows in rows]
    return tuple(zip(*padded)) + (('unit', *(unit for unit, windows in rows)),)


def graph_trie(words):
    transitions = [{}]
    accepting = set()
    for word in sorted(words, key=repr):
        state = 0
        for symbol in word:
            if symbol not in transitions[state]:
                transitions[state][symbol] = len(transitions)
                transitions.append({})
            state = transitions[state][symbol]
        accepting.add(state)
    return transitions, accepting


def trie_accepts(trie, word):
    transitions, accepting = trie
    state = 0
    for symbol in word:
        if symbol not in transitions[state]:
            return False
        state = transitions[state][symbol]
    return state in accepting


def highest_input_cap_filter(word):
    patterns = ((0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 0, 1), (1, 0, 1))
    found_highest = False
    for symbol in word:
        if symbol[0] == 'unit':
            bit_pairs = ((symbol[1], symbol[2]),)
        else:
            bit_pairs = zip(reversed(patterns[symbol[0]]), reversed(patterns[symbol[1]]))
        for input_bit, output_bit in bit_pairs:
            expected = int(not found_highest and input_bit == 1)
            if output_bit != expected:
                return False
            found_highest = found_highest or input_bit == 1
    return found_highest


def cloitre_bounded_cap_graph_audit():
    fibonacci = [0, 1]
    while len(fibonacci) <= 150:
        fibonacci.append(sum(fibonacci[-2:]))
    limit = fibonacci[21] - 1
    actual, _, _, splits = generate(limit)
    assert actual == brent_generate(limit)
    caps = (0, 1, 2, 3, 4, 8)
    rows = []
    pair_checks = split_checks = projection_checks = 0
    closure_checks = completed_projection_checks = incorrect_completed_outputs = 0
    qualified_roots = set()
    for horizon in range(1, 7):
        maximum = fibonacci[3 * horizon + 3] - 1
        for cap in caps:
            numbers = [number for number in range(1, maximum + 1)
                       if 0 <= fibonacci[bisect_right(fibonacci, number) - 1] - actual[number] <= cap]
            pair_words = {synchronous_fib_word((number, actual[number])) for number in numbers}
            split_words = {synchronous_fib_word((number, actual[number], splits[number]))
                           for number in numbers if number >= 3}
            pair_trie = graph_trie(pair_words)
            split_trie = graph_trie(split_words)
            assert len(pair_words) == len(numbers)
            assert len(split_words) == len([number for number in numbers if number >= 3])
            for trie, words in ((pair_trie, pair_words), (split_trie, split_words)):
                assert all(trie_accepts(trie, word) for word in words)
                assert len(trie[0]) + 1 <= 2 + (horizon + 1) * len(words)
            if cap:
                bound = 20 + sum(min(fibonacci[order - 2], cap *
                                     (13 if order == 9 else (order - 2) ** 2 // 3 - 3 * order + 30))
                                 for order in range(9, 3 * horizon + 4))
                assert len(numbers) <= bound <= 20 + cap * (3 * horizon + 3) ** 3
            projected = {word for word in pair_words if highest_input_cap_filter(word)}
            for number in range(1, maximum + 1):
                highest = bisect_right(fibonacci, number) - 1
                expected = actual[number] == fibonacci[highest]
                word = synchronous_fib_word((number, fibonacci[highest]))
                assert (word in projected) == expected
                projection_checks += 1
            if horizon <= 3:
                for number in range(1, maximum + 1):
                    for output in range(maximum + 1):
                        if len(canonical_fib_word(output)[1]) > len(canonical_fib_word(number)[1]):
                            continue
                        word = synchronous_fib_word((number, output))
                        expected = number in numbers and output == actual[number]
                        assert trie_accepts(pair_trie, word) == expected
                        assert highest_input_cap_filter(word) == (output == fibonacci[bisect_right(fibonacci, number) - 1])
                        pair_checks += 1
            if horizon <= 2:
                for number in range(3, maximum + 1):
                    for output in range(number + 1):
                        for endpoint in range(number + 1):
                            word = synchronous_fib_word((number, output, endpoint))
                            expected = number in numbers and output == actual[number] and endpoint == splits[number]
                            assert trie_accepts(split_trie, word) == expected
                            split_checks += 1
            qualified_roots.update(number for number in numbers if number >= 3)
            completed_numbers = set(numbers) | set(range(1, min(55, maximum) + 1))
            completed_numbers.update(anchor for anchor in fibonacci[2:] if anchor <= maximum)
            completed_pair_words = {synchronous_fib_word((number, actual[number])) for number in completed_numbers}
            completed_split_words = {synchronous_fib_word((number, actual[number], splits[number]))
                                     for number in completed_numbers if number >= 3}
            completed_pair_trie = graph_trie(completed_pair_words)
            completed_split_trie = graph_trie(completed_split_words)
            assert len(completed_numbers) <= len(numbers) + 55 + 3 * horizon + 1
            for trie, words in ((completed_pair_trie, completed_pair_words),
                                (completed_split_trie, completed_split_words)):
                assert all(trie_accepts(trie, word) for word in words)
                assert len(trie[0]) + 1 <= 2 + (horizon + 1) * len(words)
            completed_projected = {word for word in completed_pair_words if highest_input_cap_filter(word)}
            for number in range(1, maximum + 1):
                highest = bisect_right(fibonacci, number) - 1
                word = synchronous_fib_word((number, fibonacci[highest]))
                assert (word in completed_projected) == (actual[number] == fibonacci[highest])
                completed_projection_checks += 1
            for number in sorted(completed_numbers):
                for output in (actual[number] - 1, actual[number] + 1):
                    if output <= number:
                        assert not trie_accepts(completed_pair_trie, synchronous_fib_word((number, output)))
                        incorrect_completed_outputs += 1
                if number >= 3:
                    assert splits[number] in completed_numbers
                    assert number - splits[number] in completed_numbers
                    closure_checks += 1
                    for endpoint in (splits[number] - 1, splits[number] + 1):
                        assert not trie_accepts(completed_split_trie,
                                                synchronous_fib_word((number, actual[number], endpoint)))
                        incorrect_completed_outputs += 1
            qualified_roots.update(number for number in completed_numbers if number >= 3)
            rows.append(dict(horizon_windows=horizon, cap=cap, accepted_inputs=len(numbers),
                             value_graph_states_including_reject=len(pair_trie[0]) + 1,
                             selected_split_graph_states_including_reject=len(split_trie[0]) + 1,
                             recursively_completed_inputs=len(completed_numbers),
                             completed_value_graph_states_including_reject=len(completed_pair_trie[0]) + 1,
                             completed_selected_split_graph_states_including_reject=len(completed_split_trie[0]) + 1))
    literal_updates = 0
    for number in sorted(qualified_roots):
        endpoint = number - 1
        for step in range(actual[number - 1]):
            endpoint = number - actual[endpoint]
            literal_updates += 1
        assert endpoint == splits[number]
        assert actual[number] == actual[endpoint] + actual[number - endpoint]
    aliases = []
    for order in range(3, 21):
        number = fibonacci[order]
        natural_defect = fibonacci[order] - actual[number]
        assert natural_defect == fibonacci[order - 2] > 0
        aliases.append(dict(order=order, index=number, natural_cap_defect=natural_defect))
    forced_anchors = []
    for order in range(6, 22):
        number = fibonacci[order] - 1
        endpoint = fibonacci[order - 1] - 1
        assert actual[number] == fibonacci[order - 1]
        assert splits[number] == endpoint
        assert number - endpoint == fibonacci[order - 2]
        natural_child_defect = fibonacci[order - 2] - actual[number - endpoint]
        assert natural_child_defect == fibonacci[order - 4]
        forced_anchors.append(dict(root_order=order, zero_cap_root=number,
                                   selected_split=endpoint, forced_anchor=number - endpoint,
                                   forced_anchor_natural_cap_defect=natural_child_defect))
    high_filter_checks = 0
    for order in range(3, 151):
        for number in (fibonacci[order] - 1, fibonacci[order], fibonacci[order] + 1):
            highest = bisect_right(fibonacci, number) - 1
            for output in (0, fibonacci[highest] - 1, fibonacci[highest], fibonacci[highest] + 1):
                if len(canonical_fib_word(output)[1]) > len(canonical_fib_word(number)[1]):
                    continue
                assert highest_input_cap_filter(synchronous_fib_word((number, output))) == (output == fibonacci[highest])
                high_filter_checks += 1
    return dict(cap_levels=list(caps), horizon_windows_inclusive=[1, 6],
                independent_evaluators_agree_through=limit, trie_examples=rows,
                exhaustive_value_output_checks=pair_checks, exhaustive_selected_split_checks=split_checks,
                zero_cap_projection_checks=projection_checks, endpoint_aliases=aliases,
                recursively_completed_child_checks=closure_checks,
                completed_zero_cap_projection_checks=completed_projection_checks,
                incorrect_completed_output_checks=incorrect_completed_outputs,
                zero_cap_roots_forcing_anchor_completion=forced_anchors,
                literal_selected_roots=len(qualified_roots), literal_endpoint_updates=literal_updates,
                high_order_filter_checks=high_filter_checks, highest_filter_order=150,
                minimum_nonuniform_DFA_NFA_state_bit_order='Theta(log L) for every fixed cap, both value and actual selected-split graphs, including the least recursive completion by Fibonacci anchors and the declared base1..55',
                general_state_bounds='Omega(L) below; O(m L^4) above for m>=1; O(L^3) above for m=0',
                scope='The infinite theorem uses the proved quadratic cap enclosure and zero-plateau fooling set; additive child cap conservation and forced anchor children identify the least recursive completion. Finite tries test actual graphs, incorrect outputs, literal selected endpoints, recursive child closure and constant-state cap filtering. Table storage and construction, streaming decoding, full unbounded-cap graph and full recursive minimum remain separate.')


def main():
    rows = [check_period(period) for period in range(1, 9)]
    five = rows[4]
    assert five["payload_dimension_including_scale"] == 6
    assert five["additional_coordinates_beyond_scale"] == 5
    assert rows[1]["alternating_defect_identity"] == "translation"
    dimensions = {f"p={row['period']}": row["payload_dimension_including_scale"]
                  for row in rows}
    additional = {f"p={row['period']}": row["additional_coordinates_beyond_scale"]
                  for row in rows}
    ranks = {f"p={row['period']}": row["feature_rank"] for row in rows}
    print(json.dumps({
        "status": "passed",
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "evaluator_source_sha256": hashlib.sha256(Path(__file__).with_name('conway_explore.py').read_bytes()).hexdigest(),
        "periods_checked": [row["period"] for row in rows],
        "payload_dimension_including_scale": dimensions,
        "additional_coordinates_beyond_scale": additional,
        "feature_rank": ranks,
        "five_window_payload": {
            "input": ["t", "u0", "e0", "e1", "e2", "e3"],
            "derived": ["u1", "u2", "u3", "u4", "e4"],
            "additional_coordinates_beyond_scale": five["additional_coordinates_beyond_scale"],
        },
        "Campbell_FIB_scale_memory": scale_memory_audit(),
        "Cloitre_top_plateau_FIB_memory": cloitre_top_plateau_memory_audit(),
        "Cloitre_bounded_cap_graph_FIB_memory": cloitre_bounded_cap_graph_audit(),
        "scope": "Exact symbolic affine closure; branch inequalities and family-specific selectors remain separate.",
    }, indent=2))


if __name__ == "__main__":
    main()

"""Independent exact experiments for Cloitre's variable-depth Conway recurrence."""

import argparse
from collections import Counter
from fractions import Fraction
import hashlib
import json
from math import isqrt
from pathlib import Path


SUPPLIED_PREFIX = [
    1, 1, 2, 3, 3, 4, 5, 5, 6, 7, 7, 8, 8, 9, 10,
    11, 12, 12, 13, 13, 13, 14, 15, 15, 16, 18, 19, 19, 20, 20,
]


def full_orbit(prefix, index):
    positions = {}
    trajectory = []
    argument = index - 1
    while argument not in positions:
        assert 1 <= argument < index
        positions[argument] = len(trajectory)
        trajectory.append(argument)
        argument = index - prefix[argument]
    preperiod = positions[argument]
    return trajectory, preperiod, len(trajectory) - preperiod


def generate(limit):
    sequence = [0, 1, 1]
    preperiods = [0, 0, 0]
    periods = [0, 0, 0]
    splits = [0, 0, 0]
    for index in range(3, limit + 1):
        trajectory, preperiod, period = full_orbit(sequence, index)
        depth = sequence[index - 1]
        position = depth if depth < len(trajectory) else preperiod + (depth - preperiod) % period
        split = trajectory[position]
        value = sequence[split] + sequence[index - split]
        assert 2 <= value < index
        sequence.append(value)
        preperiods.append(preperiod)
        periods.append(period)
        splits.append(split)
    return sequence, preperiods, periods, splits


def literal_generate(limit):
    sequence = [0, 1, 1]
    updates = 0
    for index in range(3, limit + 1):
        argument = index - 1
        for iteration in range(sequence[index - 1]):
            assert 1 <= argument < index
            argument = index - sequence[argument]
            updates += 1
        sequence.append(sequence[argument] + sequence[index - argument])
    return sequence, updates


def brent_generate(limit):
    sequence = [0, 1, 1]
    for index in range(3, limit + 1):
        power = period = 1
        tortoise = index - 1
        hare = index - sequence[index - 1]
        while tortoise != hare:
            if power == period:
                tortoise = hare
                power *= 2
                period = 0
            hare = index - sequence[hare]
            period += 1
        tortoise = hare = index - 1
        for iteration in range(period):
            hare = index - sequence[hare]
        preperiod = 0
        while tortoise != hare:
            tortoise = index - sequence[tortoise]
            hare = index - sequence[hare]
            preperiod += 1
        depth = sequence[index - 1]
        steps = depth if depth < preperiod else preperiod + (depth - preperiod) % period
        argument = index - 1
        for iteration in range(steps):
            argument = index - sequence[argument]
        sequence.append(sequence[argument] + sequence[index - argument])
    return sequence


def envelope_certificate(sequence, lower):
    upper = 8 * lower - 1
    assert upper < len(sequence)
    minimum_index = lower
    maximum_index = lower
    for index in range(lower + 1, upper + 1):
        if sequence[index] * minimum_index < sequence[minimum_index] * index:
            minimum_index = index
        if sequence[index] * maximum_index > sequence[maximum_index] * index:
            maximum_index = index
    lower_ratio = Fraction(sequence[minimum_index], minimum_index)
    upper_ratio = Fraction(sequence[maximum_index], maximum_index)
    assert all(lower_ratio.numerator * index <= lower_ratio.denominator * sequence[index]
               and upper_ratio.denominator * sequence[index] <= upper_ratio.numerator * index
               for index in range(lower, upper + 1))
    return dict(
        seed_interval_inclusive=[lower, upper],
        lower_numerator=lower_ratio.numerator, lower_denominator=lower_ratio.denominator,
        upper_numerator=upper_ratio.numerator, upper_denominator=upper_ratio.denominator,
        lower_witness=dict(index=minimum_index, value=sequence[minimum_index]),
        upper_witness=dict(index=maximum_index, value=sequence[maximum_index]),
        all_seed_inequalities_verified=True,
        universal_domain=f'all n >= {lower}, by the written finite-window propagation lemma',
    )


def hofstadter_g(limit):
    sequence = [0]
    for index in range(1, limit + 1):
        sequence.append(index - sequence[sequence[index - 1]])
    return sequence


def g_closed(index):
    shifted = index + 1
    return (isqrt(5 * shifted * shifted) - shifted) // 2


def grytczuk(limit):
    sequence = [0, 1, 1]
    for index in range(3, limit + 1):
        split = sequence[sequence[index - 1]]
        sequence.append(sequence[split] + sequence[index - split])
    return sequence


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--limit', type=int, default=1048576)
    parser.add_argument('--literal-limit', type=int, default=4096)
    parser.add_argument('--output', type=Path)
    arguments = parser.parse_args()
    assert 30 <= arguments.literal_limit <= arguments.limit
    sequence, preperiods, periods, splits = generate(arguments.limit)
    literal, updates = literal_generate(arguments.literal_limit)
    assert sequence[:len(literal)] == literal
    assert sequence == brent_generate(arguments.limit)
    assert sequence[1:31] == SUPPLIED_PREFIX
    reference = hofstadter_g(arguments.limit)
    assert all(value == g_closed(index) for index, value in enumerate(reference))
    related = grytczuk(arguments.limit)
    fibonacci = [0, 1]
    while fibonacci[-1] <= arguments.limit + 1:
        fibonacci.append(sum(fibonacci[-2:]))
    fibonacci_neighbors = {value + offset for value in fibonacci for offset in (-1, 0, 1)}
    equalities = [index for index in range(1, arguments.limit + 1) if sequence[index] == reference[index]]
    blocks = []
    for exponent in range(2, arguments.limit.bit_length()):
        lower, upper = 2 ** (exponent - 1), 2 ** exponent
        histogram = Counter(periods[lower + 1:upper + 1])
        period_witness = max(range(lower + 1, upper + 1), key=periods.__getitem__)
        transient_witness = max(range(lower + 1, upper + 1), key=preperiods.__getitem__)
        ratio_witness = max(range(lower + 1, upper + 1), key=lambda index: Fraction(sequence[index], index))
        blocks.append(dict(
            lower_exclusive=lower, upper_inclusive=upper,
            max_cycle=periods[period_witness], max_cycle_first_index=period_witness,
            mean_cycle_numerator=sum(periods[lower + 1:upper + 1]), denominator=upper - lower,
            mean_cycle=sum(periods[lower + 1:upper + 1]) / (upper - lower),
            max_preperiod=preperiods[transient_witness], max_preperiod_first_index=transient_witness,
            cycles_above_two=sum(count for period, count in histogram.items() if period > 2),
            fraction_above_two=sum(count for period, count in histogram.items() if period > 2) / (upper - lower),
            max_ratio_numerator=sequence[ratio_witness], max_ratio_denominator=ratio_witness,
            max_ratio=sequence[ratio_witness] / ratio_witness,
            cycle_histogram=dict(sorted(histogram.items())),
        ))
    differences = [sequence[index] - sequence[index - 1] for index in range(2, min(131072, arguments.limit) + 1)]
    fibonacci_checks = [dict(
        fibonacci_index=position, index=index, expected=fibonacci[position - 1],
        actual=sequence[index], split=splits[index], preperiod=preperiods[index], period=periods[index],
    ) for position, index in enumerate(fibonacci) if position >= 2 and index <= arguments.limit]
    envelope_seeds = [3] + [2 ** exponent for exponent in range(3, arguments.limit.bit_length() - 2)]
    envelope_certificates = [envelope_certificate(sequence, lower) for lower in envelope_seeds
                             if 8 * lower - 1 <= arguments.limit]
    split_bound_failures = [index for index in range(4, arguments.limit + 1)
                            if 8 * min(splits[index], index - splits[index]) < index + 3]
    assert not split_bound_failures
    small_exceptions = [dict(index=index, conway=sequence[index], g=reference[index],
                            split=splits[index], split_values=[sequence[splits[index]], sequence[index-splits[index]]])
                        for index in equalities if index not in fibonacci_neighbors]
    expected_equalities = {11, 24, 25, 59}
    for position, value in enumerate(fibonacci):
        if position >= 2:
            expected_equalities.update((value, value + 1))
        if position >= 3 and position % 2:
            expected_equalities.add(value - 1)
    expected_equalities = {index for index in expected_equalities if 1 <= index <= arguments.limit}
    pair_failures = [dict(first=first, second=second, value=sequence[first] + sequence[second],
                          g_at_sum=g_closed(first + second))
                     for position, first in enumerate(equalities) for second in equalities[position:]
                     if sequence[first] + sequence[second] < g_closed(first + second)]
    depth_failures = [index for index in range(3, arguments.limit + 1)
                      if sequence[index - 1] < preperiods[index]]
    assert not depth_failures
    small_orbit_checks = [dict(index=index, depth=sequence[index - 1], preperiod=preperiods[index],
                              period=periods[index]) for index in range(3, min(52, arguments.limit) + 1)]
    witness_indices = {row['max_cycle_first_index'] for row in blocks
                       if row['upper_inclusive'] in (1024, 16384, 262144, 1048576)}
    witnesses = []
    for index in sorted(witness_indices):
        trajectory, preperiod, period = full_orbit(sequence, index)
        witnesses.append(dict(index=index, depth=sequence[index - 1], trajectory=trajectory,
                              preperiod=preperiod, period=period, selected_split=splits[index],
                              result=sequence[index]))
    report = dict(
        status='finite exact computation; envelope certificates imply universal bounds via the separate written lemma; G/Fibonacci remain conjectural; no Lean validation',
        definition='C(1)=C(2)=1; g=T_n^C(n-1)(n-1); C(n)=C(g)+C(n-g); T_n(x)=n-C(x)',
        limit=arguments.limit, literal_limit=arguments.literal_limit,
        literal_updates=updates, literal_agrees=True, supplied_prefix_agrees=True,
        independent_brent_limit=arguments.limit, independent_brent_agrees=True,
        first_80=sequence[1:81],
        sequence_sha256=hashlib.sha256(','.join(map(str, sequence[1:])).encode('ascii')).hexdigest(),
        g_lower_bound_failure_count=sum(sequence[index] < reference[index] for index in range(1, arguments.limit + 1)),
        g_lower_bound_first_failures=[index for index in range(1, arguments.limit + 1) if sequence[index] < reference[index]][:20],
        equality_indices=equalities,
        equality_count_through_2_17=sum(index <= 131072 for index in equalities),
        equality_outside_fibonacci_neighbors=[index for index in equalities if index not in fibonacci_neighbors],
        equality_exception_details=small_exceptions,
        refined_equality_set_symmetric_difference=sorted(set(equalities) ^ expected_equalities),
        pair_g_inequality=dict(argument_limit=arguments.limit, zero_defect_pairs_checked=len(equalities) * (len(equalities) + 1) // 2,
                               failures=pair_failures,
                               justification='C >= G checked on prefix; G(a)+G(b) >= G(a+b)-1 from the floor formula, so only two zero-defect arguments can fail'),
        fibonacci_checks=fibonacci_checks,
        fibonacci_identity_failures=[row for row in fibonacci_checks if row['actual'] != row['expected']],
        difference_range_through_2_17=[min(differences), max(differences)],
        grytczuk_first_disagreement=next((dict(index=index, conway=sequence[index], grytczuk=related[index]) for index in range(1, arguments.limit + 1) if sequence[index] != related[index]), None),
        blocks=blocks,
        envelope_certificates=envelope_certificates,
        split_bound_failure_count=len(split_bound_failures),
        depth_before_cycle_failure_count=len(depth_failures),
        small_orbit_checks=small_orbit_checks,
        orbit_witnesses=witnesses,
        source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    )
    rendered = json.dumps(report, indent=2) + '\n'
    if arguments.output:
        arguments.output.write_text(rendered)
    print(rendered)


if __name__ == '__main__':
    main()

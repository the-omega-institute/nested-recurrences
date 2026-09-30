"""Exact finite audit of Fibonacci landing and shifted depth recurrences."""

import argparse
from array import array
from collections import Counter
import hashlib
import json
from math import log2, sqrt
from pathlib import Path
import sys

from conway_explore import brent_generate, full_orbit, g_closed


def generate_compact(limit, start_shift=1, depth_shift=1):
    sequence = array('I', [0, 1, 1])
    for index in range(3, limit + 1):
        positions = {}
        trajectory = []
        argument = index - start_shift
        while argument not in positions:
            assert 1 <= argument < index
            positions[argument] = len(trajectory)
            trajectory.append(argument)
            argument = index - sequence[argument]
        preperiod = positions[argument]
        period = len(trajectory) - preperiod
        depth = sequence[index - depth_shift]
        position = depth if depth < len(trajectory) else preperiod + (depth - preperiod) % period
        split = trajectory[position]
        sequence.append(sequence[split] + sequence[index - split])
        if index % 1048576 == 0:
            print(f'L={start_shift}, D={depth_shift}: {index} terms', file=sys.stderr, flush=True)
    return sequence


def literal_family(limit, start_shift, depth_shift):
    sequence = [0, 1, 1]
    for index in range(3, limit + 1):
        argument = index - start_shift
        for iteration in range(sequence[index - depth_shift]):
            argument = index - sequence[argument]
        sequence.append(sequence[argument] + sequence[index - argument])
    return sequence


def digest_sequence(sequence):
    digest = hashlib.sha256()
    for start in range(1, len(sequence), 65536):
        if start > 1:
            digest.update(b',')
        digest.update(','.join(map(str, sequence[start:start + 65536])).encode('ascii'))
    return digest.hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--limit', type=int, default=14930352)
    parser.add_argument('--family-limit', type=int, default=1048576)
    parser.add_argument('--output', type=Path)
    arguments = parser.parse_args()
    assert __debug__ and 6765 <= arguments.limit < 2**32
    assert 4096 <= arguments.family_limit <= arguments.limit
    fibonacci = [0, 1]
    while fibonacci[-1] <= arguments.limit + 1:
        fibonacci.append(sum(fibonacci[-2:]))
    zero_set = {11, 24, 25, 59}
    for order, value in enumerate(fibonacci):
        if order >= 2:
            zero_set.update((value, value + 1))
        if order >= 3 and order % 2:
            zero_set.add(value - 1)
    sequence = generate_compact(arguments.limit)
    independent_limit = min(arguments.limit, 1048576)
    assert list(sequence[:independent_limit + 1]) == brent_generate(independent_limit)
    baseline = json.loads(Path(__file__).with_name('conway-results.json').read_text())
    if arguments.limit >= baseline['limit']:
        assert digest_sequence(sequence[:baseline['limit'] + 1]) == baseline['sequence_sha256']
    equalities = []
    negative_defects = []
    delta_counts = Counter()
    landing_counts = Counter()
    negative_carry_landings = []
    corrected_landing_failures = []
    for index in range(1, len(sequence)):
        defect = sequence[index] - g_closed(index)
        if defect == 0:
            equalities.append(index)
        if defect < 0:
            negative_defects.append(index)
        if index < 3 or index > arguments.family_limit:
            continue
        trajectory, preperiod, period = full_orbit(sequence, index)
        depth = sequence[index - 1]
        position = depth if depth < len(trajectory) else preperiod + (depth - preperiod) % period
        first = trajectory[position]
        second = index - first
        first_defect = sequence[first] - g_closed(first)
        second_defect = sequence[second] - g_closed(second)
        delta = g_closed(first) + g_closed(second) - g_closed(index)
        assert delta in (-1, 0, 1)
        assert defect == first_defect + second_defect + delta
        delta_counts[delta] += 1
        zero_count = (first_defect == 0) + (second_defect == 0)
        if zero_count:
            landing_counts[f'zero_arguments={zero_count},delta={delta}'] += 1
            if delta == -1:
                negative_carry_landings.append(dict(index=index, split=[first, second],
                    defects=[first_defect, second_defect], result_defect=defect))
                if defect != 0:
                    corrected_landing_failures.append(index)
    fibonacci_audit = []
    for order, index in enumerate(fibonacci):
        if order < 6 or index > arguments.limit:
            continue
        center, base, radius = fibonacci[order - 1], fibonacci[order - 2], fibonacci[order - 4]
        trajectory, preperiod, period = full_orbit(sequence, index)
        distances = [value - center for value in trajectory]
        neighborhood_failures = []
        symmetric_two_cycles = []
        for offset in range(1, radius + 1):
            positive = sequence[center + offset] - base
            negative = sequence[center - offset] - base
            if not (0 <= positive <= offset and -offset <= negative <= 0):
                neighborhood_failures.append([offset, positive, negative])
            if positive == offset and negative == -offset:
                symmetric_two_cycles.append(offset)
        fibonacci_audit.append(dict(order=order, index=index, value=sequence[index],
            predecessor_value=sequence[index - 1], expected_value=center,
            preperiod=preperiod, period=period, distances=distances,
            first_three_match=distances[:3] == [base - 1, -fibonacci[order - 3], radius],
            alternating=all(first * second < 0 for first, second in zip(distances, distances[1:]) if second),
            nonincreasing_magnitudes=all(abs(second) <= abs(first) for first, second in zip(distances, distances[1:])),
            neighborhood_radius=radius, neighborhood_failures=neighborhood_failures,
            symmetric_two_cycles=symmetric_two_cycles))
    arch_sequence = [6, 13]
    while len(arch_sequence) <= 33:
        arch_sequence.append(sum(arch_sequence[-2:]))
    alpha = (sqrt(5) - 1) / 2
    decay_samples = []
    for order in range(21, 34):
        value = arch_sequence[order]
        index = (value + 2) // 5
        if index > arguments.limit:
            continue
        excess = sequence[index] / index - alpha
        decay_samples.append(dict(oeis_index=order, oeis_value=value, index=index,
            value=sequence[index], scaled_quarter=excess * log2(index)**0.25,
            scaled_half=excess * log2(index)**0.5,
            relative_error_from_0087=excess * log2(index)**0.25 / 0.087 - 1))
    family_audit = []
    for start_shift, depth_shift, expected_side in [(2, 2, 'above'), (2, 1, 'below'), (1, 2, 'below')]:
        variant = generate_compact(arguments.family_limit, start_shift, depth_shift)
        assert list(variant[:4097]) == literal_family(4096, start_shift, depth_shift)
        side_failures = [index for index in range(1, len(variant))
            if (variant[index] < g_closed(index) if expected_side == 'above' else variant[index] > g_closed(index))]
        anchor_failures = [order for order, index in enumerate(fibonacci)
            if order >= 2 and index < len(variant) and variant[index] != fibonacci[order - 1]]
        family_audit.append(dict(start_shift=start_shift, depth_shift=depth_shift,
            initial_values=[1, 1], recurrence_starts_at=3, limit=arguments.family_limit,
            expected_side=expected_side, side_failures=side_failures,
            fibonacci_failures=anchor_failures, literal_agrees_through=4096,
            first_30=list(variant[1:31]), sequence_sha256=digest_sequence(variant)))
    report = dict(status='Finite audit; conditional lemmas are proved separately; no universal G/Fibonacci or limit theorem claimed.',
        source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        evaluator_source_sha256=hashlib.sha256(Path(__file__).with_name('conway_explore.py').read_bytes()).hexdigest(),
        limit=arguments.limit, sequence_sha256=digest_sequence(sequence),
        independent_brent_agrees_through=independent_limit,
        negative_defects=negative_defects, equality_indices=equalities,
        equality_set_symmetric_difference=sorted(set(equalities) ^ {index for index in zero_set if 1 <= index <= arguments.limit}),
        selected_split_audit_limit=arguments.family_limit, delta_counts=dict(sorted(delta_counts.items())),
        landing_counts=dict(sorted(landing_counts.items())), negative_carry_landings=negative_carry_landings,
        corrected_landing_failures=corrected_landing_failures,
        fibonacci_audit=fibonacci_audit, decay_samples=decay_samples,
        decay_values_are_floating_point_observations=True,
        oeis_source='https://oeis.org/A022388; offset 0; a(0)=6, a(1)=13, a(m)=a(m-1)+a(m-2)',
        family_audit=family_audit)
    rendered = json.dumps(report, indent=2, ensure_ascii=False) + '\n'
    if arguments.output:
        arguments.output.write_text(rendered)
    else:
        print(rendered, end='')


if __name__ == '__main__':
    main()

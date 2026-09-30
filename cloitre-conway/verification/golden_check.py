"""Check the finite premises of the global golden-ratio induction."""

import bisect
import hashlib
import json
from pathlib import Path

from conway_explore import brent_generate, envelope_certificate, full_orbit, generate, g_closed, literal_generate


def fibonacci_values(limit):
    values = [0, 1]
    while values[-1] <= limit + 1:
        values.append(sum(values[-2:]))
    return values


def candidate_zeros(fibonacci):
    indices = {11, 24, 25, 59}
    for order, value in enumerate(fibonacci):
        if order >= 2:
            indices.update((value, value + 1))
        if order >= 3 and order % 2:
            indices.add(value - 1)
    return indices


def upper_cap(index, fibonacci):
    if index == 1:
        return 1
    order = bisect.bisect_right(fibonacci, index) - 1
    return min(index - fibonacci[order - 2], fibonacci[order])


def main():
    if not __debug__:
        raise SystemExit('Run without -O; assertions check the finite premises.')
    seed_start = 16384
    induction_start = 4 * seed_start
    limit = 8 * seed_start - 1
    sequence, preperiods, periods, splits = generate(limit)
    assert sequence == brent_generate(limit)
    literal, updates = literal_generate(4096)
    assert sequence[:len(literal)] == literal
    fibonacci = fibonacci_values(limit)
    zero_set = candidate_zeros(fibonacci)
    certificate = envelope_certificate(sequence, seed_start)
    assert certificate['upper_numerator'] == 15225
    assert certificate['upper_denominator'] == 22877
    assert 3 * certificate['upper_numerator'] < 2 * certificate['upper_denominator']
    base_zeros = []
    for index in range(1, induction_start):
        defect = sequence[index] - g_closed(index)
        assert defect >= 0
        if defect == 0:
            assert index in zero_set
            base_zeros.append(index)
    caps = [0] + [upper_cap(index, fibonacci) for index in range(1, limit + 1)]
    assert all(0 <= caps[index] - caps[index - 1] <= 1 for index in range(2, len(caps)))
    assert all(sequence[index] <= caps[index] for index in range(1, len(sequence)))
    equality_indices = [index for index in range(1, len(sequence)) if sequence[index] == g_closed(index)]
    assert set(equality_indices) == {index for index in zero_set if 1 <= index <= limit}
    cycle_points_checked = 0
    for index in range(8, limit + 1):
        order = bisect.bisect_right(fibonacci, index) - 1
        anchor = fibonacci[order]
        previous = fibonacci[order - 1]
        earlier = fibonacci[order - 2]
        trajectory, preperiod, period = full_orbit(sequence, index)
        assert preperiod == preperiods[index] and period == periods[index]
        assert sequence[index - 1] >= preperiod
        for point in trajectory[preperiod:]:
            assert max(previous, index - previous) <= point <= min(anchor, index - earlier)
            cycle_points_checked += 1
        if index >= induction_start:
            assert 9 * splits[index] > 5 * index
            assert 3 * splits[index] < 2 * index
    fibonacci_checks = []
    for order, index in enumerate(fibonacci):
        if order < 2 or index > limit:
            continue
        assert sequence[index] == fibonacci[order - 1]
        if order >= 5:
            assert sequence[index - 1] == fibonacci[order - 1]
        if order >= 3 and index + 1 <= limit:
            assert sequence[index + 1] == fibonacci[order - 1] + 1
        fibonacci_checks.append(dict(order=order, index=index, value=sequence[index]))
    rotation_checks = []
    rotation_fibonacci = fibonacci_values(200000)
    for order in range(5, 26, 2):
        anchor = rotation_fibonacci[order]
        previous = rotation_fibonacci[order - 1]
        stop = rotation_fibonacci[order + 2]
        high_returns = [argument for argument in range(1, stop)
            if g_closed(argument + anchor - 1) >= g_closed(argument - 1) + previous + 1]
        assert high_returns == [rotation_fibonacci[order + 1]]
        rotation_checks.append(dict(order=order, argument_upper_exclusive=stop, high_returns=high_returns))
    report = dict(
        status='Exact finite premises; the universal induction and cycle capture are written in golden-proof.md; no Lean formalization.',
        source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        evaluator_source_sha256=hashlib.sha256(Path(__file__).with_name('conway_explore.py').read_bytes()).hexdigest(),
        limit=limit, sequence_sha256=hashlib.sha256(','.join(map(str, sequence[1:])).encode('ascii')).hexdigest(),
        independent_brent_agrees_through=limit, literal_agrees_through=4096, literal_updates=updates,
        induction_base_inclusive=[1, induction_start - 1],
        base_defects_nonnegative=True, base_zero_set_contained=True,
        base_zero_count=len(base_zeros), base_zero_indices=base_zeros,
        propagation_seed=certificate, upper_seed_strictly_below_two_thirds=True,
        upper_cap_initial_values=caps[1:8], upper_cap_lipschitz_checked_through=limit,
        upper_cap_inequalities_checked_through=limit,
        exact_equality_set_checked_through=limit, equality_indices=equality_indices,
        cycle_capture_checked_inclusive=[8, limit], cycle_points_checked=cycle_points_checked,
        fibonacci_checks=fibonacci_checks,
        exact_rotation_diagnostics=rotation_checks,
    )
    print(json.dumps(report, indent=2) + '\n', end='')


if __name__ == '__main__':
    main()

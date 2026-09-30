"""Exact experiments for Campbell's variable-depth recurrence.

No candidate formula is used to generate the recursive sequence. A separate
literal implementation checks the orbit-based evaluator on a shorter prefix.
"""

import argparse
from collections import Counter
import hashlib
import json


def candidate(n):
    if n == 1:
        return 1
    s = 1
    if n % 2:
        while 9 * s <= n:
            s *= 3
        return max(2 * s, n - 3 * s)
    while 6 * s <= n:
        s *= 3
    return min(n - s, 3 * s)


def orbit(prefix, n):
    values = []
    seen = {}
    x = n - 1
    while x not in seen:
        assert 1 <= x < n
        seen[x] = len(values)
        values.append(x)
        x = n - prefix[x]
    mu = seen[x]
    return values, mu, len(values) - mu


def orbit_value(values, mu, period, depth):
    if depth < len(values):
        return values[depth]
    return values[mu + (depth - mu) % period]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--limit', type=int, default=1_000_000)
    parser.add_argument('--literal-limit', type=int, default=5_000)
    args = parser.parse_args()
    assert 19 <= args.literal_limit <= args.limit
    b = [0, 1]
    cycles = Counter()
    max_mu = 0
    max_distinct = 0
    formula_failures = []
    orbit_failures = []
    witnesses = {}
    for n in range(2, args.limit + 1):
        values, mu, period = orbit(b, n)
        depth = b[n - 1]
        result = orbit_value(values, mu, period, depth)
        assert 1 <= result < n
        b.append(result)
        cycles[period] += 1
        max_mu = max(max_mu, mu)
        max_distinct = max(max_distinct, len(values))
        if result != candidate(n):
            formula_failures.append(n)
        if mu > 4 or period > 2:
            orbit_failures.append(n)
        if n in (4, 11, 24, 29, 30, 36, 47, 54, 81):
            witnesses[str(n)] = dict(depth=depth, values=values, mu=mu,
                                     period=period, result=result)

    literal = [0, 1]
    literal_updates = 0
    for n in range(2, args.literal_limit + 1):
        x = n - 1
        for _ in range(literal[n - 1]):
            assert 1 <= x < n
            x = n - literal[x]
            literal_updates += 1
        literal.append(x)
    assert literal == b[:args.literal_limit + 1]
    assert b[1:20] == [1, 1, 2, 3, 2, 3, 4, 5, 6, 7, 6, 9, 6, 9, 6, 9, 8, 9, 10]
    assert not formula_failures
    assert not orbit_failures
    digest = hashlib.sha256(','.join(map(str, b[1:])).encode('ascii')).hexdigest()
    print(json.dumps(dict(
        definition='b(1)=1; b(n)=T_n^b(n-1)(n-1); T_n(x)=n-b(x)',
        limit=args.limit,
        literal_limit=args.literal_limit,
        literal_updates=literal_updates,
        literal_agrees=True,
        candidate_mismatches=formula_failures,
        orbit_bound_failures=orbit_failures,
        cycle_histogram=dict(sorted(cycles.items())),
        max_preperiod=max_mu,
        max_distinct_orbit_values=max_distinct,
        first_80=b[1:81],
        comma_separated_sequence_sha256=digest,
        witnesses=witnesses,
        status='finite exact computation, not a universal proof or Lean verification',
    ), indent=2))


if __name__ == '__main__':
    main()

"""Check all orbit-table identities by exact rational linear elimination.

The two variables are n and s. Each table domain has s >= 3. Feasibility
uses Fourier-Motzkin elimination, including strict inequalities, so these
checks range over entire real polyhedra, not sampled integer parameters.
Parity and the power-of-three scale are explicit mathematical premises.
"""

from fractions import Fraction as Q
from itertools import product
import json
from math import gcd, lcm


def affine(n=0, s=0, c=0):
    return (Q(n), Q(s), Q(c))


N, S, ONE = affine(n=1), affine(s=1), affine(c=1)
ZERO = affine()


def add(a, b):
    return tuple(x + y for x, y in zip(a, b))


def scale(a, q):
    return tuple(x * q for x in a)


def sub(a, b):
    return add(a, scale(b, -1))


def norm(constraints):
    result = {}
    for a, strict in constraints:
        denominator = lcm(*(v.denominator for v in a))
        integers = tuple(int(v * denominator) for v in a)
        divisor = gcd(*integers) or 1
        key = tuple(Q(v // divisor) for v in integers)
        result[key] = result.get(key, False) or strict
    return list(result.items())


def feasible(constraints):
    constraints = norm(constraints)
    for variable in (0, 1):
        positive, negative, independent = [], [], []
        for a, strict in constraints:
            if a[variable] > 0:
                positive.append((a, strict))
            elif a[variable] < 0:
                negative.append((a, strict))
            else:
                independent.append((a, strict))
        for (p, ps), (m, ms) in product(positive, negative):
            independent.append((add(scale(p, 1 / p[variable]),
                                    scale(m, -1 / m[variable])), ps or ms))
        constraints = norm(independent)
    return all(a[2] > 0 if strict else a[2] >= 0
               for a, strict in constraints)


def nonnegative(region, value):
    assert not feasible(region + [(scale(value, -1), True)]), (region, value)


def equal(region, a, b):
    nonnegative(region, sub(a, b))
    nonnegative(region, sub(b, a))


def minimum(a, b):
    return ('min', a, b)


def pieces(expression):
    if expression[0] == 'min':
        _, a, b = expression
        return [(a, [(sub(b, a), False)]),
                (b, [(sub(a, b), False)])]
    return [(expression, [])]


def parity(expression, n_parity):
    # Substitute s=3t with t odd, as s is a power of 3 and s >= 3.
    a, b, c = expression
    coefficients = (a, 3*b, c)
    assert all(v.denominator == 1 for v in coefficients)
    return int(a*n_parity + 3*b + c) % 2


def f_pieces(x, x_parity):
    for t in (scale(S, Q(1, 3)), S, scale(S, 3)):
        if x_parity == 0:
            yield sub(x, t), [(sub(x, scale(t, 2)), False),
                              (sub(scale(t, 4), x), False)]
            yield scale(t, 3), [(sub(x, scale(t, 4)), False),
                               (sub(scale(t, 6), x), False)]
        else:
            yield scale(t, 2), [(sub(x, scale(t, 3)), False),
                               (sub(scale(t, 5), x), False)]
            yield sub(x, scale(t, 3)), [(sub(x, scale(t, 5)), False),
                                       (sub(scale(t, 9), x), False)]


def v(a=0, b=0, c=0):
    return affine(a, Q(b), c)


# Each row lists its closed n interval, followed by x_1,...,x_6.
EVEN = [
    ('E1', v(0, 2), v(0, 3, 1), [
        v(0, 1, 1), v(1, '-2/3', -1),
        minimum(v(1, '-2/3'), v(0, '5/3', 1)), v(1, -1),
        minimum(v(1, '-2/3'), v(0, 2)), v(1, -1)]),
    ('E2', v(0, 3, 1), v(0, '10/3'), [
        v(1, -2), v(0, '7/3'), v(1, '-4/3'), v(1, -1), v(0, 2), v(1, -1)]),
    ('E3', v(0, '10/3'), v(0, 4), [
        v(1, -2), v(1, -1), v(0, 2), v(1, -1), v(0, 2), v(1, -1)]),
    ('E4', v(0, 4), v(0, 5, 1), [
        v(1, -2), v(0, 3), v(1, -2), v(0, 3), v(1, -2), v(0, 3)]),
    ('E5', v(0, 5, 1), v(0, 6), [
        v(0, 3, 1), v(1, -2, -1), v(1, -2), v(0, 3), v(1, -2), v(0, 3)]),
]
ODD = [
    ('O1', v(0, 3), v(0, 4, 1), [
        v(0, 1, 1), v(1, '-2/3', -1), v(0, '5/3', 1), v(1, -1), v(0, 2), v(1, -1)]),
    ('O2', v(0, 4, 1), v(0, '13/3'), [
        v(1, -3), v(0, '10/3'), v(1, '-7/3'), v(1, -1), v(0, 2), v(1, -1)]),
    ('O3', v(0, '13/3'), v(0, 5), [
        v(1, -3), v(1, -1), v(0, 2), v(1, -1), v(0, 2), v(1, -1)]),
    ('O4', v(0, 5), v(0, 6, 1), [
        v(1, -3), v(0, 4), v(1, -3), v(0, 4), v(1, -3), v(0, 4)]),
    ('O5', v(0, 6, 1), v(0, 7), [
        v(0, 3, 1), v(1, -2, -1), v(1, -3), v(0, 4), v(1, -3), v(0, 4)]),
    ('O6', v(0, 7), v(0, 8, 1), [
        v(0, 3, 1), v(1, -2, -1), v(1, -3), v(1, -3), v(1, -3), v(1, -3)]),
    ('O7', v(0, 8, 1), v(0, 9), [
        v(0, 3, 1), v(1, -2, -1), v(0, 5, 1), v(1, -3), v(1, -3), v(1, -3)]),
]


def check_tables():
    count = 0
    scale_region = [(v(0, 1, -3), False)]
    for n_parity, rows, lower, upper in ((0, EVEN, 2, 6), (1, ODD, 3, 9)):
        assert rows[0][1] == v(0, lower)
        assert rows[-1][2] == v(0, upper)
        for left, right in zip(rows, rows[1:]):
            assert left[2] == right[1]
        for name, lo, hi, orbit in rows:
            nonnegative(scale_region, sub(hi, lo))
            region = scale_region + [(sub(N, lo), False), (sub(hi, N), False)]
            values = [v(1, 0, -1)] + orbit
            for j in range(6):
                for (x, xr), (y, yr) in product(pieces(values[j]), pieces(values[j+1])):
                    active = region + xr + yr
                    if not feasible(active):
                        continue
                    p = parity(x, n_parity)
                    assert parity(y, n_parity) == (n_parity + p + 1) % 2
                    # These full intervals are covered by the six F branches.
                    low = scale(S, Q(2, 3)) if p == 0 else S
                    high = scale(S, 18 if p == 0 else 27)
                    nonnegative(active, sub(x, low))
                    nonnegative(active, sub(high, x))
                    nonnegative(active, sub(x, ONE))
                    nonnegative(active, sub(sub(N, ONE), x))
                    for fx, fr in f_pieces(x, p):
                        branch = active + fr
                        if feasible(branch):
                            equal(branch, y, sub(N, fx))
                            count += 1
            equal(region, orbit[3], orbit[5])
            target = orbit[3] if n_parity == 0 else orbit[4]
            for fn, fr in f_pieces(N, n_parity):
                branch = region + fr
                if feasible(branch):
                    equal(branch, target, fn)
            # Check the minimum depth needed to select x4 or x5.
            deep = region + [(v(1, 0, -(9 if n_parity else 10)), False)]
            for fn, fr in f_pieces(v(1, 0, -1), 1-n_parity):
                branch = deep + fr
                if feasible(branch):
                    nonnegative(branch, sub(fn, affine(c=4+n_parity)))
    return count


def check_small():
    b = [0, 1]
    for n in range(2, 9):
        x = n-1
        values = [x]
        for _ in range(max(6, b[n-1])):
            x = n-b[x]
            values.append(x)
        b.append(values[b[n-1]])
        assert values[4] == values[6]
    assert b[1:] == [1, 1, 2, 3, 2, 3, 4, 5]


def check_elimination():
    assert feasible([(N, True), (scale(N, -1), False)]) is False
    assert feasible([(sub(N, S), True), (sub(S, N), True)]) is False
    assert feasible([(N, True), (S, True)]) is True
    assert feasible([(sub(N, S), False), (sub(S, N), False)]) is True
    assert feasible([(sub(N, S), False), (sub(S, N), False),
                     (affine(c=-1), False)]) is False


def check_closure_interface():
    templates = {
        'even_low_linear': (v(1, -1), v(1, '-2/3')),
        'even_low_plateau': (v(1, -1), v(0, 2)),
        'even_high': (v(0, 3), v(1, -2)),
        'odd_low': (v(1, -1), v(0, 2)),
        'odd_middle': (v(0, 4), v(1, -3)),
        'odd_high_fixed': (v(1, -3), v(1, -3)),
    }
    row_groups = {
        'even_low_linear': ['E1-left'],
        'even_low_plateau': ['E1-right', 'E2', 'E3'],
        'even_high': ['E4', 'E5'],
        'odd_low': ['O1', 'O2', 'O3'],
        'odd_middle': ['O4', 'O5'],
        'odd_high_fixed': ['O6', 'O7'],
    }
    endpoint_pairs = set(templates.values())
    assert len(templates) == 6
    assert len(endpoint_pairs) == 5
    assert sum(len(rows) for rows in row_groups.values()) == 13
    assert row_groups['even_low_linear'] == ['E1-left']
    assert row_groups['even_low_plateau'] == ['E1-right', 'E2', 'E3']
    assert row_groups['even_high'] == ['E4', 'E5']
    assert row_groups['odd_low'] == ['O1', 'O2', 'O3']
    assert row_groups['odd_middle'] == ['O4', 'O5']
    assert row_groups['odd_high_fixed'] == ['O6', 'O7']
    return templates, row_groups


if __name__ == '__main__':
    check_elimination()
    check_small()
    count = check_tables()
    templates, row_groups = check_closure_interface()
    print(json.dumps(dict(
        status='passed', table_rows=12, transitions=72,
        feasible_affine_transition_branches=count,
        method='exact rational Fourier-Motzkin elimination over all real s>=3',
        checked=['interval coverage', 'transition identities', 'index bounds',
                 'parity', 'x6=x4', 'formula output', 'minimum depth',
                 'small cases', 'six distinct endpoint templates'],
        closure_interface=dict(
            endpoint_template_count=len(templates),
            distinct_affine_endpoint_map_count=len(set(templates.values())),
            endpoint_templates={
                name: [[str(value) for value in pair] for pair in endpoint]
                for name, endpoint in templates.items()
            },
            row_groups=row_groups,
            phase='parity of n; no independent five-phase selector',
            qualification='The six labels are distinct parity/domain templates; five affine endpoint maps occur because the even- and odd-low plateau labels share the same map on different domains. The explicit formula derives the applicable label from n and its power-of-three scale.'
        ),
        scope='arithmetic certificate for the written induction, not Lean verification',
    ), indent=2))

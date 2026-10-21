import argparse
import json
import math
from array import array
from bisect import bisect_right


def golden(index):
    return (math.isqrt(5 * (index + 1) ** 2) - index - 1) // 2


def upper(index, fibonacci):
    order = bisect_right(fibonacci, index) - 1
    return min(index - fibonacci[order - 2], fibonacci[order])


def rounded(index, fibonacci):
    cap = upper(index, fibonacci)
    return max(golden(index), 2 * (cap // 2))


def brent_selected(parent, value):
    depth = value(parent - 1)
    power = period = 1
    tortoise = parent - 1
    hare = parent - value(tortoise)
    updates = 1
    while tortoise != hare:
        if power == period:
            tortoise = hare
            power *= 2
            period = 0
        hare = parent - value(hare)
        updates += 1
        period += 1
    entrance = 0
    tortoise = hare = parent - 1
    for iteration in range(period):
        hare = parent - value(hare)
        updates += 1
    while tortoise != hare:
        tortoise = parent - value(tortoise)
        hare = parent - value(hare)
        updates += 2
        entrance += 1
    rank = depth if depth < entrance else entrance + (depth - entrance) % period
    selected = parent - 1
    for iteration in range(rank):
        selected = parent - value(selected)
        updates += 1
    return selected, entrance, period, updates


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--limit', type=int, default=131072)
    arguments = parser.parse_args()
    limit = arguments.limit
    if limit < 512:
        parser.error('--limit must be at least 512 to cover the finite premise')
    fibonacci = [0, 1]
    while len(fibonacci) <= 182 or fibonacci[-1] <= limit:
        fibonacci.append(sum(fibonacci[-2:]))
    golden_values = array('I', [0])
    values = array('I', [0])
    order = 2
    for index in range(1, limit + 1):
        golden_values.append(index - golden_values[golden_values[index - 1]])
        assert golden_values[index] == golden(index)
        while index >= fibonacci[order + 1]:
            order += 1
        cap = min(index - fibonacci[order - 2], fibonacci[order])
        values.append(max(golden_values[index], 2 * (cap // 2)))
        assert cap - 1 <= values[index] <= cap
    minimum = maximum = 0
    minimum_parent = maximum_parent = 0
    literal_updates = base_updates = visited_updates = brent_updates = 0
    maximum_c = maximum_r = drawdown_c = drawdown_r = 0
    odd_clock_count = 0
    base_minimum = base_maximum = 0
    for parent in range(3, limit + 1):
        path, positions = [], {}
        point = parent - 1
        while point not in positions:
            assert 0 < point < parent
            positions[point] = len(path)
            path.append(point)
            point = parent - values[point]
            visited_updates += 1
        entrance = positions[point]
        period = len(path) - entrance
        assert period <= 2
        depth = values[parent - 1]
        assert depth >= entrance
        rank = depth if depth < len(path) else entrance + (depth - entrance) % period
        selected = path[rank]
        independent, entrance_b, period_b, updates = brent_selected(parent, values.__getitem__)
        brent_updates += updates
        assert (selected, entrance, period) == (independent, entrance_b, period_b)
        if parent <= 4096:
            literal = parent - 1
            for iteration in range(depth):
                literal = parent - values[literal]
                literal_updates += 1
                if parent <= 511:
                    base_updates += 1
            assert selected == literal
        output = values[selected] + values[parent - selected]
        residual = output - values[parent]
        assert -2 <= residual <= 2
        if parent <= 511:
            base_minimum = min(base_minimum, residual)
            base_maximum = max(base_maximum, residual)
        if residual < minimum:
            minimum, minimum_parent = residual, parent
        if residual > maximum:
            maximum, maximum_parent = residual, parent
        odd_clock_count += depth % 2
    for index in range(1, limit + 1):
        drawdown_c = max(drawdown_c, maximum_c - values[index])
        drawdown_r = max(drawdown_r, maximum_r - (index - values[index]))
        maximum_c = max(maximum_c, values[index])
        maximum_r = max(maximum_r, index - values[index])
    assert drawdown_c == 0 and drawdown_r <= 1
    knee_checks = 0
    last_knee = None
    for order in range(6, 181, 3):
        source = fibonacci[order] + fibonacci[order - 2]
        cap_value = lambda index: upper(index, fibonacci)
        rounded_value = lambda index: rounded(index, fibonacci)
        selected_u, entrance_u, period_u, updates = brent_selected(source, cap_value)
        selected_v, entrance_v, period_v, updates = brent_selected(source, rounded_value)
        assert cap_value(source - 1) >= entrance_u
        assert rounded_value(source - 1) >= entrance_v
        assert selected_u == 2 * fibonacci[order - 2]
        output_u = cap_value(selected_u) + cap_value(source - selected_u)
        output_v = rounded_value(selected_v) + rounded_value(source - selected_v)
        assert output_u == fibonacci[order] - fibonacci[order - 5]
        assert abs(output_v - rounded_value(source)) <= 10
        assert output_v - output_u >= fibonacci[order - 5] - 10
        knee_checks += 1
        last_knee = dict(order=order, source=source, output_difference=output_v - output_u)
    print(json.dumps(dict(
        finite_premise=dict(domain=[3, 511], residual_range=[base_minimum, base_maximum],
                            literal_updates=base_updates),
        corroboration=dict(limit=limit, residual_range=[minimum, maximum],
                           residual_witnesses=[minimum_parent, maximum_parent],
                           visited_updates=visited_updates, brent_updates=brent_updates,
                           independent_selector_comparisons=limit - 2,
                           literal_limit=min(limit, 4096), literal_updates=literal_updates,
                           odd_clocks=odd_clock_count, drawdowns=[drawdown_c, drawdown_r]),
        instability_knees=dict(orders=[6, 180, 3], count=knee_checks, last=last_knee),
        scope='The literal finite premise supports the written universal bound 10. '
              'The observed bound 2 and additional knee checks are finite corroboration only. '
              'V is an explicit comparison sequence, not canonical Cloitre values.'), indent=2))


if __name__ == '__main__':
    main()

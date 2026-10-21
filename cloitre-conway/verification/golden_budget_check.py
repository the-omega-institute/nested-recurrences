"""Check the finite base and selected-tree consequences of the golden budget."""

import json
import math

from conway_explore import brent_generate, generate, literal_generate


def main():
    if not __debug__:
        raise SystemExit('Run without -O; assertions check the finite premises.')
    limit = 131072
    values, preperiods, periods, selected = generate(limit)
    assert values == brent_generate(limit)
    for index in range(3, limit + 1):
        depth = values[index - 1]
        slow, fast = index - 1, index - values[index - 1]
        power = period = steps = 1
        while slow != fast and steps < depth:
            if power == period:
                slow = fast
                power *= 2
                period = 0
            fast = index - values[fast]
            period += 1
            steps += 1
        if slow == fast:
            for iteration in range((depth - steps) % period):
                fast = index - values[fast]
        assert fast == selected[index]
    literal, literal_updates = literal_generate(4096)
    assert values[:4097] == literal
    for index in range(3, 4097):
        point = index - 1
        for iteration in range(literal[index - 1]):
            point = index - literal[point]
        assert point == selected[index]

    def golden(index):
        return (math.isqrt(5 * (index + 1) ** 2) - index - 1) // 2

    defects = [0] + [values[index] - golden(index) for index in range(1, limit + 1)]
    budgets = [max(defect - 1, 0) for defect in defects]
    assert selected[12] == 7 and (defects[12], defects[7], defects[5]) == (0, 1, 0)
    heights = [0] * (limit + 1)
    positive_counts = [0] * (limit + 1)
    fibonacci = [0, 1]
    while fibonacci[-1] <= limit:
        fibonacci.append(sum(fibonacci[-2:]))
    one_zero_negative = []
    inherited_positive_defect = 0
    positive_parents = 0
    simultaneous_positive_children = 0
    total_spine_edges = 0
    maximum_spine = None
    maximum_spine_steps = -1
    for index in range(3, limit + 1):
        first, second = selected[index], index - selected[index]
        parent, left, right = defects[index], defects[first], defects[second]
        carry = parent - left - right
        assert -1 <= carry <= 1
        assert budgets[first] + budgets[second] <= budgets[index]
        assert 5 * first <= 4 * index and 5 * second <= 4 * index
        heights[index] = 1 + max(heights[first], heights[second])
        positive_counts[index] = ((1 + positive_counts[first] + positive_counts[second])
                                  if budgets[index] else 0)
        assert positive_counts[index] <= budgets[index] * (heights[index] + 1)
        if parent:
            positive_parents += 1
            assert max(left, right) <= parent
            if not left or not right:
                assert carry >= 0
        else:
            assert max(left, right) <= 1
            inherited_positive_defect += bool(left or right)
        simultaneous_positive_children += bool(budgets[first] and budgets[second])
        if bool(left) != bool(right) and carry == -1:
            row = dict(index=index, children=[first, second], defects=[parent, left, right])
            one_zero_negative.append(row)
            if index >= 65536:
                order = next(order for order in range(3, len(fibonacci))
                             if fibonacci[order] - 1 == index)
                assert order % 2 == 1
                assert first == fibonacci[order - 1] - 1
                assert second == fibonacci[order - 2]
                assert (parent, left, right) == (0, 1, 0)

        point, spine = index, []
        while budgets[point]:
            first, second = selected[point], point - selected[point]
            child = min((first, second), key=lambda argument: (budgets[argument], argument))
            assert budgets[child] <= budgets[point] // 2
            spine.append(point)
            point = child
        assert len(spine) <= budgets[index].bit_length()
        total_spine_edges += len(spine)
        if len(spine) > maximum_spine_steps:
            maximum_spine_steps = len(spine)
            maximum_spine = dict(root=index, budget=budgets[index], indices=spine,
                                  terminal=point, terminal_defect=defects[point])

    print(json.dumps(dict(limit=limit, finite_base_inclusive=[3, 65535],
                          finite_base_splits=65533, higher_corroboration_splits=limit - 65535,
                          independent_values_compared=limit, independent_selectors_compared=limit - 2,
                          literal_prefix=4096,
                          literal_updates=literal_updates, literal_selectors_compared=4094,
                          all_budget_splits_checked=limit - 2,
                          positive_parent_monotonicity_checks=positive_parents,
                          zero_parents_with_positive_child=inherited_positive_defect,
                          one_zero_negative_carries=one_zero_negative,
                          simultaneous_positive_budget_children=simultaneous_positive_children,
                          maximum_tree_height=max(heights),
                          positive_occurrence_count_checks=limit - 2,
                          total_greedy_spine_edges=total_spine_edges,
                          longest_retained_spine=maximum_spine,
                          scope='The written proof supplies all indices >=65536. Independent finite base checks supply smaller indices. Tree and spine checks corroborate the proved consequences; no uniform dispersion or full convergence claim.'), indent=2))


if __name__ == '__main__':
    main()

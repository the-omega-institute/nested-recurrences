import collections
import json
import math

from conway_explore import brent_generate, generate, literal_generate


def transition(state, inputs):
    parity, previous, carried = state
    current = list(inputs) + [0] * 9
    next_carried = [0] * 11
    for order in range(2, 11):
        next_carried[order] = (current[order - 2] if current[order - 1] == 0
                               else (carried >> (order - 2)) & 1)
        anchor_parity = int((order - 1) % 3 != 0)
        prior = (previous >> (order - 2)) & 1
        current[order] = next_carried[order] * int(
            (anchor_parity + 1 - parity - prior) % 2 == 0)
    return (1 - parity,
            sum(current[order] << (order - 2) for order in range(2, 11)),
            sum(next_carried[order] << (order - 2) for order in range(2, 11)))


def certificate():
    states = [(0, 0, 0)]
    indices = {states[0]: 0}
    queue = collections.deque(states)
    rows = []
    while queue:
        state = queue.popleft()
        successors = []
        for inputs in ((0, 0), (1, 0), (0, 1), (1, 1)):
            target = transition(state, inputs)
            if target not in indices:
                indices[target] = len(states)
                states.append(target)
                queue.append(target)
            successors.append(indices[target])
        outputs = [order for order in range(2, 11) if (state[1] >> (order - 2)) & 1]
        assert 9 not in outputs and 10 not in outputs
        rows.append(dict(parity=state[0], output_orders=outputs,
                         carried_orders=[order for order in range(2, 11)
                                         if (state[2] >> (order - 2)) & 1],
                         successors=successors))
    expected = [[1, 2, 3, 3], [0, 4, 5, 5], [0, 6, 6, 6], [0, 4, 7, 7],
                [1, 2, 2, 2], [1, 8, 3, 3], [1, 9, 10, 10], [1, 11, 12, 12],
                [0, 13, 13, 13], [0, 4, 14, 14], [0, 4, 15, 15], [0, 16, 16, 16],
                [0, 4, 5, 5], [1, 9, 17, 17], [1, 8, 8, 8], [1, 11, 11, 11],
                [1, 9, 10, 10], [0, 4, 14, 14]]
    assert len(states) == 18
    assert [row['successors'] for row in rows] == expected
    return dict(states=len(states), transitions=4 * len(states),
                first_two_identically_zero_orders=[9, 10], rows=rows)


def canonical_check():
    limit = 832302
    values, _, _, _ = generate(limit)
    assert values == brent_generate(limit)
    literal, updates = literal_generate(4096)
    assert values[:4097] == literal
    fibonacci = [0, 1]
    for order in range(2, 32):
        fibonacci.append(sum(fibonacci[-2:]))

    def defect(order, offset):
        return fibonacci[order - 1] + offset - values[fibonacci[order] + offset]

    barriers = {}
    binary_ends = {}
    for order in range(11, 30):
        domain = fibonacci[order - 1]
        first_defect = next(offset for offset in range(domain + 1) if defect(order, offset))
        barriers[order] = min(first_defect - 1,
                              min(offset - defect(order, offset)
                                  for offset in range(first_defect, domain + 1)))
        binary_ends[order] = next(offset for offset in range(domain + 1)
                                  if defect(order, offset) > 1) - 1
        assert all(min(offset, barriers[order]) <= offset - defect(order, offset) <= offset
                   for offset in range(domain + 1))
    rows = []
    identities = binary_values = 0
    positive = []
    for initial_order in range(11, 29):
        width = min(barriers[initial_order], barriers[initial_order + 1])
        endpoint = min(2 * width, binary_ends[initial_order], binary_ends[initial_order + 1],
                       fibonacci[initial_order - 1])
        exact_width = (math.isqrt(5 * endpoint * endpoint) - endpoint) // 2
        extinction_order = 3 * ((initial_order + 2) // 3) + 9
        assert 1 <= width <= endpoint
        for order in range(initial_order + 2, 31):
            assert all(defect(order, offset) in (0, 1) for offset in range(endpoint + 1))
            binary_values += endpoint + 1
            last_zero = 0
            for offset in range(1, exact_width + 1):
                if defect(order - 1, offset) == 0:
                    last_zero = offset
                predicted = defect(order - 2, last_zero) * int(
                    (fibonacci[order - 1] + offset - defect(order, offset - 1)) % 2 == 0)
                current = defect(order, offset)
                assert current == predicted
                identities += 1
                if current:
                    positive.append(dict(initial_order=initial_order, order=order,
                                         offset=offset, source_last_zero=last_zero,
                                         defect=current))
                if order >= extinction_order:
                    assert current == 0
        rows.append(dict(initial_order=initial_order, saturated_width=width,
                         binary_endpoint=endpoint, resulting_exact_width=exact_width,
                         guaranteed_extinction_order=extinction_order))
    return dict(limit=limit, literal_prefix=4096, literal_updates=updates,
                last_zero_feedback_identities=identities, propagated_binary_values=binary_values,
                positive_identity_cases=positive, rows=rows,
                scope='Independent finite corroboration; extinction orders above 30 are not '
                      'checked by this prefix. The infinite conclusion uses the written '
                      'actual-entry proof and exhaustive state closure.')


def main():
    if not __debug__:
        raise SystemExit('Run without -O; assertions perform the mathematical checks.')
    print(json.dumps(dict(status='PASS', binary_certificate=certificate(),
                          canonical=canonical_check()), indent=2))


if __name__ == '__main__':
    main()

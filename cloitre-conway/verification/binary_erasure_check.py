import collections
import itertools
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


def even_profiles(width, endpoint, parity, sparse=False):
    positions = [offset for offset in range(width + 1, endpoint + 1)
                 if offset % 2 == parity]
    if sparse:
        yield [0] * (endpoint + 1)
        for offset in positions:
            for value in range(2, offset - width + 1, 2):
                row = [0] * (endpoint + 1)
                row[offset] = value
                yield row
        return
    for values in itertools.product(*(range(0, offset - width + 1, 2)
                                      for offset in positions)):
        row = [0] * (endpoint + 1)
        for offset, value in zip(positions, values):
            row[offset] = value
        yield row


def even_defect_check():
    pairs = zero_class = lower_zero = positive = upper_entries = lower_entries = 0
    largest = 0
    for width in range(2, 12):
        endpoint = 2 * width
        inner = (math.isqrt(5 * endpoint * endpoint) - endpoint) // 2
        for phase in range(3):
            parent_parity = int((phase - 1) % 3 != 0)
            source_parity = int((phase - 2) % 3 != 0)
            lower_parity = int((phase - 3) % 3 != 0)
            for source in even_profiles(width, endpoint, source_parity):
                for lower in even_profiles(width, endpoint, lower_parity, sparse=True):
                    pairs += 1
                    largest = max(largest, max(source), max(lower))
                    for offset in range(width + 1, inner + 1):
                        starts = {offset}
                        lower_entries += 1
                        for upper in range(offset + 1, endpoint + 1):
                            start = upper - source[upper]
                            if start <= offset:
                                assert source[upper] > 0 and start >= width
                                assert start % 2 == upper % 2
                                starts.add(start)
                                upper_entries += 1
                        outputs = {0}
                        if offset % 2 == parent_parity:
                            outputs = set()
                            for start in starts:
                                contact = start
                                while source[contact]:
                                    contact -= source[contact]
                                    assert contact >= width
                                assert contact % 2 == start % 2
                                outputs.add(lower[contact])
                        if phase == 0:
                            assert outputs == {0}
                            zero_class += 1
                        if phase == 2 and not any(lower[:inner + 1]):
                            assert outputs == {0}
                            lower_zero += 1
                        positive += any(outputs)
    assert positive > 0 and largest > 2
    return dict(source_profile_lower_probe_pairs=pairs,
                all_possible_upper_entries=upper_entries, lower_entries=lower_entries,
                impossible_order_zero_mod3_outputs=zero_class,
                lower_zero_order_two_mod3_outputs=lower_zero,
                positive_candidates_other_phases=positive,
                largest_defect_in_profiles=largest,
                scope='Finite corroboration of the written even-defect proof, using all '
                      'allowed small source profiles and single-position lower probes '
                      'with the derived support restrictions. Not a canonical sequence '
                      'construction or an infinite premise.')


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
                          even_defects=even_defect_check(),
                          canonical=canonical_check()), indent=2))


if __name__ == '__main__':
    main()

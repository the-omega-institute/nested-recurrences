import argparse
import json

from collections import deque


def quotient(graph):
    """Minimize a DFA whose real states are all accepting."""
    n = len(graph)
    dead = n

    complete = [
        tuple(dead if x < 0 else x for x in row)
        for row in graph
    ] + [(dead,) * 9]

    blocks = [set(range(n)), {dead}]

    while True:
        color = {
            q: i
            for i, block in enumerate(blocks)
            for q in block
        }

        refined = []
        for block in blocks:
            groups = {}
            for q in block:
                signature = tuple(color[x] for x in complete[q])
                groups.setdefault(signature, set()).add(q)
            refined.extend(groups.values())

        if len(refined) == len(blocks):
            break
        blocks = refined

    good = [block for block in blocks if dead not in block]

    start = next(i for i, block in enumerate(good) if 0 in block)
    good[0], good[start] = good[start], good[0]

    color = {
        q: i
        for i, block in enumerate(good)
        for q in block
    }

    return [
        tuple(
            color.get(x, -1)
            for x in complete[next(iter(block))]
        )
        for block in good
    ]


def transform(graph, phase, wpar):
    """
    Input letters:  (lower, source), encoded 3*lower + source.
    Output letters: (source, output), encoded 3*source + output.

    NFA memory:
      input state after pending site,
      pending-site parity,
      pending source,
      pending route,
      preceding route,
      preceding output.
    """
    initials = set()

    for symbol, dest in enumerate(graph[0]):
        if dest < 0:
            continue
        a, b = divmod(symbol, 3)
        initials.add((
            dest,
            1 - wpar,
            b,
            a if b == 0 else 0,
            0,
            0,
        ))

    arrows = {}
    queue = deque(initials)
    seen = set(initials)

    while queue:
        node = queue.popleft()
        q, p, source, z, lastz, lastc = node
        outgoing = [set() for _ in range(9)]

        for symbol, dest in enumerate(graph[q]):
            if dest < 0:
                continue

            a, b = divmod(symbol, 3)

            if b == 0:
                newz = a
            elif b == 1:
                newz = z
            else:
                newz = lastz

            if (phase + p - lastc) % 2:
                candidates = {0}
            else:
                candidates = {z, lastz} if b == 2 else {z}

            for c in candidates:
                nxt = (dest, 1 - p, b, newz, z, c)
                outgoing[3 * source + c].add(nxt)

                if nxt not in seen:
                    seen.add(nxt)
                    queue.append(nxt)

        arrows[node] = outgoing

    root = frozenset(initials)
    states = [root]
    index = {root: 0}
    deterministic = []

    for subset in states:
        row = []

        for letter in range(9):
            target = frozenset().union(
                *(arrows[q][letter] for q in subset)
            )

            if not target:
                row.append(-1)
                continue

            if target not in index:
                index[target] = len(states)
                states.append(target)

            row.append(index[target])

        deterministic.append(tuple(row))

    return quotient(deterministic)




def minimize(graph):
    count = len(graph)
    table = [tuple(target if target >= 0 else count for target in row) for row in graph]
    table.append((count,) * 9)
    colors = [0] * count + [1]
    while True:
        signatures = {}
        refined = []
        for state, row in enumerate(table):
            signature = (state == count, tuple(colors[target] for target in row))
            if signature not in signatures:
                signatures[signature] = len(signatures)
            refined.append(signatures[signature])
        if len(set(refined)) == len(set(colors)):
            colors = refined
            break
        colors = refined
    representatives = {}
    for state, color in enumerate(colors):
        representatives.setdefault(color, state)
    dead = colors[count]
    reachable = [colors[0]]
    indices = {reachable[0]: 0}
    result = []
    for color in reachable:
        row = []
        for target in table[representatives[color]]:
            target_color = colors[target]
            if target_color == dead:
                row.append(-1)
            else:
                if target_color not in indices:
                    indices[target_color] = len(reachable)
                    reachable.append(target_color)
                row.append(indices[target_color])
        result.append(tuple(row))
    return result


def advance(graph, phase, width_parity):
    root = (0, 1 - width_parity, 0, 0, 0, False)
    nodes = [root]
    indices = {root: 0}
    arrows = []
    for node in nodes:
        state, parity, previous_route, older_route, previous_output, require_two = node
        outgoing = [set() for _ in range(9)]
        for symbol, target_state in enumerate(graph[state]):
            lower, source = divmod(symbol, 3)
            if target_state < 0 or (require_two and source != 2):
                continue
            route = lower if source == 0 else previous_route if source == 1 else older_route
            if (phase + parity - previous_output) % 2:
                choices = {(0, False)}
            else:
                choices = {(route, False), (previous_route, True)}
            for output, next_requires_two in choices:
                continuation = any(destination >= 0 and (not next_requires_two or letter % 3 == 2)
                                   for letter, destination in enumerate(graph[target_state]))
                if not continuation:
                    continue
                target = (target_state, 1 - parity, route, previous_route,
                          output, next_requires_two)
                if target not in indices:
                    indices[target] = len(nodes)
                    nodes.append(target)
                outgoing[3 * source + output].add(indices[target])
        arrows.append(outgoing)
    subsets = [frozenset({0})]
    subset_indices = {subsets[0]: 0}
    deterministic = []
    for subset in subsets:
        row = []
        for symbol in range(9):
            target = frozenset(destination for state in subset for destination in arrows[state][symbol])
            if not target:
                row.append(-1)
                continue
            if target not in subset_indices:
                subset_indices[target] = len(subsets)
                subsets.append(target)
            row.append(subset_indices[target])
        deterministic.append(tuple(row))
    return minimize(deterministic), len(nodes), len(subsets)



def equivalent(left, right):
    pending = [(0, 0)]
    seen = set(pending)
    for first, second in pending:
        for symbol in range(9):
            left_target = left[first][symbol]
            right_target = right[second][symbol]
            assert (left_target < 0) == (right_target < 0)
            if left_target >= 0:
                pair = (left_target, right_target)
                if pair not in seen:
                    seen.add(pair)
                    pending.append(pair)
    return len(seen)


def default_three_transform(graph, phase, width_parity, allow_suppression=False):
    initial = (0, 1 - width_parity, (0, 0, 0), 0)
    queue = deque([initial])
    seen = {initial}
    arrows = {}
    while queue:
        node = queue.popleft()
        state, parity, history, previous = node
        outgoing = [set() for symbol in range(9)]
        for symbol, target in enumerate(graph[state]):
            if target < 0:
                continue
            lower, source = divmod(symbol, 3)
            assert lower in (0, 1) and source in (0, 1)
            route = history[0] if source else lower
            output = route if (phase + parity - previous) % 2 == 0 else 0
            choices = {0, output} if allow_suppression else {output}
            for choice in choices:
                successor = (target, 1 - parity, history[1:] + (route,), choice)
                outgoing[3 * source + choice].add(successor)
                if successor not in seen:
                    seen.add(successor)
                    queue.append(successor)
        arrows[node] = outgoing
    root = frozenset([initial])
    subsets = [root]
    indices = {root: 0}
    deterministic = []
    for subset in subsets:
        transitions = []
        for symbol in range(9):
            target = frozenset().union(*(arrows[node][symbol] for node in subset))
            if not target:
                transitions.append(-1)
                continue
            if target not in indices:
                indices[target] = len(subsets)
                subsets.append(target)
            transitions.append(indices[target])
        deterministic.append(tuple(transitions))
    return quotient(deterministic)


def default_three_advance(graph, phase, width_parity, allow_suppression=False):
    root = (1 - width_parity) << 4
    nodes = [root]
    indices = {root: 0}
    arrows = []
    for node in nodes:
        state = node >> 5
        parity = (node >> 4) & 1
        previous = (node >> 3) & 1
        register = node & 7
        outgoing = [set() for symbol in range(9)]
        for symbol, target_state in enumerate(graph[state]):
            if target_state < 0:
                continue
            lower, source = divmod(symbol, 3)
            assert lower < 2 and source < 2
            route = (register >> 2) if source else lower
            output = int((phase + parity + previous) % 2 == 0) * route
            next_register = ((register << 1) | route) & 7
            choices = (0, 1) if allow_suppression and output else (output,)
            for choice in choices:
                target = (target_state << 5) | ((1 - parity) << 4) | (choice << 3) | next_register
                if target not in indices:
                    indices[target] = len(nodes)
                    nodes.append(target)
                outgoing[3 * source + choice].add(indices[target])
        arrows.append(outgoing)
    subsets = [frozenset([0])]
    subset_indices = {subsets[0]: 0}
    deterministic = []
    for subset in subsets:
        row = []
        for symbol in range(9):
            target = frozenset(destination for state in subset for destination in arrows[state][symbol])
            if not target:
                row.append(-1)
                continue
            if target not in subset_indices:
                subset_indices[target] = len(subsets)
                subsets.append(target)
            row.append(subset_indices[target])
        deterministic.append(tuple(row))
    return minimize(deterministic)


def default_three_certificate(allow_suppression=False):
    evidence = []
    for phase_offset in range(3):
        for width_parity in (0, 1):
            initial = [(1,) + (-1,) * 8, (2,) + (-1,) * 8,
                       (2, 2, -1, 2, 2, -1, -1, -1, -1)]
            history_graph = register_graph = initial
            counts, compared, positive_rows = [], [], []
            first_zero = (22, 21, 23)[phase_offset] if allow_suppression else 16 - phase_offset
            for order in range(2, first_zero + 2):
                phase = int((order + phase_offset) % 3 != 0)
                history_graph = default_three_transform(history_graph, phase, width_parity, allow_suppression)
                register_graph = default_three_advance(register_graph, phase, width_parity, allow_suppression)
                compared.append(equivalent(history_graph, register_graph))
                assert len(history_graph) == len(register_graph)
                counts.append(len(history_graph))
                if any(target >= 0 and symbol % 3 for row in history_graph
                       for symbol, target in enumerate(row)):
                    positive_rows.append(order)
            zero_pair = [first_zero, first_zero + 1]
            assert max(positive_rows) == zero_pair[0] - 1
            assert history_graph == register_graph == [(0,) + (-1,) * 8]
            evidence.append(dict(phase_offset=phase_offset, width_parity=width_parity,
                                 orders=[2, zero_pair[1]], minimized_states=counts,
                                 equivalent_language_state_pairs=compared,
                                 last_possible_positive_row=max(positive_rows),
                                 final_zero_pair=zero_pair))
    if allow_suppression:
        return dict(status='PASS', uniform_zero_from_row=23, phases=evidence,
                    scope='Two independent exact whole-word transductions prove extinction '
                          'of amplitude-three routing while allowing arbitrary suppression '
                          'of default-positive outputs. Arbitrary-length initial rows have '
                          'two zero sites after the collar. No spatial cutoff, canonical '
                          'sequence data, actual creation-frequency upper bound or convergence claim.')
    return dict(status='PASS', uniform_zero_from_row=16, phases=evidence,
                scope='Two independent exact whole-word transductions prove default-only '
                      'amplitude-three extinction for arbitrary-length initial rows with '
                      'two zero sites after the collar. No spatial cutoff, canonical '
                      'sequence data, actual entrance frequency or convergence claim.')


def amplitude_three_obstruction():
    profiles = [('001011001011', '001011'),
                ('000100010110', '010110'),
                ('000001100110', '010110')]
    routes = [('010011011001', '001001'),
              ('000100010010', '010010'),
              ('001011011011', '011011')]

    def bit(table, row, offset):
        if offset < 0:
            return 0
        prefix, tail = table[row]
        return int(prefix[offset] if offset < 12 else tail[(offset - 12) % 6])

    def profile(row, offset):
        quotient, residue = divmod(row, 3)
        return bit(profiles, residue, offset - 2 * quotient)

    alternate_positive = 0
    for row in range(3):
        for offset in range(-3, 21):
            lower = profile(row - 2, offset)
            source = profile(row - 1, offset)
            route = bit(routes, row, offset)
            assert route == (lower if source == 0 else bit(routes, row, offset - 3))
            gate = (int(row % 3 != 0) + offset - profile(row, offset - 1)) % 2 == 0
            choices = {0} if not gate else {route}
            if gate and profile(row - 1, offset + 2):
                choices.add(bit(routes, row, offset - 1))
            if gate and profile(row - 1, offset + 1):
                choices.add(bit(routes, row, offset - 2))
            output = profile(row, offset)
            assert output in choices
            alternate_positive += int(output == 1 and route == 0)
        assert all(profile(row, offset) == 0 for offset in range(-3, 2))
    assert alternate_positive > 0
    return dict(status='PASS', profiles=profiles, routes=routes,
                checked_row_phases=3, checked_offsets=[-3, 20],
                tail_identity_start=15, tail_period=6,
                row_translation=[3, 2], alternate_positive_cases=alternate_positive,
                scope='An exact prefix and periodic-tail certificate for a persistent '
                      'relaxed amplitude-three history with a zero left boundary. '
                      'The written proof covers all spatial offsets and both collar '
                      'parities. This is not a canonical recurrence counterexample.')


def slow_three_front_certificate():
    profiles = [('000010110010', '000010'), ('011001010110', '011000'),
                ('000001100110', '010001'), ('001000001011', '001100'),
                ('000001100101', '100001'), ('000110000100', '000110')]
    routes = [('000110010110010110010110', '010110'),
              ('011010010010011010011010', '011010'),
              ('000010110110010010010010', '010010'),
              ('011001010010011001001001', '001001'),
              ('000001101101011001011001', '011001'),
              ('001001001011001101101101', '101101')]

    def bit(table, row, offset):
        if offset < 0:
            return 0
        prefix, tail = table[row]
        return int(prefix[offset] if offset < len(prefix)
                   else tail[(offset - len(prefix)) % 6])

    def profile(row, offset):
        quotient, phase = divmod(row, 6)
        return bit(profiles, phase, offset - 2 * quotient)

    for row in range(6):
        for offset in range(-4, 33):
            route = bit(routes, row, offset)
            lower, source = profile(row - 2, offset), profile(row - 1, offset)
            assert route == (bit(routes, row, offset - 3) if source else lower)
            clock = (int(row % 3 != 0) + offset - profile(row, offset - 1)) % 2
            choices = {0} if clock else {route}
            if not clock and profile(row - 1, offset + 2):
                choices.add(bit(routes, row, offset - 1))
            if not clock and profile(row - 1, offset + 1):
                choices.add(bit(routes, row, offset - 2))
            assert profile(row, offset) in choices
        assert all(not profile(row, offset) for offset in range(-4, 1))
    fronts = [next(offset for offset in range(12) if bit(profiles, row, offset))
              for row in range(6)]
    assert fronts == [4, 1, 5, 2, 5, 3]
    delays = []
    for initial_class in range(3):
        pair = []
        for site_parity in (0, 1):
            states = {(0, 0), (0, 1), (1, 0), (1, 1)}
            last_positive = 1
            for order in range(2, 12):
                phase = int((order + initial_class - 1) % 3 != 0)
                states = {(source, choice) for lower, source in states
                          for choice in ({0, lower} if not source and
                                         (phase + site_parity) % 2 == 0 else {0})}
                if any(output for source, output in states):
                    last_positive = order
            assert states == {(0, 0)}
            pair.append(last_positive + 1)
        delays.append(pair)
    assert delays == [[2, 6], [4, 5], [3, 4]]
    return dict(status='PASS', profiles=profiles, routes=routes,
                checked_row_phases=6, checked_offsets=[-4, 32],
                tail_identity_start=27, tail_period=6, row_translation=[6, 2],
                first_positive_offsets=fronts, asymptotic_front_speed='1/3',
                one_offset_delays_even_odd=delays,
                scope='Exact prefix/periodic-tail identities attain the universal '
                      'one-offset drift coefficient 1/3 in the guarded relaxed rule. '
                      'The written proof supplies the infinite induction and rate. '
                      'No canonical realization or global convergence claim.')


def main():
    parser = argparse.ArgumentParser()
    modes = parser.add_mutually_exclusive_group()
    modes.add_argument('--default-three', action='store_true',
                       help='Prove default-only amplitude-three extinction by whole-word automata.')
    modes.add_argument('--creation-three', action='store_true',
                       help='Prove extinction allowing arbitrary deletion of default-positive outputs.')
    modes.add_argument('--slow-three', action='store_true',
                       help='Check the sharp one-third front speed for relaxed amplitude-three routing.')
    arguments = parser.parse_args()
    if not __debug__:
        raise SystemExit('Run without -O; assertions perform the mathematical checks.')
    if arguments.slow_three:
        print(json.dumps(slow_three_front_certificate(), indent=2))
        return
    if arguments.default_three or arguments.creation_three:
        print(json.dumps(default_three_certificate(arguments.creation_three), indent=2))
        return
    expected = [[119, 176, 215, 98, 183, 252, 189, 77, 77, 51, 14, 14, 1],
                [119, 175, 214, 98, 182, 251, 188, 76, 76, 50, 15, 15, 1]]
    evidence = []
    for width_parity in (0, 1):
        pending_graph = obligation_graph = [(0,) * 9]
        stages = []
        for order in range(2, 15):
            phase = int(order % 3 != 0)
            pending_graph = transform(pending_graph, phase, width_parity)
            obligation_graph, nondeterministic, subsets = advance(
                obligation_graph, phase, width_parity)
            compared = equivalent(pending_graph, obligation_graph)
            assert len(pending_graph) == len(obligation_graph) == expected[width_parity][order - 2]
            alphabet = sorted({symbol for row in pending_graph
                               for symbol, target in enumerate(row) if target >= 0})
            if order == 11:
                assert alphabet == [0, 3, 6]
            if order == 14:
                assert pending_graph == obligation_graph == [(0,) + (-1,) * 8]
            stages.append(dict(order=order, minimized_states=len(pending_graph),
                               obligation_nondeterministic_states=nondeterministic,
                               obligation_subset_states=subsets,
                               equivalent_language_state_pairs=compared, alphabet=alphabet))
        evidence.append(dict(width_parity=width_parity, stages=stages))
    print(json.dumps(dict(status='PASS', aligned_initial_order_modulo_three=1,
                          zero_output_rows=[11, 13, 14],
                          phases=evidence,
                          amplitude_three_obstruction=amplitude_three_obstruction(),
                          scope='Two independently implemented exact whole-word transductions '
                                'recognize the same arbitrary-length languages. Their closed '
                                'finite automata prove the ternary identity. Actual recurrence '
                                'application and the finite-window loss use the written proof; '
                                'this program uses no canonical sequence data or spatial cutoff.'),
                     indent=2))


if __name__ == '__main__':
    main()

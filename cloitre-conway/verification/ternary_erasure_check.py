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


def main():
    if not __debug__:
        raise SystemExit('Run without -O; assertions perform the mathematical checks.')
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

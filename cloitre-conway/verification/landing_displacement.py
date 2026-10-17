"""Check selected landing jumps independently of the convergence criterion."""

import argparse
from array import array
import json
from pathlib import Path
import sys

from conway_explore import brent_generate, g_closed, generate, literal_generate


def witness(index, sequence, split, jump):
    return dict(index=index, value=sequence[index], split=split,
                next_point=split + jump, jump=jump)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--limit', type=int, default=2**24)
    parser.add_argument('--output', type=Path)
    arguments = parser.parse_args()
    if not __debug__:
        raise SystemExit('Run without -O; assertions perform the checks.')
    assert 4096 <= arguments.limit < 2**32
    fibonacci = [0, 1]
    while fibonacci[-1] <= arguments.limit:
        fibonacci.append(sum(fibonacci[-2:]))
    sequence = array('I', [0, 1, 1])
    independent_limit = min(arguments.limit, 2**20)
    prefix_splits = array('I', [0, 0, 0])
    prefix_jumps = array('i', [0, 0, 0])
    shells = {}
    order = 3
    for index in range(3, arguments.limit + 1):
        positions = {}
        trajectory = []
        point = index - 1
        while point not in positions:
            assert 1 <= point < index
            positions[point] = len(trajectory)
            trajectory.append(point)
            point = index - sequence[point]
        transient = positions[point]
        period = len(trajectory) - transient
        depth = sequence[index - 1]
        assert depth >= transient
        position = transient + (depth - transient) % period
        split = trajectory[position]
        next_point = trajectory[transient + (position - transient + 1) % period]
        jump = next_point - split
        assert jump == index - sequence[split] - split
        sequence.append(sequence[split] + sequence[index - split])
        if index <= independent_limit:
            prefix_splits.append(split)
            prefix_jumps.append(jump)
        while fibonacci[order + 1] <= index:
            order += 1
        anchor = fibonacci[order]
        previous = fibonacci[order - 1]
        earlier = fibonacci[order - 2]
        assert g_closed(index) <= sequence[index] <= min(index - earlier, anchor)
        if index >= 8:
            assert max(previous, index - previous) <= split <= min(anchor, index - earlier)
        if index >= 65536:
            assert 9 * split > 5 * index and 3 * split < 2 * index
        exponent = (index - 1).bit_length()
        row = shells.setdefault(exponent, dict(
            lower_exclusive=2**(exponent - 1), upper_inclusive=min(2**exponent, arguments.limit),
            count=0, negative_count=0, zero_count=0, positive_count=0,
            max_negative_jump=dict(numerator=0, denominator=1, witness=None),
            max_positive_jump=dict(numerator=0, denominator=1, witness=None),
            max_ratio=dict(numerator=0, denominator=1, witness=None),
            max_period=0, max_transient=0))
        row['count'] += 1
        row['negative_count' if jump < 0 else 'positive_count' if jump > 0 else 'zero_count'] += 1
        row['max_period'] = max(row['max_period'], period)
        row['max_transient'] = max(row['max_transient'], transient)
        for key, numerator in [('max_negative_jump', max(0, -jump)),
                               ('max_positive_jump', max(0, jump)),
                               ('max_ratio', sequence[index])]:
            entry = row[key]
            if numerator * entry['denominator'] > entry['numerator'] * index:
                entry.update(numerator=numerator, denominator=index,
                             witness=witness(index, sequence, split, jump))
        if index % 2**20 == 0:
            print(f'{index:,} terms checked', file=sys.stderr, flush=True)
    assert list(sequence[:independent_limit + 1]) == brent_generate(independent_limit)
    full_orbit_limit = min(arguments.limit, 2**17)
    reference, _, _, reference_splits = generate(full_orbit_limit)
    assert list(sequence[:full_orbit_limit + 1]) == reference
    assert list(prefix_splits[:full_orbit_limit + 1]) == reference_splits
    literal_limit = 4096
    literal, updates = literal_generate(literal_limit)
    assert list(sequence[:literal_limit + 1]) == literal
    selected_literal_updates = 0
    for index in range(3, literal_limit + 1):
        point = index - 1
        for iteration in range(sequence[index - 1]):
            point = index - sequence[point]
            selected_literal_updates += 1
        assert point == prefix_splits[index]
        assert index - sequence[point] - point == prefix_jumps[index]
    assert selected_literal_updates == updates
    for row in shells.values():
        assert row['count'] == row['upper_inclusive'] - row['lower_exclusive']
        assert row['count'] == row['negative_count'] + row['zero_count'] + row['positive_count']
        for key in ('max_negative_jump', 'max_positive_jump', 'max_ratio'):
            entry = row[key]
            entry['decimal'] = entry['numerator'] / entry['denominator']
    report = dict(
        status='Finite exact orbit computation; no extrapolation to a displacement bound or a limit.',
        definition='g=T_n^C(n-1)(n-1); e(n)=T_n(g)-g=n-C(g)-g',
        limit=arguments.limit,
        cycle_selection_and_jump_checked_through=arguments.limit,
        golden_lower_cap_and_selected_capture_checked_through=arguments.limit,
        independent_brent_values_through=independent_limit,
        independent_full_orbit_values_and_splits_through=full_orbit_limit,
        literal_values_selected_splits_and_jumps_through=literal_limit,
        literal_updates=updates,
        shells=list(shells.values()),
        interpretation='A finite shell maximum is not a bound on a limsup. The criterion L<=phi*E applies to infinite tail limsups, not these individual shells.')
    output = json.dumps(report, indent=2) + '\n'
    if arguments.output:
        arguments.output.write_text(output)
    else:
        print(output, end='')


if __name__ == '__main__':
    main()

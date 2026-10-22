import argparse
import json
import struct
from fractions import Fraction
from pathlib import Path


def main():
    if not __debug__:
        raise RuntimeError('certificate checks require enabled assertions')
    parser = argparse.ArgumentParser()
    parser.add_argument('certificate', type=Path)
    arguments = parser.parse_args()
    raw = arguments.certificate.read_bytes()
    width, known, end = struct.unpack_from('<III', raw)
    assert (width, known, end) == (512, 141422079, 1836311902)
    assert len(raw) == 12 + 8 * (end // width + 1)
    lower_source, upper_source = 701408733, 1836311903
    good_first, good_last = 865732608, 867432447
    assert lower_source <= good_first <= good_last < upper_source
    assert 4 * good_last < 5 * good_first
    assert 4 * good_last < 5 * lower_source
    assert 2 * good_last < upper_source
    bound = Fraction(567008869, 866573824)
    outside_bound = Fraction(567563869, 867435520)
    maximum_value, maximum_source = 0, 1
    checked_cells, outside_cells = 0, 0
    for cell, (lower, upper) in enumerate(struct.iter_unpack('<II', memoryview(raw)[12:])):
        assert lower <= upper
        first = max(cell * width, lower_source)
        last = min((cell + 1) * width - 1, end)
        if first > last:
            continue
        checked_cells += 1
        assert upper * bound.denominator <= bound.numerator * first
        if good_first <= first <= last <= good_last:
            continue
        assert last < good_first or first > good_last
        outside_cells += 1
        assert upper * outside_bound.denominator <= outside_bound.numerator * first
        if upper * maximum_source > maximum_value * first:
            maximum_value, maximum_source = upper, first
    assert Fraction(maximum_value, maximum_source) == outside_bound
    epsilon = bound - outside_bound
    bad_mass_fraction = Fraction(5, 9)
    improvement = epsilon * bad_mass_fraction
    assert epsilon > 0 and 0 < bad_mass_fraction <= 1
    print(json.dumps(dict(
        terminal_window=[lower_source, upper_source],
        checked_cells=checked_cells, outside_cells=outside_cells,
        superlevel_container=[good_first, good_last],
        outside_bound=str(outside_bound), outside_bound_witness=[maximum_value, maximum_source],
        previous_bound=str(bound), epsilon=str(epsilon),
        bad_mass_fraction=str(bad_mass_fraction), improvement=str(improvement),
        tail_threshold=upper_source,
        tail_bound=str(bound - improvement), tail_bound_float=float(bound - improvement),
        scope='Exact integer comparisons on an already validated cycle-enclosure '
              'certificate. This program does not validate its input against the '
              'canonical prefix; cycle_enclosure_check.py supplies that separate '
              'check. The written terminal-mass argument supplies the infinite tail.'
    ), indent=2))


if __name__ == '__main__':
    main()

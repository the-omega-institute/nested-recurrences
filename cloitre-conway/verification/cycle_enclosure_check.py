import argparse
import json
from fractions import Fraction
from pathlib import Path

import numpy as np


def main():
    if not __debug__:
        raise RuntimeError('certificate verification requires enabled assertions')
    parser = argparse.ArgumentParser()
    parser.add_argument('values', type=Path)
    parser.add_argument('certificate', type=Path)
    arguments = parser.parse_args()
    raw = np.fromfile(arguments.certificate, dtype='<u4')
    width, known, end = map(int, raw[:3])
    assert 16 <= width <= 65536
    assert 102334155 <= known + 1 <= 165580141
    assert end in (267914295, 1836311902)
    continuation = end == 1836311902
    bounds = raw[3:].reshape(-1, 2)
    cells = len(bounds)
    assert cells == end // width + 1
    known_cells = (known + 1) // width
    assert known + 1 == known_cells * width
    values = np.memmap(arguments.values, dtype='<u4', mode='r')
    known_values = values[:known + 1].reshape(known_cells, width)
    assert np.array_equal(bounds[:known_cells, 0], known_values.min(axis=1))
    assert np.array_equal(bounds[:known_cells, 1], known_values.max(axis=1))
    assert np.all(bounds[:, 0] <= bounds[:, 1])
    levels = cells.bit_length()
    minima = np.full((levels, cells), np.iinfo(np.uint32).max, dtype=np.uint32)
    maxima = np.zeros((levels, cells), dtype=np.uint32)
    minima[0], maxima[0] = bounds[:, 0], bounds[:, 1]
    for level in range(1, levels):
        shift = 1 << (level - 1)
        count = cells - (1 << level) + 1
        if count <= 0:
            break
        minima[level, :count] = np.minimum(minima[level - 1, :count],
                                          minima[level - 1, shift:shift + count])
        maxima[level, :count] = np.maximum(maxima[level - 1, :count],
                                          maxima[level - 1, shift:shift + count])

    def query(first, last):
        assert np.all(first <= last)
        first_cell, last_cell = first // width, last // width
        length = last_cell - first_cell + 1
        level = np.frexp(length)[1].astype(np.int64) - 1
        shift = np.left_shift(1, level)
        right_start = last_cell - shift + 1
        return (np.minimum(minima[level, first_cell], minima[level, right_start]),
                np.maximum(maxima[level, first_cell], maxima[level, right_start]))

    fibonacci = [0, 1]
    while fibonacci[-1] <= end:
        fibonacci.append(sum(fibonacci[-2:]))
    fib = np.array(fibonacci, dtype=np.int64)
    parent_cell = np.arange(known_cells, cells, dtype=np.int64)
    first = parent_cell * width
    last = np.minimum((parent_cell + 1) * width - 1, end)
    order_first = np.searchsorted(fib, first, side='right') - 1
    order_last = np.searchsorted(fib, last, side='right') - 1
    left = np.maximum(fib[order_first - 1], first - fib[order_first - 1])
    right = np.minimum(fib[order_last], last - fib[order_last - 2])
    left = np.maximum(left, 5 * first // 9 + 1)
    right = np.minimum(right, (2 * last - 1) // 3)
    for iteration in range(100):
        assert np.all(right // width < parent_cell)
        lower, upper = query(left, right)
        left = np.maximum(left, first - upper)
        right = np.minimum(right, last - lower)
        assert np.all(left <= right)
    lower_readout = np.empty(len(first), dtype=np.uint32)
    upper_readout = np.empty(len(first), dtype=np.uint32)
    readout_cells = 0
    for start in range(0, len(first), 256):
        stop = min(start + 256, len(first))
        counts = right[start:stop] // width - left[start:stop] // width + 1
        offsets = np.concatenate(([0], np.cumsum(counts)))
        parent = np.repeat(np.arange(start, stop), counts)
        argument_cell = (np.arange(offsets[-1]) - np.repeat(offsets[:-1], counts)
                         + np.repeat(left[start:stop] // width, counts))
        assert np.all(argument_cell < parent_cell[parent])
        argument_first = np.maximum(left[parent], argument_cell * width)
        argument_last = np.minimum(right[parent], (argument_cell + 1) * width - 1)
        complement_first = first[parent] - argument_last
        complement_last = last[parent] - argument_first
        assert np.all(complement_last // width < parent_cell[parent])
        lower, upper = query(complement_first, complement_last)
        lower_readout[start:stop] = np.minimum.reduceat(
            bounds[argument_cell, 0] + lower, offsets[:-1])
        upper_readout[start:stop] = np.maximum.reduceat(
            bounds[argument_cell, 1] + upper, offsets[:-1])
        readout_cells += int(offsets[-1])
    shifted = first.astype(np.uint64) + 1
    radicand = 5 * shifted * shifted
    root = np.sqrt(radicand).astype(np.uint64)
    root += ((root + 1) * (root + 1) <= radicand)
    root -= (root * root > radicand)
    assert np.all(root * root <= radicand)
    assert np.all((root + 1) * (root + 1) > radicand)
    golden = (root - shifted) // 2
    lower_readout = np.maximum(lower_readout, golden)
    scalar_cap = (np.array([
        42085100 * int(source) // 64203827 if source_first < fib[41]
        else 19580084505646265 * int(source) // 29872542956223744
        for source_first, source in zip(first, last)], dtype=np.uint32) if continuation
        else 42085100 * last // 64203827)
    upper_readout = np.minimum(upper_readout, scalar_cap)
    upper_readout = np.minimum(upper_readout,
                              np.minimum(last - fib[order_last - 2], fib[order_last]))
    assert np.array_equal(bounds[known_cells:, 0], lower_readout)
    assert np.array_equal(bounds[known_cells:, 1], upper_readout)
    if continuation:
        row_bounds = {}
        for order in range(41, 46):
            in_row = (last >= fib[order]) & (first < fib[order + 1])
            source_first = np.maximum(first[in_row], fib[order])
            upper_row = upper_readout[in_row].astype(np.int64)
            witness = int(np.argmax(upper_row / source_first))
            numerator = int(upper_row[witness])
            denominator = int(source_first[witness])
            assert np.all(upper_row * denominator <= numerator * source_first)
            row_bounds[order] = Fraction(numerator, denominator)
        tail_bound = max(row_bounds[44], row_bounds[45])
        old = Fraction(19580084505646265, 29872542956223744)
        assert tail_bound < old
        print(json.dumps(dict(
            cell_width=width, known_prefix_through=known, derived_through=end,
            known_cells_verified=known_cells, derived_cells_verified=len(first),
            independent_enclosure_queries=100 * len(first),
            readout_cells_verified=readout_cells,
            row_bounds={order: str(value) for order, value in row_bounds.items()},
            tail_threshold=int(fib[44]), tail_bound=str(tail_bound),
            tail_bound_float=float(tail_bound), improvement=float(old - tail_bound),
            scope='Independent sparse-table verification of every cell from the '
                  'retained canonical prefix, using the previously proved tail '
                  'cap. The finite-window argument at order44 supplies the '
                  'infinite conclusion.'), indent=2))
        return
    row = last >= fib[41]
    source_first = np.maximum(first[row], fib[41])
    upper_row = upper_readout[row].astype(np.int64)
    witness = int(np.argmax(upper_row / source_first))
    numerator, denominator = int(upper_row[witness]), int(source_first[witness])
    assert np.all(upper_row * denominator <= numerator * source_first)
    row_bound = Fraction(numerator, denominator)
    assert Fraction(int(fib[41]), int(fib[42])) <= row_bound
    old = Fraction(42085100, 64203827)
    assert row_bound < old
    tail_bound = Fraction(5, 9) * row_bound + Fraction(4, 9) * old
    print(json.dumps(dict(
        cell_width=width, known_prefix_through=known, derived_through=end,
        known_cells_verified=known_cells,
        derived_cells_verified=len(first),
        independent_enclosure_queries=100 * len(first),
        readout_cells_verified=readout_cells,
        row41_bound=str(row_bound), tail_bound=str(tail_bound),
        tail_bound_float=float(tail_bound), improvement=float(old - tail_bound),
        scope='Independent NumPy reductions and sparse-table range queries '
              'verify every cell against earlier cells, including 100 cycle '
              'enclosure rounds and all final readout slices. No canonical '
              'values beyond the retained prefix are generated.'), indent=2))


if __name__ == '__main__':
    main()

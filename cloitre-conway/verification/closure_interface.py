"""Exact checks for the generic reflection-window closure interface."""

from fractions import Fraction
import json


def zero(size):
    return (Fraction(0),) * size


def add(left, right):
    return tuple(a + b for a, b in zip(left, right))


def sub(left, right):
    return tuple(a - b for a, b in zip(left, right))


def scale(value, factor):
    return tuple(factor * a for a in value)


def variable(size, index):
    result = list(zero(size))
    result[index] = Fraction(1)
    return tuple(result)


def alternating(values):
    result = zero(len(values[0]))
    for index, value in enumerate(values):
        result = add(result, scale(value, Fraction(1 if index % 2 == 0 else -1)))
    return result


def rank(rows):
    if not rows:
        return 0
    matrix = [list(row) for row in rows]
    height, width = len(matrix), len(matrix[0])
    pivot = 0
    for column in range(width):
        candidate = next((row for row in range(pivot, height)
                          if matrix[row][column]), None)
        if candidate is None:
            continue
        matrix[pivot], matrix[candidate] = matrix[candidate], matrix[pivot]
        divisor = matrix[pivot][column]
        matrix[pivot] = [entry / divisor for entry in matrix[pivot]]
        for row in range(height):
            if row == pivot or not matrix[row][column]:
                continue
            factor = matrix[row][column]
            matrix[row] = [a - factor * b
                           for a, b in zip(matrix[row], matrix[pivot])]
        pivot += 1
        if pivot == height:
            break
    return pivot


def build_payload(period):
    size = period + 1
    t = variable(size, 0)
    start = variable(size, 1)
    defects = [variable(size, 2 + index) for index in range(period - 1)]
    offsets = [start]
    for index in range(period - 1):
        offsets.append(add(sub(t, offsets[-1]), defects[index]))
    last_defect = sub(add(start, offsets[-1]), t)
    defects.append(last_defect)
    closure = add(sub(t, offsets[-1]), last_defect)
    return t, offsets, defects, closure


def check_period(period):
    t, offsets, defects, closure = build_payload(period)
    size = period + 1
    assert closure == offsets[0]
    for index in range(period):
        next_offset = offsets[(index + 1) % period]
        transition = add(sub(t, offsets[index]), defects[index])
        assert transition == next_offset
    alternating_defects = alternating(defects)
    if period % 2:
        assert scale(offsets[0], 2) == add(t, alternating_defects)
    else:
        assert alternating_defects == zero(size)
    features = [t, *offsets, *defects]
    assert rank(features) == size
    return {
        "period": period,
        "payload_dimension_including_scale": size,
        "additional_coordinates_beyond_scale": period,
        "alternating_defect_identity": "fixed-point" if period % 2 else "translation",
        "feature_rank": rank(features),
    }


def main():
    rows = [check_period(period) for period in range(1, 9)]
    five = rows[4]
    assert five["payload_dimension_including_scale"] == 6
    assert five["additional_coordinates_beyond_scale"] == 5
    assert rows[1]["alternating_defect_identity"] == "translation"
    dimensions = {f"p={row['period']}": row["payload_dimension_including_scale"]
                  for row in rows}
    additional = {f"p={row['period']}": row["additional_coordinates_beyond_scale"]
                  for row in rows}
    ranks = {f"p={row['period']}": row["feature_rank"] for row in rows}
    print(json.dumps({
        "status": "passed",
        "periods_checked": [row["period"] for row in rows],
        "payload_dimension_including_scale": dimensions,
        "additional_coordinates_beyond_scale": additional,
        "feature_rank": ranks,
        "five_window_payload": {
            "input": ["t", "u0", "e0", "e1", "e2", "e3"],
            "derived": ["u1", "u2", "u3", "u4", "e4"],
            "additional_coordinates_beyond_scale": five["additional_coordinates_beyond_scale"],
        },
        "scope": "Exact symbolic affine closure; branch inequalities and family-specific selectors remain separate.",
    }, indent=2))


if __name__ == "__main__":
    main()

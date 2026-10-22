import argparse
import json
import math
from decimal import Decimal, getcontext
from pathlib import Path


def main():
    if not __debug__:
        raise RuntimeError('arithmetic checks require enabled assertions')
    parser = argparse.ArgumentParser()
    parser.add_argument('--figure', type=Path)
    arguments = parser.parse_args()
    getcontext().prec = 80
    one = Decimal(1)
    alpha = (Decimal(5).sqrt() - one) / 2
    phi = one / alpha
    ratio = phi.sqrt().sqrt()
    defect = alpha * alpha
    plateau = alpha * ratio
    knee = defect + plateau
    transition = alpha * knee + defect * ratio
    maximum = ratio / (alpha + ratio)
    tolerance = Decimal('1e-65')

    def profile(point):
        exponent = math.floor(math.log(float(point)) / math.log(float(ratio)))
        anchor = ratio ** exponent
        while point < anchor:
            exponent -= 1
            anchor = ratio ** exponent
        while point >= anchor * ratio:
            exponent += 1
            anchor = ratio ** exponent
        return min(point - defect * anchor, plateau * anchor)

    checked = 0
    maximum_error = Decimal(0)
    for exponent in range(-24, 25):
        scale = ratio ** exponent
        for region, left, right in ((1, one, knee), (2, knee, transition),
                                    (3, transition, ratio)):
            for step in range(33):
                source = left + (right - left) * step / 32
                if region == 1:
                    selected = alpha * source
                    partner = source - alpha * profile(source)
                elif region == 2:
                    selected = alpha * knee
                    partner = source - defect * ratio
                else:
                    selected = source - defect * ratio
                    partner = selected
                source *= scale
                selected *= scale
                partner *= scale
                residuals = [source - profile(selected) - partner,
                             source - profile(partner) - selected,
                             profile(selected) + profile(source - selected)
                             - profile(source)]
                error = max(abs(value) / source for value in residuals)
                maximum_error = max(maximum_error, error)
                assert error < tolerance
                native_anchor = phi ** (exponent // 4)
                if step == 32 and region == 3 and exponent % 4 == 3:
                    native_anchor *= phi
                native_lower = max(alpha * native_anchor,
                                   source - alpha * native_anchor)
                native_upper = min(native_anchor, source - defect * native_anchor)
                for point in (selected, partner):
                    assert point > 5 * source / 9
                    assert point < 2 * source / 3
                    assert native_lower - tolerance * source <= point
                    assert point <= native_upper + tolerance * source
                assert alpha * source - tolerance * source <= profile(source)
                assert profile(source) <= maximum * source + tolerance * source
                assert profile(source) <= min(native_anchor,
                                              source - defect * native_anchor) + tolerance * source
                checked += 1
    assert alpha < maximum < Decimal(13) / 20
    knee_partner = knee - defect * ratio
    phase_gap = profile(knee) - profile(knee_partner) - profile(knee - knee_partner)
    exact_gap = alpha ** 4 * (ratio - one)
    assert exact_gap > 0 and abs(phase_gap - exact_gap) < tolerance
    print(json.dumps(dict(
        sources_checked=checked, precision_digits=80,
        maximum_relative_residual=str(maximum_error), maximum_ratio=str(maximum),
        knee_phase_gap=str(exact_gap),
        scope='Finite high-precision checks of all three explicit selectors, '
              'their cycles/readouts and capture bounds. The written proof '
              'establishes the construction for all positive reals; these '
              'checks alone do not.'), indent=2))
    if arguments.figure:
        import matplotlib
        import matplotlib.pyplot as plt

        matplotlib.rcParams.update({'svg.fonttype': 'none',
                                    'svg.hashsalt': 'continuous-cycle-profile',
                                    'font.size': 11})
        figure, axes = plt.subplots(figsize=(9.6, 4.3), layout='constrained')
        for exponent in range(4):
            scale = ratio ** exponent
            sources = [scale * (one + (knee - one) * step / 200)
                       for step in range(201)]
            sources += [scale * (knee + (ratio - knee) * step / 200)
                        for step in range(1, 201)]
            axes.plot([float(source) for source in sources],
                      [float(profile(source) / source) for source in sources],
                      color='#245fa3', linewidth=2.4,
                      label='Relaxed A(x)/x' if exponent == 0 else None)
        axes.axhline(float(alpha), color='#777777', linestyle='--', linewidth=1.2,
                     label='Golden proportion')
        bound = 567008869 / 866573824
        axes.axhline(bound, color='#a35b27', linestyle=':', linewidth=1.5,
                     label='Canonical tail bound')
        axes.set(xlim=(1, float(phi)), ylim=(float(alpha) - .002, bound + .002),
                 xlabel='Real source x in one golden-scale block', ylabel='Ratio',
                 title='Continuous relaxed profile: persistent oscillations')
        axes.set_xticks([float(ratio ** exponent) for exponent in range(5)],
                        ['1', 'q', 'q²', 'q³', 'φ'])
        axes.spines[['right', 'top']].set_visible(False)
        axes.grid(axis='y', color='#e5e5e5', linewidth=.6)
        axes.legend(loc='center left', bbox_to_anchor=(1.01, .5),
                    frameon=False, fontsize=9)
        figure.savefig(arguments.figure, metadata={'Date': None}
                       if arguments.figure.suffix == '.svg' else None, dpi=180)
        plt.close(figure)


if __name__ == '__main__':
    main()

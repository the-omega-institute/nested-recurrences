# Exact tail certificate through F45

For the canonical variable-depth Conway sequence defined in the
[Conway guide](../../README.md), the exact maximum on `[F43,F45)` is
`367631381/561724478`, attained only at `n=561724478`.
The [finite-window maximum principle](../../dispersion.md#a-finite-window-maximum-principle)
extends the same bound to every `n>=F43`.

Cloitre's hash-table evaluator `cmax.c`, its output `cmax45.txt` and
separate array checker `verify45.py` are preserved here. `verify_brent.cpp`
regenerates the sequence independently from its initial values, using
Brent cycle detection and the exact prescribed iteration depth. It reads
no author-generated array. It also checks values and selected splits
against literal nesting through 4096, records exact Fibonacci-block maxima,
and checks negative selected-jump maxima on dyadic shells through 2^28.

## Reproduce

Use a C++17 compiler and Python 3. Do not disable assertions in Python.
The full independent run stores one 32-bit value per index, about 4.6 GB.
Check available memory before running it. Its progress is printed to stderr.

```sh
c++ -O3 -std=c++17 -Wall -Wextra -Werror verify_brent.cpp -o /tmp/conway-brent
/tmp/conway-brent 1048576 > /tmp/conway-prefix.json
/tmp/conway-brent 1134903170 > /tmp/conway-F45.json
```

The first run checks a small prefix, and does not reach the certificate
interval. The second checks all 701408733 indices in
`[433494437,1134903170)`. Compare its complete JSON with the `result` object in
`independent.json`, which also records the evaluator source hash.
All finite comparisons and maxima use integer cross products. The reported
FNV-1a fingerprint is a diagnostic of the regenerated sequence, not a proof.

To replay Cloitre's original route and check its generated array:

```sh
cc -O2 cmax.c -o /tmp/conway-cmax -lm
/tmp/conway-cmax 1134903170 - 0 /tmp/conway-C45.bin
python3 verify45.py /tmp/conway-C45.bin 43 561724478 367631381
```

The NumPy checker needs NumPy and prints violation/equality counts. Its
original version does not turn a violation into a nonzero exit status, so
read those counts: expected zero violations and exactly one equality.
The independent Brent program returns a nonzero status on a violated
inequality. The raw array is regenerable and is not stored in this repository.

This certificate verifies a finite premise of an infinite-tail upper bound.
It does not prove the full golden-ratio limit. Stronger later bounds in the
research notes remain separate from this standalone exact two-block check.

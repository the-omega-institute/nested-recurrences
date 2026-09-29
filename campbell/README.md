# Campbell's variable-depth recurrence

The [PDF note](note.pdf) and [LaTeX source](note.tex) prove global
well-definedness, the explicit power-of-three formula, the sharp four-step
transient bound, the eventual cycle classification and the asymptotic ratio
bounds for the recurrence proposed by John M. Campbell.

The note has no author byline. It acknowledges Campbell's proposal and
Cloitre's discussion of stabilization, and discloses AI assistance.

## Reproduce

With Python 3.10 or newer, from this directory:

```sh
python3 check_proof.py
python3 explore.py
```

Run without `-O` or `PYTHONOPTIMIZE`. Both programs use only the standard
library. The first verifies 12 table rows, 72 transitions and 146 feasible
affine transition branches by exact rational Fourier–Motzkin elimination.
The second compares 1,000,000 recursive terms with the formula and independently
performs literal nesting through 5,000 terms. Expected output is recorded in
[proof-check.json](proof-check.json) and [results.json](results.json).

The sequence SHA-256, using comma-separated decimal ASCII without a trailing
comma or newline, is
`819d3a0632427cefca525a96b7d498c453586e8ae2c93882520231aad8f4a801`.

To rebuild the PDF with a standard TeX installation:

```sh
pdflatex -interaction=nonstopmode -halt-on-error note.tex
pdflatex -interaction=nonstopmode -halt-on-error note.tex
```

Tectonic can also compile the source. The committed PDF is the previously
verified three-page unsigned note. The written induction and arithmetic
certificate are distinct from Lean formalization, which is not included.

# Campbell's variable-depth recurrence

[Back to the research overview](../README.md) · [Current research status](../STATUS.md)

## Read the proof

**[Open the three-page proof (PDF)](note.pdf).** No software or GitHub account
is needed. Read it in GitHub's preview, or use **Download raw file** (the
download-arrow button) to save a copy for reading or printing.

The note proves global
well-definedness, the explicit power-of-three formula, the sharp four-step
transient bound, the eventual cycle classification and the asymptotic ratio
bounds for the recurrence proposed by John M. Campbell.

The main result is an explicit formula organized by powers of three. The proof
then explains why the inner orbit reaches a fixed point or a two-cycle after
at most four transient steps. The final consequences include the dilation
identity and the lower and upper asymptotic ratios.

You can send comments in the existing email thread; no GitHub workflow is
required. For the second example, continue to the
[Conway research guide](../cloitre-conway/README.md).

## Optional computational checks

The [LaTeX source](note.tex), Python programs and recorded data support the PDF;
you do not need them to read the argument. The note remains unsigned and retains
its acknowledgements and research-practice disclosure.

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

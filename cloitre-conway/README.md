# Cloitre's variable-depth Conway candidate

[Research overview](../README.md) · [Current status](../STATUS.md)

## Reading route

1. **[Global golden structure](golden-proof.md):** the main theorem. Start with
   its result list, then Sections 4 and 6 for the inductions and Section 7 for
   the exact finite premises.
   Section 8 shortens the propagation window, improves the tail bound, and
   reduces the limsup to a decreasing family of exact finite-window maxima.
2. **[Fibonacci collars](fibonacci-collars.md):** consequences near Fibonacci
   indices, all-cycle period bounds, five-offset classification and convergence
   in sublinear neighborhoods.
   Section 6 propagates exact collars from two seeds and gives the complete
   fixed-point/two-cycle classification throughout a wider certified band.
3. **[Foundations](proof.md):** the recurrence definition, well-definedness,
   elementary ratio bounds, finite-window propagation and cycle entry.
4. **[Supporting arithmetic and numerical audit](landing.md):** the exact carry
   formula, the infinite equality-set arithmetic lemma, a landing criterion,
   and corrections to the decay observations.

The notes display directly as web pages. No software or GitHub account is
needed. Full ratio convergence and decay remain open; the former equality-set
and Fibonacci landing problems are proved in the global note.
Comments and proposed arguments can be shared in our existing email thread.

## Optional computational checks

Programs and compact recorded evidence are grouped in [verification/](verification/).
With Python 3.10 or newer, from the repository's main folder:

```sh
python3 scripts/verify.py
```

The five checks cover Campbell's symbolic and sequence proofs, the independent
Conway evaluators, the golden theorem's finite premises and the collar diagnostics.
They compare exact JSON output and source hashes with committed evidence.
Run without `-O` or `PYTHONOPTIMIZE`; only the standard library is needed.

For just the original Conway computation, from this directory:

```sh
python3 verification/conway_explore.py --output replay.json
```

The default limit is 1,048,576, with full-orbit and Brent evaluators and a separate
literal check through 4096. [Recorded output](verification/conway-results.json)
contains finite-window certificates, equality corrections and orbit witnesses.
Its historical conjecture labels describe that experiment's original scope;
the global note supplies the subsequent proofs.

The optional larger [audit](verification/landing_audit.py) reaches
F_36=14,930,352 and tests three shifted variants, using compact sequence storage.
Run `python3 scripts/verify.py --extended` from the repository's main folder
to replay and compare it too. The stored output remains the original finite
audit; it supplies no proof of a limit or a universal shifted-family law.

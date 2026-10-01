# Cloitre's variable-depth Conway recurrence

[Project home](../README.md) · [Current status](../STATUS.md)

## Definition

Set C(1)=C(2)=1. For n>=3, let T_n(x)=n-C(x), start at x_0=n-1,
and use exactly C(n-1) iterations:

$$
g=T_n^{\,C(n-1)}(n-1),\qquad C(n)=C(g)+C(n-g).
$$

The first terms are 1, 1, 2, 3, 3, 4, 5, 5, 6, 7. Benoît Cloitre
proposed this candidate. Its inner orbit can have longer cycles than
Campbell's recurrence, so the selected phase can retain information
beyond parity.

## Start with these proofs

1. **[Global golden structure](golden-proof.md).** The main theorem:
   C(n)>=floor((n+1)/phi), the exact equality set, Fibonacci values and
   orbit landing, an upper cap, and liminf C(n)/n=1/phi.
   Its induction uses explicitly verified finite premises.
2. **[Fibonacci orbit bounds](fibonacci-collars.md).** All-cycle capture,
   nearby cycle classification, and ratio convergence within sublinear-width
   neighborhoods of Fibonacci indices.
3. **[Exact collars and phases](exact-collars.md).** Wider exact bands,
   saturation, the prescribed positive-collar phase, and eventual linearity
   at every fixed positive offset.

The full limit C(n)/n -> 1/phi and its decay rate remain open. The
[dispersion note](dispersion.md) gives a precise conditional route to an
upper rate and explains the remaining uniform inequality.

Everything can be read in your browser. No programming knowledge or GitHub
account is needed. The proof notes contain the full arguments; the programs
and JSON files are optional supporting evidence.

## Technical research map

Choose the topic you need; there is no need to read every note in order.

| Question | Note | Depends on |
|---|---|---|
| Is the sequence well defined, and does its depth reach a cycle? | [Foundations](proof.md) | The definition |
| What global golden bounds and Fibonacci identities are proved? | [Global golden structure](golden-proof.md) | Foundations and explicit finite certificates |
| How are cycles captured near Fibonacci indices? | [Orbit bounds](fibonacci-collars.md) | Global golden structure |
| Which nearby values, cycles, and selected phases are exact? | [Exact collars](exact-collars.md) | Capture and stated finite seeds |
| What closes a local reflection window, and what phase information does an output need? | [Profiles and five-window closure](five-window-closure.md) | Global structure and profile identities |
| Can candidate cycles be reconstructed and qualified? | [Inverse reconstruction](inverse-reconstruction.md) | Reflection-window equations |
| How much information is shared between recursive rows? | [Recursive descent](recursive-descent.md) | Inverse reconstruction |
| What would prove a global decay rate, and why are static collars insufficient? | [Martingales and dispersion](dispersion.md) | Profile identity and additive child blocks |
| Does the same finite encoding work for Campbell's example? | [Campbell scale memory](../campbell/scale-memory.md) | Campbell's explicit formula |
| What arithmetic supports the global induction and shifted-family tests? | [Supporting arithmetic and audit](landing.md) | Foundations |

The local interface theorems state exactly which context is supplied.
A candidate geometric cycle, a finite numerical test, and an actual selected
recursive orbit are distinct objects. The [status page](../STATUS.md) tracks
the unresolved full-interface and asymptotic questions.

Previously shared anchors in the original collar note still point to their
new topic sections. Exact revision links continue to show the cited version.

## Optional computational checks

Programs and compact evidence are in [verification/](verification/).
From the repository root, with Python 3.10 or newer:

```sh
python3 scripts/verify.py
```

This reruns eight checks and compares exact JSON output and source hashes.
Only the standard library is needed. Run without `-O` or
`PYTHONOPTIMIZE`; assertions perform mathematical checks.
See the [verification guide](../CONTRIBUTING.md#reproduce-the-evidence).

For the original independent Conway calculation alone, from this directory:

```sh
python3 verification/conway_explore.py
```

The default limit is 1,048,576, with full-orbit and Brent evaluators and a
separate literal check through 4096. [Recorded output](verification/conway-results.json)
contains certificates, equality corrections, and orbit witnesses. Historical
conjecture labels describe the original experiment; current theorem status
is given in the proof notes.

The optional larger [audit](verification/landing_audit.py) reaches
F_36=14,930,352 and checks three shifted variants using compact storage.
Use `python3 scripts/verify.py --extended` from the root to replay it.
Its finite data supplies no proof of a limit or a universal shifted-family law.

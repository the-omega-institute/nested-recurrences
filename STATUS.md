# Results and open questions

[Project home](README.md) · [Definitions and context](GENERAL.md)

**Campbell's recurrence is solved. Cloitre's full golden-ratio limit is open.**
This page summarizes the current results;
the linked notes give exact hypotheses, thresholds, and finite premises.

## Campbell: complete solution

The [three-page proof](campbell/note.pdf) gives an explicit formula on
power-of-three intervals. Every inner orbit reaches a fixed point or a
two-cycle after at most four transient steps. The lower and upper limiting
ratios are respectively 2/5 and 3/4, so the ratio does not converge.
The written proof is supported by exact symbolic and independent sequence
checks. The [Campbell guide](campbell/README.md) explains the formula.

## Cloitre: established results

Write C for Cloitre's sequence, F_k for the Fibonacci numbers, and
alpha=1/phi=(sqrt(5)-1)/2. These results concern the precise starting point
and iteration depth in [the definition](cloitre-conway/README.md#definition).

| Result | Proof |
|---|---|
| The sequence is well defined; its prescribed depth reaches an inner cycle. | [Foundations](cloitre-conway/proof.md) |
| C(n)>=floor(alpha(n+1)), C(F_k)=F_(k-1), and liminf C(n)/n=alpha. The exact equality set and global upper bounds are proved. | [Global golden structure](cloitre-conway/golden-proof.md) |
| The ratio converges to alpha in neighborhoods of Fibonacci indices whose width is sublinear in the index. Exact nearby values and selected phases are known, including a growing constant band below each Fibonacci index. | [Orbit bounds](cloitre-conway/fibonacci-collars.md) · [Exact neighborhoods](cloitre-conway/exact-collars.md) |
| Local recursive interfaces and variance estimates are proved under explicit context and domain hypotheses. They give partial routes toward convergence; the uniform dispersion inequality remains open. | [Technical research map](cloitre-conway/README.md#technical-research-map) |

The global induction and some exact-neighborhood results are
**computer-assisted proofs**: an infinite argument uses explicit finite
premises checked by independent programs. Finite tests of additional
conjectures remain finite observations. No Lean formalization is included.

## Questions that remain open

1. **Convergence and decay over all integers.** Prove C(n)/n -> alpha,
   including the interiors of the Fibonacci blocks. The
   [dispersion note](cloitre-conway/dispersion.md) gives a conditional decay
   theorem; its required uniform inequality is still open. A matching
   lower bound for maxima is a separate question.
2. **The full recursive interface.** Determine what scale, position,
   profile, branch, and phase information suffices beyond the exact
   Fibonacci neighborhoods. Five digit labels or a candidate geometric
   cycle alone do not determine the actual selected recursive orbit.
   Actual nesting must also generate the profiles used by the
   [local decoders](cloitre-conway/recursive-descent.md#cap4-query-profiles-and-the-information-they-carry).
3. **Inner dynamics between Fibonacci indices.** Control periods,
   landing times, and selected phases in the wider block interiors.

An [explicit nonconvergent extension](cloitre-conway/dispersion.md#exact-small-cap-closure-still-does-not-force-convergence)
preserves arbitrarily late actual prefixes, exact small-cap closure and
cap-dependent dispersion. These premises alone do not prove convergence;
actual nesting outside those neighborhoods must also be used.

## Encoding comparison and related families

The [technical research map](cloitre-conway/README.md#technical-research-map)
collects the local-cycle, recursive-interface, and digit-encoding results.
The [Campbell comparison](campbell/scale-memory.md) explains why short inner
cycles need not give a recognizer with constant memory. The corresponding
upper bound for Cloitre's full sequence graph remains open.

Shifted Conway/Mallows variants remain finite observations under their
stated initial conditions; see the [supporting audit](cloitre-conway/landing.md).
Literature review, a manuscript, and formalization are separate milestones.

[CONTRIBUTING.md](CONTRIBUTING.md) explains verification and the PR workflow.
Current proofs are maintained by topic; superseded versions live in Git
history. Historical labels in saved computations retain their original scope.

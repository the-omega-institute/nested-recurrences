# Results and open questions

[Project home](README.md) · [Definitions and context](GENERAL.md)

Campbell's recurrence has a complete solution. Cloitre's recurrence has
proved global bounds and exact Fibonacci structure, but its full ratio
limit and decay rate remain open. This page summarizes the current results;
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
| Local profile equations and qualified cycle reconstruction are proved. Exact small-defect neighborhoods close recursively; every bounded cap defect stays near a Fibonacci index. | [Closure](cloitre-conway/five-window-closure.md) · [Reconstruction](cloitre-conway/inverse-reconstruction.md) · [Exact neighborhoods](cloitre-conway/exact-collars.md) · [Cap budget](cloitre-conway/recursive-descent.md#a-quadratic-enclosure-for-every-bounded-cap-level) |
| Given lower profiles and a certified entrance into the local orbit, an arithmetic decoder determines the actual child terms with small working memory. Those supplied inputs remain hypotheses of the theorem. | [Modular decoder](cloitre-conway/recursive-descent.md#a-modular-symbolic-selector-with-small-working-memory) |
| Given ordered point golden defects and the inverse parameters, an odd window has a unique numeric reconstruction; an even window has at most three. Supplying and qualifying these integers, and certifying actual selection, remain separate tasks. | [Golden-defect decoder](cloitre-conway/inverse-reconstruction.md#golden-defect-words-give-a-uniform-cyclic-decoder) · [Campbell's sharp even example](campbell/scale-memory.md#golden-defect-words-and-the-period-two-interface) |
| Variance estimates are proved in specified Fibonacci neighborhoods, including a bound whose horizon grows logarithmically with the cap defect. They do not yet establish dispersion uniformly over wider blocks. | [Dispersion](cloitre-conway/dispersion.md) · [Logarithmic horizon](cloitre-conway/dispersion.md#a-logarithmic-horizon-from-one-retained-child) |

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
3. **Inner dynamics between Fibonacci indices.** Control periods,
   landing times, and selected phases in the wider block interiors.

An [explicit nonconvergent extension](cloitre-conway/dispersion.md#exact-small-cap-closure-still-does-not-force-convergence)
preserves arbitrarily late actual prefixes, exact small-cap closure and
cap-dependent dispersion. These premises alone do not prove convergence;
actual nesting outside those neighborhoods must also be used.

## Encoding comparison and related families

The encoding comparison asks how much memory is needed to recognize values
and recursive choices from canonical Fibonacci digits. Short inner cycles
do not imply constant memory. Exact memory orders are proved for the stated
Campbell diagnostic and Cloitre's bounded-cap graphs; the corresponding
upper bound for Cloitre's full sequence graph remains open. Read the
[Campbell theorem](campbell/scale-memory.md) and
[Cloitre theorem](cloitre-conway/five-window-closure.md#exact-state-bit-order-for-every-bounded-cap-graph)
for the recognition models and hypotheses.

Both families have proved feature interactions on the five legal canonical
digit patterns. This is a separate question from an orbit having five steps:
the digit labels alone do not determine the recursive state. Read the
[Cloitre construction](cloitre-conway/exact-collars.md#a-persistent-interaction-on-canonical-index-words)
and [Campbell comparison](campbell/scale-memory.md#five-pattern-interaction-on-ternary-scale-interiors).

Shifted Conway/Mallows variants remain finite observations under their
stated initial conditions; see the [supporting audit](cloitre-conway/landing.md).
Literature review, a manuscript, and formalization are separate milestones.

[CONTRIBUTING.md](CONTRIBUTING.md) explains verification and the PR workflow.
Current proofs are maintained by topic; superseded versions live in Git
history. Historical labels in saved computations retain their original scope.

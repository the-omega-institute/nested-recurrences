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
| C(n)>=floor(alpha(n+1)), the equality set is classified, C(F_k)=F_(k-1), and liminf C(n)/n=alpha. A global upper cap and a certified eventual bound C(n)/n<=8900/13459 are also proved. | [Global golden structure](cloitre-conway/golden-proof.md) |
| The ratio converges to alpha in neighborhoods of Fibonacci indices whose width is sublinear in the index. Exact nearby values and selected phases are known, including a growing constant band below each Fibonacci index. | [Orbit bounds](cloitre-conway/fibonacci-collars.md) · [Exact neighborhoods](cloitre-conway/exact-collars.md) |
| Five-window profile equations and qualified reconstruction results are proved. A growing band with cap defects0 or1 has exact recursive child gaps; supplying order and gaps removes residual selector labels there. A unit defect follows a single first-child spine. | [Closure](cloitre-conway/five-window-closure.md) · [Reconstruction](cloitre-conway/inverse-reconstruction.md) · [Descent](cloitre-conway/recursive-descent.md) |
| Exact martingale identities reduce a possible decay proof to a uniform dispersion inequality. A phase-free quadratic lower bound is proved in the zero/unit-defect band; the global inequality remains open. Explicit alternative sequences show why finite prefixes, golden bounds, and eventual fixed neighborhoods alone cannot prove convergence. | [Dispersion and limitations](cloitre-conway/dispersion.md) |

The global induction and some exact-neighborhood results are
**computer-assisted proofs**: an infinite argument uses explicit finite
premises checked by independent programs. Finite tests of additional
conjectures remain finite observations. No Lean formalization is included.

## Questions that remain open

1. **Convergence and decay over all integers.** Prove C(n)/n -> alpha,
   including the interiors of the Fibonacci blocks. The dispersion note
   proves that a stated uniform four-generation inequality would give
   an upper error rate O(n/(log n)^(1/4)); that inequality is still open.
   A matching lower bound for maxima is a separate question.
2. **The full recursive interface.** Determine what scale, position,
   profile, branch, and phase information suffices beyond the exact
   Fibonacci neighborhoods. Five digit labels or a candidate geometric
   cycle alone do not determine the actual selected recursive orbit.
3. **Inner dynamics between Fibonacci indices.** Control periods,
   landing times, and selected phases in the wider block interiors.

## Encoding comparison and related families

Canonical Fibonacci digit encoding provides a comparison with Campbell's
power-of-three solution. For the specified diagnostic in each family,
the minimum autonomous state-bit order is Theta(log log N); short inner
cycles do not imply constant encoding memory. The matching upper bound
for Cloitre's full sequence graph remains open. Read the
[Campbell theorem](campbell/scale-memory.md) and
[Cloitre diagnostic](cloitre-conway/five-window-closure.md#autonomous-memory-of-the-actual-top-plateau-diagnostic)
for the exact models and supplied-context distinctions.

Both families also have proved context-dependent interactions on the five
legal canonical digit patterns. Cloitre has an infinite interaction1
family with fixed-point root basins and recursive signal persistence;
Campbell's current coefficient has exactly three value classes.
Read the [Cloitre construction](cloitre-conway/exact-collars.md#a-persistent-interaction-on-canonical-index-words)
and [Campbell comparison](campbell/scale-memory.md#five-pattern-interaction-on-ternary-scale-interiors).

Shifted Conway/Mallows variants remain finite observations under their
stated initial conditions; see the [supporting audit](cloitre-conway/landing.md).
Literature review, a manuscript, and formalization are separate milestones.

[CONTRIBUTING.md](CONTRIBUTING.md) explains verification and the PR workflow.
Current proofs are maintained by topic; superseded versions live in Git
history. Historical labels in saved computations retain their original scope.

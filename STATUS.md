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
| Golden excess above one has an additive budget along actual selected children. Along value iteration n -> C(n), its normalized sum is at most 4/9, independently of the starting index. The selected-tree and value-orbit budgets do not yet establish full convergence. | [Selected-tree budget](cloitre-conway/golden-proof.md#9-a-global-integer-budget-for-the-selected-recursion-tree) · [Value-iteration budget](cloitre-conway/golden-proof.md#a-uniform-budget-along-value-iteration) |
| The ratio converges to alpha in neighborhoods of Fibonacci indices whose width is sublinear in the index. Exact nearby values and selected phases are known, including a growing constant band below each Fibonacci index. In a growing doubled band above the anchor, the canonical clock forces zero defect or copies one earlier defect unchanged. | [Orbit bounds](cloitre-conway/fibonacci-collars.md) · [Exact neighborhoods](cloitre-conway/exact-collars.md) |
| If two saturated source windows have cap defects at most two, a wider inner band becomes exact after a uniformly bounded number of orders. Persistent defects require a larger-amplitude witness in an explicit earlier window. The surrounding-window estimate needed for repeated enlargement remains open, so no unconditional faster collar rate follows yet. | [Ternary extinction](cloitre-conway/exact-collars.md#simultaneous-extinction-of-ternary-cap-defects) · [Sharper single-amplitude cases](cloitre-conway/exact-collars.md#simultaneous-extinction-of-binary-cap-defects) |
| If all defects in two saturated source windows are even, an inner band becomes exact after a uniformly bounded number of orders, with no fixed amplitude bound. A persistent defect requires an odd defect in an explicit earlier window. | [Even-defect extinction](cloitre-conway/exact-collars.md#even-cap-defects-vanish-by-parity) |
| If one saturated initial row is zero throughout the inherited band, its entire row parity stays zero. The other initial row may have arbitrary amplitudes; an inner band becomes exact within eight orders. A finite canonical certificate supplies the zero row for every inherited zero/three window starting at orders 20 through 40, with no bound on later orders. | [One-zero-row extinction](cloitre-conway/exact-collars.md#one-zero-initial-row-extinguishes-arbitrary-partner-amplitudes) |
| Full convergence is equivalent to sublinear negative displacement at the selected inner landing point. A quantitative limsup bound follows from the minimum Fibonacci phase of extremal subsequences; the required displacement estimate remains open. | [One-sided displacement criterion](cloitre-conway/dispersion.md#a-one-sided-landing-displacement-criterion) |
| A finite Fibonacci window determines the maximum on an infinite tail. Independently checked cycle enclosures give C(n)/n<0.65431110 for every n>=701408733. Concentration of the near-maximum terminal values forces a uniform loss in the actual selected tree, sharpening the bound to 0.65430545 on a later infinite tail. The outermost normalized cap contacts have a limit and an exact cumulative-loss criterion. Canonical clock rules also restrict local defect production and longer-cycle contacts. Full convergence remains open. | [Maximum principle](cloitre-conway/dispersion.md#a-finite-window-maximum-principle) · [Improved tail certificate](cloitre-conway/dispersion.md#a-smaller-tail-bound-from-cycle-enclosures) · [Terminal loss](cloitre-conway/dispersion.md#concentrated-high-terminal-values-force-a-uniform-loss) · [Contact budget](cloitre-conway/dispersion.md#an-exact-budget-for-the-outermost-cap-contacts) · [Canonical clock](cloitre-conway/dispersion.md#defect-production-by-the-canonical-clock) |
| At the least extremal phase both child phases lock exactly. If forward drawdowns are sublinear, failure of convergence forces synchronized intervals of strong negative jumps across arbitrarily many consecutive Fibonacci levels. Every wrong clock orientation also forces a spatial interval of approximate two-step returns. Sublinear drawdown and exclusion of those intervals remain unproved. | [Phase locking and synchronized intervals](cloitre-conway/dispersion.md#synchronized-negative-jump-intervals-under-sublinear-drawdown) |
| Local recursive interfaces and variance estimates are proved under explicit context and domain hypotheses. They give partial routes toward convergence; the uniform dispersion inequality remains open. | [Technical research map](cloitre-conway/README.md#technical-research-map) |

The global induction and some exact-neighborhood results are
**computer-assisted proofs**: an infinite argument uses explicit finite
premises checked by independent programs. Finite tests of additional
conjectures remain finite observations. No Lean formalization is included.

The [contact-frontier dynamics theorem](cloitre-conway/frontier-dynamics.md)
characterizes collapse of the outermost relative contact width by divergence
of the prescribed first-capture ranks. Positive width forces uniformly
bounded first capture. Positive-width gated frontiers force macroscopic
adjacent drops at the next level; under sublinear forward drawdown,
the frontier must eventually be ungated. Neither contact
collapse nor sublinear drawdown has been established. Complementary drawdown
tests in the [dispersion note](cloitre-conway/dispersion.md#complementary-drawdowns-and-the-upward-modulus)
remain finite observations.

Under sublinear complementary drawdowns on the actual reached frontier
cycles, the [cycle geometry theorem](cloitre-conway/frontier-dynamics.md#cycle-geometry-under-small-drawdowns)
restricts every scaled cycle limit to at most two reflected intervals.
Odd frontier periods must diverge; bounded periods give two limiting
positions. The sublinear drawdown hypothesis remains unproved.

A [continuous relaxed family](cloitre-conway/dispersion.md#continuous-cycle-readouts-do-not-determine-the-golden-profile)
preserves the golden anchors and native cap, has zero forward drawdowns
in both complementary profiles, and admits exact readouts at captured
fixed points or two-cycles for every real source. Its ratio still oscillates,
even below the current canonical tail bound. These are real profiles with
a choice of cycle point. Those limiting conditions alone therefore do not
replace the actual seed and clock in the canonical integer recurrence.

An [earlier-row feedback theorem](cloitre-conway/frontier-dynamics.md#earlier-row-feedback-preserves-the-prescribed-clock)
expresses every possible contact candidate using fixed earlier rows and one
preceding defect, retaining its exact seed and clock. A finite certificate
excludes a terminal interval uniformly over all capped preceding states.
A cross-level lower bound on these excluded widths remains open.

The [shorter query-domain theorem](cloitre-conway/frontier-dynamics.md#a-shorter-source-prefix-and-sparse-continuation)
computes a Fibonacci-row segment from the exact anchor and a shorter earlier
prefix, skipping an intervening interval of earlier indices. It applies
without an amplitude bound. Independent orbit selectors reproduce finite
sparse continuations; this gives no global convergence or complexity claim.

In a saturated amplitude-three source window, an
[exact seeded decoder](cloitre-conway/frontier-dynamics.md#an-exact-three-route-decoder-for-amplitude-three-windows)
reduces every paired seed and clock to one of three routed lower values
after logarithmically many earlier-row excursions. A finite level-33
certificate excludes a locally permitted positive branch for every capped
preceding state. A uniform reset estimate remains open.
Under inherited zero/three windows, a possible split between two diagnostic
routes must leave one contact among the last four offsets; their first
returns remain outside the known terminal shelves. Complete synchronization
and a cross-level reset estimate remain open.

The [default-channel extinction theorem](cloitre-conway/frontier-dynamics.md#persistent-amplitude-three-defects-need-effective-nondefault-entrances)
shows that a persistent amplitude-three defect needs repeated effective
nondefault entrances, with a quantitative backward chain of guarded events.
Bounding the frequency of those actual channel choices remains open.

Allowing arbitrary suppression still gives
[bounded extinction without positive creation](cloitre-conway/frontier-dynamics.md#positive-creating-entrances-have-strictly-leftward-ancestry).
Persistent amplitude-three defects therefore require positive-creating
entrances with a strictly leftward chain of lower contacts, staying
inside the controlled band. This refines the mechanism of persistence;
the existing one-offset theorem already gives faster exact-prefix growth.
Control of the surrounding windows needed for repeated enlargement
remains open.

A [traveling amplitude-three history](cloitre-conway/exact-collars.md#an-amplitude-three-traveling-history-limits-the-relaxed-routing-method)
shows that the local necessary routing rules alone cannot extend uniform
extinction to larger alphabets. It satisfies the zero left boundary and
clock parity but leaves the actual seed-selected entrance unconstrained.
For this relaxed rule the optimal lower bound on asymptotic front speed
is 1/3, matching the existing one-offset argument. One explicitly adjusted
history also attains every site deadline in a specified phase. These are
limitations of that relaxation, not
canonical counterexamples.

Even retaining the full prescribed seed and depth, an explicit nonconvergent
comparison sequence has a uniformly bounded additive recurrence error and
bounded drawdowns in both complementary sequences. A one-unit input change
can also produce a linear change in the nested operator's output. The
[bounded-forcing theorem](cloitre-conway/dispersion.md#bounded-forcing-with-the-complete-prescribed-clock)
shows why small scalar errors do not control the actual clock. These are
limitations of approximation arguments; the canonical equation has zero error.

With a different ten-term initialization, an explicit nonconvergent sequence
[satisfies the exact nested equation at every later index](cloitre-conway/dispersion.md#exact-nesting-after-finitely-many-forced-values).
Its recurrence error is supported at seven early sources. Any finite
canonical prefix can also be retained, allowing finitely many subsequent
forced values before an exact nonconvergent tail. Both drawdowns remain
bounded, but the canonical Fibonacci anchors and upper cap are lost.
This shows that exact tail nesting and bounded drawdowns alone do not force
convergence; the canonical initial history still matters.

## Questions that remain open

1. **Convergence and decay over all integers.** Prove C(n)/n -> alpha,
   including the interiors of the Fibonacci blocks. The
   [one-sided displacement criterion](cloitre-conway/dispersion.md#a-one-sided-landing-displacement-criterion)
   reduces convergence to controlling negative jumps at the prescribed
   landing point; it does not yet prove those jumps are sublinear. The
   [dispersion note](cloitre-conway/dispersion.md) gives a conditional decay
   theorem; its required uniform inequality is still open. A matching
   lower bound for maxima is a separate question.
   An [exact two-generation policy certificate](cloitre-conway/dispersion.md#a-two-generation-certificate-at-the-forced-geometric-bottleneck)
   repairs a checked one-step bottleneck and separates scalar-preserving
   from nodewise moment-preserving proof policies. Its finite minimum uses
   one randomized split state. A [block-terminal criterion](cloitre-conway/dispersion.md#block-terminal-means-remove-intermediate-scalar-constraints)
   removes intermediate scalar constraints and repairs that threshold
   with a deterministic tree; two complete trees attain the larger finite
   optimum. Uniform terminal compensation and dispersion remain open.
2. **The full recursive interface.** Determine what scale, position,
   profile, branch, and phase information suffices beyond the exact
   Fibonacci neighborhoods. Five digit labels or a candidate geometric
   cycle alone do not determine the actual selected recursive orbit.
   The [generated Fibonacci band](cloitre-conway/exact-collars.md#a-propagated-cap4-band-generates-its-own-profiles)
   gives actual profiles and descendants in a growing neighborhood.
   [Shared response words](cloitre-conway/recursive-descent.md#arithmetic-support-cones-shrink-the-shared-response-word)
   reduce the data outside it. The
   [first exterior pair](cloitre-conway/recursive-descent.md#the-exterior-replay-reaches-an-unbounded-profile-after-two-steps)
   and its high digit context are generated without extra context labels,
   but the next lookup enters a macroscopic interior with unbounded
   natural-cap defect. Constructing those interior values and the
   remaining clock is necessary for this replay route. Arithmetic outputs
   can sometimes skip replay; these dependencies are not a general
   lower bound on evaluation inputs.
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

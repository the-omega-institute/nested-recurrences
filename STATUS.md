# Research status

Updated 2026-10-01. [Reading guide](README.md)

## Completed results

| Result | Verification scope | Read |
|---|---|---|
| Campbell: totality, explicit power-of-three formula, sharp four-step transient, periods 1 or 2, dilation identity and ratio extrema | Written proof; exact symbolic arithmetic and independent sequence checks; closure checker records six parity/domain endpoint templates (five distinct affine maps) and parity phase | [Three-page PDF](campbell/note.pdf) · [Proof certificate](campbell/verification/proof-check.json) |
| Cloitre: totality, elementary 3/5 and 3/4 bounds, split separation and entry into the eventual cycle at the prescribed depth | Written arguments with explicit finite initial cases | [Foundations](cloitre-conway/proof.md) |
| Cloitre: rational envelope for every n>=131072 | Propagation proof plus exact finite seed certificate | [Propagation](cloitre-conway/proof.md#3-finite-window-propagation-and-explicit-infinite-bounds) |
| Cloitre: C>=G, exact equality set, Fibonacci identities and landing, block upper cap, liminf C(n)/n=1/phi | Computer-assisted theorem: exact finite base followed by general induction and cycle capture | [Global golden structure](cloitre-conway/golden-proof.md) |
| Cloitre: all-cycle period bound at F_k+t, exact +/-2 identities, five-offset cycle classification and uniform convergence in sublinear Fibonacci neighborhoods | Consequences of the global theorem; no additional finite premise | [Fibonacci collars](cloitre-conway/fibonacci-collars.md) |
| Cloitre: capture distance contracts by at most 2/3 every two steps; capture takes `O(log n)` steps; intersecting all Fibonacci anchor bounds gives width `min(t,F_(k-3),F_(k-1)-t)`; globally `limsup (mu+period)/n<=(3-sqrt(5))/4` | General proof from G, the exact equality set and the cap; 130 small-anchor floor checks introduce no sequence premise. All-start and prescribed-orbit checks are corroboration. An abstract monotone profile with defects 0/1 has linear interior tails even with a fixed identity collar; full C landing in wide arches remains open | [Quantitative capture](cloitre-conway/fibonacci-collars.md#quantitative-capture-and-a-short-exterior-certificate) · [Anchor intersection](cloitre-conway/fibonacci-collars.md#intersecting-the-anchor-bounds) · [Exact check](cloitre-conway/verification/collar-check.json) |
| Cloitre: three-window certificates, exact finite-window characterization of the tail supremum, and C(n)/n<=8900/13459 for all n>=349525 | General propagation theorem plus independently reproduced window [349525,1048574] | [Limsup certificates](cloitre-conway/golden-proof.md#8-shorter-certificates-and-the-global-limsup) |
| Defect-plateau return certificates: two verified constant-defect intervals give an exact translation run, its exit time and selected-depth endpoint; the abstract linear tail has a two-block certificate | General written proof; exhaustive all-start/depth tests for capped profiles on domains of width at most five; exact selected-split replay through n=131071; n=248 eight-step run compressed into one block; large abstract examples use integer arithmetic without building the long orbit. No uniform short C certificate is proved | [Return certificates](cloitre-conway/fibonacci-collars.md#defect-plateau-return-certificates) · [Exact check](cloitre-conway/verification/collar-check.json) |
| Cloitre: C(F_k+t)=F_(k-1)+max(0,t) for k>=23 and -12<=t<=32; complete fixed-point/two-cycle classification for k>=24 | Two-collar induction using 90 exact seed values at orders 23 and 24; all-start graph diagnostics are corroboration | [Exact collars](cloitre-conway/fibonacci-collars.md#6-exact-collars-propagate-from-two-seeds) |
| Cloitre: exact Fibonacci profile renormalization and nonpositive defect cocycle; first period-five arch certificate at n=196 | Direct consequence of cycle capture and the upper cap; exact finite orbit/profile arithmetic | [Profile dynamics](cloitre-conway/fibonacci-collars.md#7-fibonacci-profile-renormalization-and-defect-dynamics) |
| Five-window closure interface: compressed one-scale payload, cross-scale child selectors and selected phase | Exact alternating closure and centroid identities; 13 public period-five words reconstructed; 57/65 parent rows have split ambiguity, 56/65 individual candidate sets are non-contiguous, all 69,064 row-local selector combinations are replayed, the two lower-map parameters satisfy `alpha_i+beta_i=t` on all 65 rows, `alpha` is injective on all 69,064 row-local combinations, and each child-split/alpha/beta parameterization adds five affine directions in the finite 13-payload rank audit; Campbell ternary endpoint templates checked by the 12-row arithmetic certificate | [Five-window interface](cloitre-conway/fibonacci-collars.md#8-five-window-closure-interface) · [Selector audit](cloitre-conway/verification/selector-payload-check.json) |
| Common reflection-window closure theorem: generic payload dimension is `p+1` including scale, with odd/even fixed-point/translation closure; the five-window needs five extra coordinates after `t` | Exact symbolic affine verification for `p=1,...,8`; Campbell's `p=2` compression is recorded as a family-specific endpoint-template relation | [Common closure theorem](cloitre-conway/fibonacci-collars.md#9-common-closure-theorem-and-generic-minimality) · [Exact check](cloitre-conway/verification/closure-interface-check.json) |
| Inverse selector interface: alpha and one admissible seed reconstruct the whole word; the conditional fixed-width branch budget is `ceil(log_2 M)` for maximum fiber size `M`; odd-window collisions require a descending profile secant | General written argument; 13 public selected words reconstructed; a complete two-word fiber at n=7739 disproves global alpha injectivity and the fixed mod-5 seed refinement | [Seed reconstruction](cloitre-conway/fibonacci-collars.md#seed-reconstruction-and-the-remaining-branch-information) · [Witness check](cloitre-conway/verification/selector-payload-check.json) |
| Defect-box seed theorem for odd windows: alpha plus `r_0 mod (floor(sum e_i/2)+1)` reconstructs the word; rotating the explicit seed interval sharpens the fiber bound; defects also give nondecreasing profile covers | General written proof; interval checked on all 69,064 public Cartesian words; adaptive decoding of 13 selected words and both n=7739 witnesses; exact abstract sharpness and even-window counterexample. A four-class candidate-set witness at n=12898 refutes a uniform three-class cover. The defect-derived budget grows at least linearly at Fibonacci knees, without implying growing fibers | [Defect budget](cloitre-conway/fibonacci-collars.md#a-universal-seed-label-from-the-parent-defect-budget) · [Exact check](cloitre-conway/verification/selector-payload-check.json) |
| Local cycle-admissibility refinement preserves actual child selectors; the n=7739 collision words are transient and are both excluded; periodicity alone does not imply general inverse injectivity | General domain-refinement argument; all 13 public selected words preserved; first-row witness trajectories and every coordinate checked against full-domain cycles; an explicit abstract shared-profile five-cycle has two locally fixed inverse words with equal alpha | [Cycle refinement](cloitre-conway/fibonacci-collars.md#local-cycle-admissibility-and-what-it-does-not-prove) · [Exact check](cloitre-conway/verification/selector-payload-check.json) |
| Minimum periodicity tests: collision-pair masks give an exact criterion for qualified inverse injectivity; collision-word masks characterize the stronger raw-image uniqueness | General conditional theorem; exhaustive small pair-path/Cartesian comparison; complete C fibers at n=11342 and n=28996. The latter needs one tested row for qualified injectivity and two for raw uniqueness; four other periodic rows still leave a collision. The contexts rule out any single fixed pivot. No universal adaptive-test bound is proved | [Minimum cycle checks](cloitre-conway/fibonacci-collars.md#minimal-periodicity-checks-for-inverse-reconstruction) · [Exact check](cloitre-conway/verification/selector-payload-check.json) |
| Exact signed-gap quotient: alpha collisions correspond in both directions to closed layered walks; odd-window defect budget E bounds each layer to at most `2*floor(E/2)` states | General Cartesian-context proof and reverse reconstruction; 132 small qualification contexts checked against full fibers. At n=28996 an eight-state graph gives a hand-checkable proof that row 1 is sufficient for qualified injectivity; both C witness minima match complete-fiber enumeration. State count and periodicity data remain context-dependent | [Gap graph](cloitre-conway/fibonacci-collars.md#a-bounded-gap-automaton-with-reverse-completeness) · [Exact check](cloitre-conway/verification/selector-payload-check.json) |
| Minimum primitive-cycle defect: a proper integer reflection-defect cycle of period p>=3 needs total E>=p; odd p at even offset needs E>=p+1 | General connected-cycle and integer-spacing proof; sharp capped-profile constructions for every p>=3. Twenty constructions at p=3,...,12 and 13,505 selected C cycles through n=28996 corroborate the argument; C attains E=p at n=68, period 4. This does not bound defect budgets across scales | [Defect cost](cloitre-conway/fibonacci-collars.md#minimum-defect-cost-of-a-proper-cycle) · [Exact check](cloitre-conway/verification/selector-payload-check.json) |
| Recursive window representation: allow a parameter A_i at each row; actual selected children remain in natural blocks at orders j-1,j-2, their parameters add to A_i, and row alignment is inherited | General theorem from intersected capture and the profile identity; no extra carry or rotation coordinates. Every branch reaches profile orders 4 or 5 within j-5 edges. Exact replay of 13 public five-window roots and 40 boundary words gives 2,509 nodes, 1,281 leaves and 159 literal selected-point checks. Uniform branch bounds, total certificate size and selected-value proof compression remain open | [Recursive windows](cloitre-conway/fibonacci-collars.md#recursive-windows-with-a-parameter-at-every-row) · [Exact check](cloitre-conway/verification/selector-payload-check.json) |
| Multiscale inverse-label budget: for an odd root window at profile order j with total defect E, each frontier needs at most floor(E/2) seed bits, and the whole tree at most `(j-5)*floor(E/2)` | General conserved-defect proof, conditional on local alpha words and profile/candidate contexts; second children need no separate seed. All 962 odd internal nodes decode by adaptive residues. At n=196 the summed sufficient labels use 29 bits versus the proved bound 66; this excludes parameter words, context proofs and selected phases, and is not a minimum for the whole certificate | [Conserved budget](cloitre-conway/fibonacci-collars.md#a-conserved-budget-for-multiscale-inverse-labels) · [Exact check](cloitre-conway/verification/selector-payload-check.json) |
| Repeated physical indices share selectors and parameters on repeated directed input pairs; their exact gap quotient imposes equality on incoming and outgoing gaps. A nonbipartite monotonicity sign graph proves inverse uniqueness with at most five vertices, independent of E. An odd two-label window collides exactly on common self-loop gaps | General proofs and reverse reconstruction; all 52 five-row equality partitions checked against complete small fibers. At n=196 one two-label child needs no seed, versus the defect rule's three-bit sufficient allowance, and alpha shrinks from five entries to three. Every prescribed five-cycle through 4096 gives 12,208 distinct internal contexts; sharing reduces 437 collision pairs to three in two contexts. The surviving n=2012 collision is excluded by periodicity at one row. Context, alpha and actual basin/phase proof costs remain separate | [Shared-row theorem](cloitre-conway/fibonacci-collars.md#sharing-selectors-at-repeated-physical-indices) · [Exact check](cloitre-conway/verification/selector-payload-check.json) |
| Cross-window absolute parameters satisfy K_(N,M)=s(M)+C(s(N)); a bipartite forest has exact universal linear rank `2|V|-c`, and one seed per strong selector component reconstructs its joint assignment. Network gap relations have reverse completeness | General proofs, 512 independent rational rank checks and 954 complete small-fiber comparisons. For the same fixed layout through 4096, 2,308 forest entries recover 6,514 physical-edge and 61,040 row entries. All 37 selector components are jointly injective on supplied geometric/value domains: 10 singleton, 14 additional sign and 13 exact gap certificates; conditional joint branch bits are zero. The edge 489->476 separates the n=2012 local collision. Layout, domain/profile and actual basin/phase proof costs are excluded; forest rank is not C-specific minimum information | [Shared network](cloitre-conway/fibonacci-collars.md#a-shared-parameter-network-and-its-forest-basis) · [Exact check](cloitre-conway/verification/selector-payload-check.json) |
| Generative shared descent: geometric splits have child fractions in `[3/11,8/11]`; total distinct root mass R gives `D<=B-8+floor(11R/(3B))` and an `O(sqrt(R) log N)` structural code with no supplied child layout, profile table or parameter graph | General mass-cut and prefix-free coding proofs; 55,408 complete small layouts and 905,301 histogram cache nodes independently checked. Saved root/header packets replay from the first eight terms alone. The n=196 root plus five-cycle has a 112-bit body; the 147-root family has 9,427 bits generating all earlier windows and parameters. Four existing knees replay, including N=103682 with 424 internal indices and 2,577 bits despite 6,870 marked leaves. Root headers and selected-validity proof costs are separate; n=11 shows a shared periodic same-basin endpoint can have the wrong phase | [Generative code](cloitre-conway/fibonacci-collars.md#generating-the-layout-from-a-sublinear-shared-descent-code) · [Exact check](cloitre-conway/verification/selector-payload-check.json) |
| Seven-symbol terminal code: the actual profile defect counts marked leaves; positioned letters recover all internal arithmetic selector/parameter data, and a generating coefficient counts every geometrically legal tree | General forward and reverse geometry proof; exact support interval and three-coordinate histogram reconstruction. Worst-case full geometric capacity is Theta(F_j), even with zero defect or a fixed histogram. Coefficient ordinals checked against all 28,284 words through order nine; 65 actual rows recover 2,815 internal splits. At n=196 joint geometric capacity is 158 bits, conditional on root offsets/defects, with profile consistency and selected-orbit proof costs excluded. This is a geometric-class minimum, not C's family-specific minimum | [Terminal code](cloitre-conway/fibonacci-collars.md#seven-terminal-symbols-and-the-full-geometric-selector-code) · [Exact check](cloitre-conway/verification/selector-payload-check.json) |
| Actual defects grow linearly at Fibonacci knees; every cycle at n=2F_(k-1) has a linearly growing mean defect. Full convergence is exactly a uniform marked-leaf occupation law | General consequences of the existing 2/3 envelope, capture and the terminal identity; four knee samples and complete cycle graphs at n=35422,57314,92736 corroborate. The consistent upper-cap profile has geometric descent and the same leaves but fails prescribed nesting at n=11. Neither unbounded defect nor a seven-letter code proves unbounded inverse fibers or a global finite-state classification | [Growing defects and occupation](cloitre-conway/fibonacci-collars.md#growing-actual-defects-and-the-remaining-occupation-problem) · [Exact check](cloitre-conway/verification/selector-payload-check.json) |
| Selected-phase interface requires prescribed-start basin and entry alignment: for canonical position `j` of the entry point, use `j+d-mu mod p` | Exact n=196 certificate: phase from entry is 3, canonical selected phase is 4, correct split 118 gives C(196)=134; ignoring alignment selects 117 and gives 131 | [Selected-value closure](cloitre-conway/fibonacci-collars.md#8-five-window-closure-interface) · [Exact check](cloitre-conway/verification/selector-payload-check.json) |
| First three Fibonacci-arch reverse-completeness audits: all starting states for 144<=n<=609 | 466 functional graphs, 174,983 vertices, exact per-block cycle histograms, and 13 period-five payloads; the first block has its unique period-five graph at n=196 | [Finite five-window certificate](cloitre-conway/verification/five-window-check.json) |

Here G(n)=floor((n+1)/phi). The equality set is exactly

$$
\{F_j,F_j+1:j\ge2\}\cup\{F_j-1:j\ge3\text{ odd}\}\cup\{11,24,25,59\},
$$

with F_0=0,F_1=1. The four exceptional indices are part of the theorem.
The older zero-set containment and Fibonacci landing problems are resolved.

The global golden proof uses a base through 65535 and the seed window
[16384,131071]. The larger F_36 experiment is corroboration, not a premise.
The [carry and infinite-set arithmetic lemma](cloitre-conway/landing.md)
supplies an ingredient of the induction; it also documents numerical corrections.

## Next research questions

1. **Full ratio convergence.** The liminf is 1/phi. To prove a full limit,
   control the limsup between Fibonacci anchors, especially the centers of
   the arches. The collar theorem covers offsets o(F_k), not offsets of order F_k.
   The new W(M)=max(C(m)/m: M<=m<3M) is exactly the tail supremum, and is
   nonincreasing for M>=21846. Its proved limit is the limsup; proving that
   limit equals 1/phi remains open. The certified upper bound is now
   8900/13459=0.6612675533100527..., improved from 103088/155677.
2. **Arch profiles and inner dynamics.** The defect identity gives a two-scale
   renormalization skeleton, while the first period-five arch supplies a local
   branch certificate. Determine whether arch defect trees admit finitely many
   certified local types and a reverse completeness map. Establish a decay rate
   only after obtaining
   global control; study whether cycle periods are unbounded and bound interior
   transients in wide arches. Exterior capture now has a logarithmic bound;
   fixed-width neighborhoods have logarithmic full landing, while the global
   joint orbit budget is at most `((3-sqrt(5))/4)*n+O(log n)`. The claimed
   0.087 +/-0.5% sampled stability was not
   reproduced; see the [decay audit](cloitre-conway/landing.md#4-reproducible-finite-audit).
   The exact-collar theorem propagates any width with suitable two seeds;
   existence of such seeds for every width has not been proved.
   Exact return blocks now distinguish a long literal transient from a long
   certificate: paired defect plateaus yield arithmetic translations, with
   a two-block certificate for the abstract linear-tail example. C's finite
   plateau audit gives limited compression; seek larger verified return cells
   rather than assuming a short transient or a bounded plateau itinerary.
   For the inverse selector interface, control the defect-derived seed interval
   or descending profile branches across orders. The adaptive defect modulus
   gives a universal arithmetic label, but its size is not uniformly bounded;
   the n=7739 witness rules out a fixed mod-5 shortcut. Establish whether the
   actually selected alpha tuples have stronger uniqueness than arbitrary
   legal row-local decomposition witnesses. Separate row-local decomposition,
   lower-cycle membership, prescribed-start basin and selected lower phase.
   Periodicity narrows the candidate domain but the abstract counterexample
   shows that a family-specific inverse theorem still needs more information.
   The exact coordinate-test criterion now distinguishes qualified injectivity
   from the stronger uniqueness against raw candidates. At n=28996 one row
   suffices for the first claim, while two are necessary for the second.
   Seek a uniform context-dependent qualification bound; a single fixed
   coordinate already fails on the two public C witnesses. The complete
   lower graph and the cost of certifying its collision exclusions remain
   part of the context, not free bits removed from the affine payload.
   The signed-gap quotient now gives an exact reverse-complete test without
   listing alpha fibers. Seek recursive certificates for its edge relations
   and qualification predicates, with controlled context size. The proper-cycle
   bound E>=p is a lower bound; it does not supply the missing uniform upper
   bound on the gap alphabet or prove an adaptive single-row theorem.
   The recursive coordinate class is now closed under descent by allowing
   row-dependent parameters. Intersected capture keeps both actual children
   in their natural lower blocks; no independent carry word or child row
   rotation is needed. Structural termination does not bound the binary
   tree's total size or certify a recovered raw word's prescribed selections.
   Seek recursive edge/qualification certificates inside this class, keeping
   its inherited row clock separate from each physical orbit's selected phase.
   Conserved defects now bound residual seed labels across the whole tree by
   `(j-5)*floor(E/2)`, and by floor(E/2) on each frontier. This controls one
   source of branch proliferation but excludes parameter/context and phase
   proof costs. Seek compression of those remaining data, rather than treating
   the conditional bit bound as a total certificate bound.
   The positioned terminal code now recovers all arithmetic selector data,
   while its coefficient counts only the larger geometric class. Shared
   profile consistency and prescribed orbit selection must still be proved.
   Actual defects grow linearly at the Fibonacci knees, so a uniform E bound
   is unavailable. Seek arithmetic compression of leaf positions and the
   occupation deficit instead; histograms recover values but can lose selected
   phases, as the explicit n=15 example shows.
   Repeated physical indices now share their selector, with an exact constrained
   gap test and a two-label odd-window criterion. This eliminates some inverse
   seed labels without adding a coordinate. Sharing alone still leaves three
   collision pairs in two audited descendant contexts; next incorporate
   consistency between tree nodes and certified periodic/basin/phase restrictions.
   Sharing is now expressed between windows in absolute physical coordinates.
   A bipartite forest removes all universal linear parameter redundancy, and
   the fixed audited joint network has no inverse collisions. Its physical
   layout is supplied: an alternative selector may change that layout under
   descent. Recover the layout and selected-validity proofs by arithmetic
   family rules, keeping their costs separate from the zero conditional seed
   count and the forest's scalar-entry rank.
   A generative first-visit code now includes that child layout and its value
   table, with a proved O(sqrt(R) log N) structural upper bound from globally
   shared balanced splits. The encoded endpoints still need prescribed
   iteration proofs: the n=11 counterexample passes periodicity and basin
   but has the wrong phase. Seek arithmetic phase rules and phase-independent
   value certificates to avoid a pointwise predecessor-depth chain. Keep
   these proof costs and the uniform marked occupation law in the objective.
3. **Shifted Conway/Mallows variants.** The proposed inequalities relative to G
   and Fibonacci anchors are finite observations through 2^20 under the stated
   initial conditions, not universal theorems. See the [family audit](cloitre-conway/verification/landing-audit.json).
4. **Literature and proof consolidation.** Review related recurrences and
   priority before preparing a manuscript. Formalization is an optional
   separate milestone; no Lean theorem is currently claimed.

## Reproducibility and maintenance

The [verifier](scripts/verify.py) replays the exact committed evidence;
[main instructions](README.md#optional-reproduce-the-computations) explain how.
Proofs and current status are maintained in place. Necessary programs and
evidence live in `verification/` subdirectories; intermediate experiments and
draft variants do not accumulate in the public tree. Earlier stages remain
available in Git history.

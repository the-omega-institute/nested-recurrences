# Research status

Updated 2026-10-01. [Reading guide](README.md)

## Completed results

| Result | Verification scope | Read |
|---|---|---|
| Campbell: totality, explicit power-of-three formula, sharp four-step transient, periods 1 or 2, dilation identity and ratio extrema | Written proof; exact symbolic arithmetic and independent sequence checks | [Three-page PDF](campbell/note.pdf) |
| Cloitre: totality, elementary 3/5 and 3/4 bounds, split separation and entry into the eventual cycle at the prescribed depth | Written arguments with explicit finite initial cases | [Foundations](cloitre-conway/proof.md) |
| Cloitre: rational envelope for every n>=131072 | Propagation proof plus exact finite seed certificate | [Propagation](cloitre-conway/proof.md#3-finite-window-propagation-and-explicit-infinite-bounds) |
| Cloitre: C>=G, exact equality set, Fibonacci identities and landing, block upper cap, liminf C(n)/n=1/phi | Computer-assisted theorem: exact finite base followed by general induction and cycle capture | [Global golden structure](cloitre-conway/golden-proof.md) |
| Cloitre: all-cycle period bound at F_k+t, exact +/-2 identities, five-offset cycle classification and uniform convergence in sublinear Fibonacci neighborhoods | Consequences of the global theorem; no additional finite premise | [Fibonacci collars](cloitre-conway/fibonacci-collars.md) |
| Cloitre: three-window certificates, exact finite-window characterization of the tail supremum, and C(n)/n<=8900/13459 for all n>=349525 | General propagation theorem plus independently reproduced window [349525,1048574] | [Limsup certificates](cloitre-conway/golden-proof.md#8-shorter-certificates-and-the-global-limsup) |
| Cloitre: C(F_k+t)=F_(k-1)+max(0,t) for k>=23 and -12<=t<=32; complete fixed-point/two-cycle classification for k>=24 | Two-collar induction using 90 exact seed values at orders 23 and 24; all-start graph diagnostics are corroboration | [Exact collars](cloitre-conway/fibonacci-collars.md#6-exact-collars-propagate-from-two-seeds) |
| Cloitre: exact Fibonacci profile renormalization and nonpositive defect cocycle; first period-five arch certificate at n=196 | Direct consequence of cycle capture and the upper cap; exact finite orbit/profile arithmetic | [Profile dynamics](cloitre-conway/fibonacci-collars.md#7-fibonacci-profile-renormalization-and-defect-dynamics) |
| Five-window closure interface: compressed one-scale payload, cross-scale child selectors and selected phase | Exact alternating closure and centroid identities; 13 public period-five words reconstructed; 57/65 parent rows have split ambiguity, 56/65 individual candidate sets are non-contiguous, and all 69,064 row-local selector combinations are replayed; Campbell ternary endpoint templates checked by the 12-row arithmetic certificate | [Five-window interface](cloitre-conway/fibonacci-collars.md#8-five-window-closure-interface) · [Selector audit](cloitre-conway/verification/selector-payload-check.json) |
| Common reflection-window closure theorem: generic payload dimension is `p+1` including scale, with odd/even fixed-point/translation closure; the five-window needs five extra coordinates after `t` | Exact symbolic affine verification for `p=1,...,8`; Campbell's `p=2` compression is recorded as a family-specific endpoint-template relation | [Common closure theorem](cloitre-conway/fibonacci-collars.md#9-common-closure-theorem-and-generic-minimality) · [Exact check](cloitre-conway/verification/closure-interface-check.json) |
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
   global control; study whether cycle periods are unbounded and derive
   landing-time bounds. The claimed 0.087 +/-0.5% sampled stability was not
   reproduced; see the [decay audit](cloitre-conway/landing.md#4-reproducible-finite-audit).
   The exact-collar theorem propagates any width with suitable two seeds;
   existence of such seeds for every width has not been proved.
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

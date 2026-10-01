# Research status

Updated 2026-10-01. [Project home](README.md) · [Definitions and context](GENERAL.md)

## Established results

| Subject | Result and proof scope | Read |
|---|---|---|
| Campbell's recurrence | Complete power-of-three formula; sharp four-step transient; periods 1 or 2; dilation identity; ratio extrema 2/5 and 3/4. Written proof with exact symbolic and independent sequence checks. | [Proof PDF](campbell/note.pdf) |
| Conway foundations | Totality, elementary 3/5 and 3/4 bounds, prescribed-depth cycle entry, and propagation of finite-window ratio bounds. | [Foundations](cloitre-conway/proof.md) |
| Global golden structure | C>=G, exact equality set, Fibonacci identities and landing, block upper cap, and liminf C(n)/n=1/phi. Computer-assisted induction with explicit finite premises. The shorter-window certificate gives C(n)/n<=8900/13459 for n>=349525. | [Global proof](cloitre-conway/golden-proof.md) |
| Fibonacci neighborhoods | All-cycle capture and period bounds, exact nearby dynamics, and convergence in sublinear-width neighborhoods. Exact values for -12<=t<=32 propagate from finite seeds; every fixed positive offset eventually becomes linear, with an explicit threshold. | [Orbit bounds](cloitre-conway/fibonacci-collars.md) · [Exact collars](cloitre-conway/exact-collars.md) |
| Five-window interfaces | Exact profile identities, closure equations, and conditional minimum phase states for a specified output. Inverse reconstruction and shared recursive codes have stated geometric and profile qualification requirements. These are not a complete minimum interface for actual C. | [Closure](cloitre-conway/five-window-closure.md) · [Inverse reconstruction](cloitre-conway/inverse-reconstruction.md) · [Recursive descent](cloitre-conway/recursive-descent.md) |
| Asymptotic reduction | Two exact size-biased martingales and a proved conditional decay implication. Basin lower envelopes and scalar-valid split policies give sufficient routes to the missing dispersion inequality. Finite tests support these routes; the uniform inequality remains open. | [Martingales and dispersion](cloitre-conway/dispersion.md) |
| Limits of static information | Explicit scalar extensions can preserve any actual finite prefix, the golden bounds, equality set, and all proved fixed collars, yet fail to converge. These are alternative extensions, not counterexamples to the prescribed recurrence. | [Nonconvergent extensions](cloitre-conway/dispersion.md#finite-prefixes-and-exact-collars-do-not-force-convergence) |
| Campbell in Fibonacci encoding | Through L canonical five-windows, an autonomous K-state DFA/NFA recognizing 5b(n)=2n must satisfy L<=4K+4. Minimum control-memory order is Theta(log L)=Theta(log log N), with horizon-specific tables whose size is excluded. This does not prove a Cloitre lower bound or a deterministic full-graph decoder. | [Scale-memory theorem](campbell/scale-memory.md) |

Proof notes state the precise domains, thresholds, finite premises, and
verification scope. No Lean validation is claimed. Historical conjecture
labels in saved experiment reports describe their original scope; the notes
give current theorem status.

## Open questions and next steps

1. **Global convergence and decay for actual C.** Prove a uniform dispersion
   inequality using restrictions on actual profiles or their selected dynamics.
   The conditional quartic criterion yields an upper error rate
   O(n/(log n)^(1/4)); proving that criterion and a matching lower bound for
   maxima are separate open tasks. Long finite prefixes and exact collars
   alone do not force convergence.
2. **The full minimum recursive interface.** Count scale, position, profile,
   branch qualification, and phase resources together. Local output-state
   minima assume the surrounding context is supplied. Prove an actual-C
   interface beyond the exact Fibonacci collars rather than treating the
   five digit labels or a geometric cycle certificate as sufficient.
3. **Dynamics in wide arches.** Control periods, landing times, and actual
   selectors in Fibonacci-block centers. The orbit bounds and saturated
   barriers restrict this domain but do not settle it.
4. **Related families and consolidation.** Shifted Conway/Mallows laws remain
   finite observations under their stated initial conditions. Review the
   literature before preparing a manuscript. Formalization is a separate
   possible milestone.

## Reproducibility and maintenance

[CONTRIBUTING.md](CONTRIBUTING.md) explains the eight reproduction checks and
the branch → pull request → review → merge workflow. Current proofs are
maintained by subject. Code and compact evidence live in verification
directories; intermediate experiments and correspondence stay outside the
public tree. Superseded stages are retained in Git history.

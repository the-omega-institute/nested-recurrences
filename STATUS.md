# Research status

Updated 2026-09-30, Asia/Singapore.

| Claim | Status | Evidence |
|---|---|---|
| Campbell totality and power-of-three formula | Written proof | [Note](campbell/note.pdf) |
| Campbell sharp four-step transient and cycle classification | Written proof; exact symbolic arithmetic checked | [Source](campbell/note.tex), [certificate](campbell/proof-check.json) |
| Conway totality and 3/5, 3/4 ratio bounds | Written induction with explicit small initial cases | [Sections 1–3](cloitre-conway/proof.md) |
| Conway depth always reaches the cycle | Written argument with exact initial cases through 52 | [Section 4](cloitre-conway/proof.md) |
| Conway global rational envelope for n>=131072 | Computer-assisted theorem: propagation lemma plus exact finite seed certificate | [Proof](cloitre-conway/proof.md), [certificate](cloitre-conway/conway-results.json) |
| Conway C(n)>=G(n) | Conjecture; checked through 2^20 | [Results](cloitre-conway/conway-results.json) |
| Conway C(F_k)=F_(k-1) for k>=2 | Conjecture; checked through k=30 | [Results](cloitre-conway/conway-results.json) |
| Every equality occurs at F_k or F_k±1 | False | Counterexamples 11,24,25,59 |
| Refined equality-set description | Conjecture; checked through 2^20 | [Section 5](cloitre-conway/proof.md) |
| Unbounded periods or an n^0.4 growth law | Open; finite data only | [Orbit tables](cloitre-conway/conway-results.json) |
| Lean formalization | Not undertaken | No Lean theorem claimed |

The main next proof problem is to control the basin of the Fibonacci fixed
point and the corrected zero-defect set. Earlier Fibonacci identities imply
that F_(k-1) is a fixed point of T_(F_k), but do not imply that the orbit starting
at F_k-1 reaches it.

A stronger finite observation is available: for all a,b<=2^20,
C(a)+C(b)>=G(a+b), except (a,b)=(2,2). This follows from the exact check of
2628 pairs of zero-defect indices and the Beatty-floor inequality. Establishing
it for all positive arguments would require a new argument.

The public repository is the research source and evidence location. Subsequent
substantive results should update this status, the affected proof and its
reproduction records together.

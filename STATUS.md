# Research status

Updated 2026-09-30, Asia/Singapore.

| Claim | Status | Evidence |
|---|---|---|
| Campbell totality and power-of-three formula | Written proof | [Note](campbell/note.pdf) |
| Campbell sharp four-step transient and cycle classification | Written proof; exact symbolic arithmetic checked | [Source](campbell/note.tex), [certificate](campbell/proof-check.json) |
| Conway totality and 3/5, 3/4 ratio bounds | Written induction with explicit small initial cases | [Sections 1–3](cloitre-conway/proof.md) |
| Conway depth always reaches the cycle | Written argument with exact initial cases through 52 | [Section 4](cloitre-conway/proof.md) |
| Conway global rational envelope for n>=131072 | Computer-assisted theorem: propagation lemma plus exact finite seed certificate | [Proof](cloitre-conway/proof.md), [certificate](cloitre-conway/conway-results.json) |
| Conway C(n)>=G(n) | Conjecture; checked through F_36=14,930,352; conditional on zero-set containment by a new written proof | [Reduction and audit](cloitre-conway/landing.md#2-an-infinite-arithmetic-lemma-for-the-candidate-equality-set) |
| Conway C(F_k)=F_(k-1) for k>=2 | Conjecture; checked through k=36; sufficient neighborhood conditions proved | [Basin criterion](cloitre-conway/landing.md#3-a-precise-sufficient-condition-for-the-fibonacci-basin) |
| Every equality occurs at F_k or F_k±1 | False | Counterexamples 11,24,25,59 |
| Refined equality-set description | Conjecture; checked through F_36, with 86 equalities | [New audit](cloitre-conway/landing-audit.json) |
| G(a)+G(b)>=G(a+b) for all a,b in the candidate Z, except (2,2) | Written proof for the entire infinite candidate set | [Arithmetic lemma](cloitre-conway/landing.md#2-an-infinite-arithmetic-lemma-for-the-candidate-equality-set) |
| Fibonacci neighborhood inequalities and absence of symmetric two-cycles | Conjectural universally; all neighborhoods checked for 6<=k<=36 | [Precise hypotheses](cloitre-conway/landing.md#3-a-precise-sufficient-condition-for-the-fibonacci-basin) |
| C(n)/n tends to 1/phi; quarter-power logarithmic decay | Open; sampled 0.087 +/-0.5% stability is not reproduced | [Decay audit](cloitre-conway/landing.md#4-reproducible-finite-audit) |
| Three shifted Conway/Mallows variants lie on the proposed side of G, with Fibonacci anchors | Finite observation through 2^20, with a(1)=a(2)=1 | [Family audit](cloitre-conway/landing-audit.json) |
| Unbounded periods or an n^0.4 growth law | Open; finite data only | [Orbit tables](cloitre-conway/conway-results.json) |
| Lean formalization | Not undertaken | No Lean theorem claimed |

The main next proof problem is to establish the neighborhood inequalities and
predecessor identities in the new conditional basin theorem, together with
containment of the zero-defect indices in the candidate set. Earlier Fibonacci
identities alone establish a fixed point, not that the prescribed orbit reaches it.

A stronger finite observation from the original audit is: for all a,b<=2^20,
C(a)+C(b)>=G(a+b), except (a,b)=(2,2). This follows from the exact check of
2628 pairs of zero-defect indices and the Beatty-floor inequality. The new
infinite-set lemma proves the pair inequality on the whole candidate Z;
identifying the actual zero set still requires a new argument. The exact carry
has three values, -1,0,+1, and all three occur in the selected splits.

The public repository is the research source and evidence location. Subsequent
substantive results should update this status, the affected proof and its
reproduction records together.

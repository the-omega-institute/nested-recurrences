# Research status

Updated 2026-09-30, Asia/Singapore.

| Claim | Status | Evidence |
|---|---|---|
| Campbell totality and power-of-three formula | Written proof | [Note](campbell/note.pdf) |
| Campbell sharp four-step transient and cycle classification | Written proof; exact symbolic arithmetic checked | [Source](campbell/note.tex), [certificate](campbell/proof-check.json) |
| Conway totality and 3/5, 3/4 ratio bounds | Written induction with explicit small initial cases | [Sections 1–3](cloitre-conway/proof.md) |
| Conway depth always reaches the cycle | Written argument with exact initial cases through 52 | [Section 4](cloitre-conway/proof.md) |
| Conway global rational envelope for n>=131072 | Computer-assisted theorem: propagation lemma plus exact finite seed certificate | [Proof](cloitre-conway/proof.md), [certificate](cloitre-conway/conway-results.json) |
| Conway C(n)>=G(n) for all n>=1 | Computer-assisted theorem: finite base plus general simultaneous induction | [Global proof](cloitre-conway/golden-proof.md#4-simultaneous-induction-g-lower-bound-and-zero-set-containment) |
| Conway C(F_k)=F_(k-1) for every k>=2 | Proved from the global lower bound and Fibonacci upper cap | [Identities](cloitre-conway/golden-proof.md#6-the-upper-cap-fibonacci-identities-and-the-full-equality-set) |
| Every equality occurs at F_k or F_k±1 | False | Counterexamples 11,24,25,59 |
| Refined equality-set description | Exact global theorem; both inclusions proved | [Full equality set](cloitre-conway/golden-proof.md#6-the-upper-cap-fibonacci-identities-and-the-full-equality-set) |
| G(a)+G(b)>=G(a+b) for all a,b in the candidate Z, except (2,2) | Written proof for the entire infinite candidate set | [Arithmetic lemma](cloitre-conway/landing.md#2-an-infinite-arithmetic-lemma-for-the-candidate-equality-set) |
| Fibonacci neighborhood inequalities and absence of symmetric two-cycles | Proved throughout the stated domains | [Neighborhood bounds](cloitre-conway/golden-proof.md#6-the-upper-cap-fibonacci-identities-and-the-full-equality-set) |
| Every orbit at n=F_k, k>=6, reaches F_(k-1) | Global theorem: the cycle-capture interval is a singleton | [Cycle capture](cloitre-conway/golden-proof.md#5-cycle-capture-from-a-fibonacci-anchor) |
| Fibonacci-block upper cap C(n)<=min(n-F_(j-2),F_j) for F_j<=n<F_(j+1), j>=3 | Proved by strong induction after the G lower bound and zero containment | [Upper cap](cloitre-conway/golden-proof.md#6-the-upper-cap-fibonacci-identities-and-the-full-equality-set) |
| liminf C(n)/n=1/phi | Proved from the G lower bound and Fibonacci subsequence | [Corollary](cloitre-conway/golden-proof.md#6-the-upper-cap-fibonacci-identities-and-the-full-equality-set) |
| C(n)/n tends to 1/phi; quarter-power logarithmic decay | Open; sampled 0.087 +/-0.5% stability is not reproduced | [Decay audit](cloitre-conway/landing.md#4-reproducible-finite-audit) |
| Three shifted Conway/Mallows variants lie on the proposed side of G, with Fibonacci anchors | Finite observation through 2^20, with a(1)=a(2)=1 | [Family audit](cloitre-conway/landing-audit.json) |
| Unbounded periods or an n^0.4 growth law | Open; finite data only | [Orbit tables](cloitre-conway/conway-results.json) |
| Lean formalization | Not undertaken | No Lean theorem claimed |

The former landing and zero-set proof problems are now resolved. The new proof
uses only the exact base through 65535 and the seed window [16384,131071],
followed by general inductions and cycle capture. The F36 experiment is
corroboration rather than a premise. Full convergence still requires an upper
limiting bound of 1/phi; the decay exponent and universal shifted-family patterns
remain research questions.

A stronger finite observation from the original audit is: for all a,b<=2^20,
C(a)+C(b)>=G(a+b), except (a,b)=(2,2). This follows from the exact check of
2628 pairs of zero-defect indices and the Beatty-floor inequality. The new
infinite-set lemma proves the pair inequality on the whole candidate Z;
the new simultaneous induction identifies the actual zero set globally. The exact carry
has three values, -1,0,+1, and all three occur in the selected splits.

The public repository is the research source and evidence location. Subsequent
substantive results should update this status, the affected proof and its
reproduction records together.

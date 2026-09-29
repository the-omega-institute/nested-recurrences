# Nested recurrences with variable iteration depth

Research on recurrences in which an earlier sequence value determines the
number of nested iterations. The initial example was proposed by John M.
Campbell; the Conway-type candidate was proposed by Benoît Cloitre.

This repository contains mathematical arguments, exact computation programs,
and reproducible evidence. Written theorems, computer-assisted theorems and
finite observations are distinguished below. Neither example has been
formalized in Lean.

## Campbell's recurrence: explicit formula proved

Define

$$
b(1)=1,\qquad T_n(x)=n-b(x),\qquad
b(n)=T_n^{b(n-1)}(n-1)\quad(n\ge2).
$$

If s is the unique power of 3 in the indicated interval, then

$$
\begin{aligned}
b(n)&=\min(n-s,3s),&&n\text{ even},\quad2s\le n<6s,\\
b(n)&=\max(2s,n-3s),&&n\text{ odd},\quad3s\le n<9s.
\end{aligned}
$$

Every starting orbit satisfies T_n^6(n-1)=T_n^4(n-1). The preperiod bound four
is sharp, and the eventual period is one or two. The formula gives b(3n)=3b(n)
for n>=2 and ratio limits liminf b(n)/n=2/5, limsup b(n)/n=3/4.

- [Complete proof PDF](campbell/note.pdf) and [LaTeX source](campbell/note.tex).
- [Reproduction instructions](campbell/README.md), [exact symbolic checker](campbell/check_proof.py),
  and [recorded checks](campbell/proof-check.json).
- The original recurrence agrees with the formula through 1,000,000 terms;
  literal nesting independently agrees through 5,000 terms.

## Cloitre's Conway candidate: proved bounds and open structure

Define C(1)=C(2)=1 and, for n>=3,

$$
T_n(x)=n-C(x),\qquad g=T_n^{C(n-1)}(n-1),\qquad
C(n)=C(g)+C(n-g).
$$

[The research note](cloitre-conway/proof.md) proves totality, the sharp bounds
3n/5<=C(n)<=3n/4 for n>=3, and that the chosen depth always reaches the cycle.
Its split-separation lemma propagates ratio bounds from [M,8M-1] to all n>=M.
An exact finite seed certificate consequently proves

$$
\frac{121393}{196418}\le\frac{C(n)}n\le\frac{103088}{155677}<\frac23
\qquad(n\ge131072).
$$

The two rational bounds are approximately 0.6180339887383030 and
0.6621915889951631. The lower one is about 1.1592e-11 below 1/phi; it does not
establish an exact golden-ratio limit.

Independent full-orbit and Brent implementations agree through 2^20=1,048,576,
with a literal check through 4096. The largest observed period is 106 and the
largest observed preperiod is 211. These maxima are finite observations.

The conjectures C(n)>=G(n) and C(F_k)=F_(k-1), k>=2, hold throughout the
computed range but still lack universal proofs. Equality C(n)=G(n) is **not**
confined to Fibonacci numbers and their immediate neighbors: 11,24,25,59 are
counterexamples. The note states a refined equality-set conjecture.

- [Proofs, counterexamples and remaining gaps](cloitre-conway/proof.md).
- [Exact experiment and certificate generator](cloitre-conway/conway_explore.py).
- [Recorded results and complete orbit witnesses](cloitre-conway/conway-results.json).
- [Current research status and next questions](STATUS.md).

## Reproduce all recorded checks

Python 3.10 or newer and its standard library are sufficient:

```sh
python3 scripts/verify.py
```

The verifier reruns both sequences and the symbolic interval checker, compares
the resulting JSON with the committed evidence, and checks the recorded source
hash. Run without Python's `-O` option or `PYTHONOPTIMIZE`: assertions are part
of the mathematical checks. PDF rebuilding is optional and described in the
Campbell directory.

## Attribution and research practice

Campbell and Cloitre are credited for their respective recurrence proposals.
This repository does not set a paper's author list or claim a journal
submission. The Campbell note retains its unsigned presentation.

AI assistance was used in exploration, proof development, implementation and
writing. Each result states its actual verification scope; executable checks
are not described as Lean proofs. The related Grytczuk paper is *Another
variation on Conway's recursive sequence* (2004),
[DOI: 10.1016/j.disc.2003.10.022](https://doi.org/10.1016/j.disc.2003.10.022).
Its relationship to the new candidate and the priority of individual methods
remain subjects for literature review.

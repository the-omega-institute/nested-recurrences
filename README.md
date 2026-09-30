# Nested recurrences with variable iteration depth

Research on recurrences in which an earlier sequence value determines the
number of nested iterations. The initial example was proposed by John M.
Campbell; the Conway-type candidate was proposed by Benoît Cloitre.

## Start here: read the mathematics

Everything can be read in your web browser. No GitHub account, installation,
or programming knowledge is needed.

| What would you like to read? | Open this document | What it contains |
|---|---|---|
| The complete solution of Campbell's first example | **[Three-page proof (PDF)](campbell/note.pdf)** | The explicit formula, why the nested iterations stabilize, and the ratio limits |
| The golden structure of Cloitre's Conway-type example | **[Global proof](cloitre-conway/golden-proof.md)** | The G lower bound, exact equality set, Fibonacci landing and golden-ratio liminf |
| A quick overview of what is proved and what remains open | **[Current research status](STATUS.md)** | A claim-by-claim table and the next proof problem |

For the recurrence and earlier ratio bounds, read the original note's
[definition](cloitre-conway/proof.md#definition-and-result-status) and
[global bounds](cloitre-conway/proof.md#3-finite-window-propagation-and-explicit-infinite-bounds).
For the new proof, start with
[the simultaneous induction](cloitre-conway/golden-proof.md#4-simultaneous-induction-g-lower-bound-and-zero-set-containment),
then [the upper cap and Fibonacci identities](cloitre-conway/golden-proof.md#6-the-upper-cap-fibonacci-identities-and-the-full-equality-set).
The [status page](STATUS.md) lists the remaining questions about convergence and decay.

**Reading on GitHub:** click any document link above to open it. The PDF can be
read in the preview; if the preview is unavailable, use **Download raw file**
(the download-arrow button) to open a local copy. The research note is a normal
web page. Your browser's Back button returns here. You can ignore the file list
and the Code button above this page.

Comments, corrections and proposed arguments are welcome in our existing email
thread. There is no need to learn GitHub Issues or submit a pull request.

**Latest research update:** [Global golden structure](cloitre-conway/golden-proof.md).
The G lower bound, exact equality set, Fibonacci identities and landing are now
proved, together with a Fibonacci-block upper cap and liminf C(n)/n=1/phi.
The proof uses a checked finite base followed by general induction. Full
convergence and decay rates remain open; the reported decay precision has been
corrected in the [earlier audit](cloitre-conway/landing.md).

## Results at a glance

- **Campbell's example: explicit formula proved.** The prescribed orbit reaches
  a fixed point or a two-cycle after at most four transient steps. A complete
  written proof is available in the PDF.
- **Cloitre's example: golden structure proved.** We prove
  that the recurrence is well-defined and that its chosen iteration depth
  reaches a cycle. A propagation argument and an exact finite computation give
  the universal rational bounds below. A further induction proves the Hofstadter
  G lower bound and exact equality set. The Fibonacci identities, landing
  theorem and golden-ratio liminf follow from a new upper cap.
- **Next question:** does the entire ratio C(n)/n converge to 1/phi, and at
  what rate? The liminf is established; controlling the limsup remains open.

The following sections give the precise statements. Code and recorded data are
optional supporting material, collected under **Optional: reproduce the checks**.

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

## Cloitre's Conway candidate: golden structure proved

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

The statements C(n)>=G(n) and C(F_k)=F_(k-1), k>=2, are now universal theorems
in the [global golden-structure proof](cloitre-conway/golden-proof.md).
Equality C(n)=G(n) is **not**
confined to Fibonacci numbers and their immediate neighbors: 11,24,25,59 are
counterexamples to that older claim. The corrected equality set is now proved
exactly, including those four exceptional indices.

- [Proofs, counterexamples and remaining gaps](cloitre-conway/proof.md).
- [Exact experiment and certificate generator](cloitre-conway/conway_explore.py).
- [Recorded results and complete orbit witnesses](cloitre-conway/conway-results.json).
- [Current research status and next questions](STATUS.md).

## Optional: reproduce the checks

The proofs and research notes above can be read without running any code.
For readers who want to audit the computations, the files have these roles:

| File type | Purpose |
|---|---|
| `.pdf` | A typeset proof to read or print |
| `.md` | A note displayed as a web page on GitHub |
| `.py` | A Python program for reproducing computations |
| `.json` | Recorded exact results for comparison with a new run |
| `.tex` | The editable LaTeX source of the PDF |

<details>
<summary>Show the command and technical reproduction instructions</summary>

After downloading or cloning this repository, open a terminal in its main
folder (the folder containing this README).

Python 3.10 or newer and its standard library are sufficient:

```sh
python3 scripts/verify.py
```

The verifier reruns both sequences and the symbolic interval checker, compares
the resulting JSON with the committed evidence, and checks the recorded source
hash. Run without Python's `-O` option or `PYTHONOPTIMIZE`: assertions are part
of the mathematical checks. PDF rebuilding is optional and described in the
Campbell directory.

For separate instructions, see the [Campbell guide](campbell/README.md#optional-computational-checks)
or the [Conway guide](cloitre-conway/README.md#optional-computational-checks).

</details>

## Attribution and research practice

Campbell and Cloitre are credited for their respective recurrence proposals.
This repository does not set a paper's author list or claim a journal
submission. The Campbell note retains its unsigned presentation.

AI assistance was used in exploration, proof development, implementation and
writing. Each result states its actual verification scope; neither example has
been formalized in Lean. The related Grytczuk paper is *Another
variation on Conway's recursive sequence* (2004),
[DOI: 10.1016/j.disc.2003.10.022](https://doi.org/10.1016/j.disc.2003.10.022).
Its relationship to the new candidate and the priority of individual methods
remain subjects for literature review.

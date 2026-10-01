# Nested recurrences with variable iteration depth

Research on recurrences in which an earlier sequence value determines the
number of nested iterations. John M. Campbell proposed the first example;
Benoît Cloitre proposed the Conway-type candidate.

## Start here

Everything below can be read in your browser. No GitHub account, installation
or programming knowledge is needed.

| Reading goal | Document |
|---|---|
| Read the complete solution of Campbell's example | **[Three-page proof (PDF)](campbell/note.pdf)** |
| Read the main theorem for Cloitre's example | **[Global golden structure](cloitre-conway/golden-proof.md)** |
| Understand cycles and convergence near Fibonacci indices | **[Fibonacci collars](cloitre-conway/fibonacci-collars.md)** |
| Follow the proposed decay proof and its remaining inequality | **[Martingales and dispersion](cloitre-conway/fibonacci-collars.md#size-biased-martingales-and-the-four-generation-dispersion-criterion)** · **[Basin lower bound without choosing a phase](cloitre-conway/fibonacci-collars.md#a-phase-free-lower-bound-from-the-prescribed-basin)** |
| See how another value-preserving split can support a decay proof | **[Additive policies and their exact proof contract](cloitre-conway/fibonacci-collars.md#additive-dispersion-policies-without-orbit-qualification)** |
| Understand why matching a long prefix and every fixed collar still does not prove convergence | **[Explicit nonconvergent extensions](cloitre-conway/fibonacci-collars.md#finite-prefixes-and-exact-collars-do-not-force-convergence)** |
| Understand how quickly an orbit enters a Fibonacci neighborhood | **[Quantitative capture](cloitre-conway/fibonacci-collars.md#quantitative-capture-and-a-short-exterior-certificate)** |
| See how long orbit runs can be checked by arithmetic blocks | **[Return certificates](cloitre-conway/fibonacci-collars.md#defect-plateau-return-certificates)** |
| See the common five-window closure interface and the exact conditional phase minimum | **[Closure theorem](cloitre-conway/fibonacci-collars.md#9-common-closure-theorem-and-generic-minimality)** · **[Phase readout](cloitre-conway/fibonacci-collars.md#the-exact-minimum-phase-interface-depends-on-the-readout)** |
| Understand the extra information needed to recover child branches | **[Seed reconstruction](cloitre-conway/fibonacci-collars.md#seed-reconstruction-and-the-remaining-branch-information)** · **[Minimum cycle checks](cloitre-conway/fibonacci-collars.md#minimal-periodicity-checks-for-inverse-reconstruction)** |
| Check inverse uniqueness with a small graph and a hand-worked example | **[Gap graph and reverse completeness](cloitre-conway/fibonacci-collars.md#a-bounded-gap-automaton-with-reverse-completeness)** |
| See the minimum total defect needed for a proper cycle | **[Cycle defect cost](cloitre-conway/fibonacci-collars.md#minimum-defect-cost-of-a-proper-cycle)** |
| Understand recursive descent and its extra inverse-label budget | **[Recursive windows](cloitre-conway/fibonacci-collars.md#recursive-windows-with-a-parameter-at-every-row)** · **[Conserved branch budget](cloitre-conway/fibonacci-collars.md#a-conserved-budget-for-multiscale-inverse-labels)** |
| See how repeated inputs can eliminate inverse branch labels | **[Shared selectors and the two-label theorem](cloitre-conway/fibonacci-collars.md#sharing-selectors-at-repeated-physical-indices)** |
| Understand sharing between windows and a basis for their parameters | **[Shared network and forest basis](cloitre-conway/fibonacci-collars.md#a-shared-parameter-network-and-its-forest-basis)** |
| See how child layouts and values can be recovered without a C table | **[Sublinear shared descent code](cloitre-conway/fibonacci-collars.md#generating-the-layout-from-a-sublinear-shared-descent-code)** |
| Read growing exact collars, phase rules and nearby cycle exclusions | **[Growing positive collars](cloitre-conway/fibonacci-collars.md#every-fixed-positive-offset-eventually-becomes-linear)** · **[Saturated profiles](cloitre-conway/fibonacci-collars.md#a-saturated-lower-barrier-and-the-exclusion-of-nearby-proper-cycles)** |
| Connect the five legal Fibonacci digit patterns to a checked local interaction | **[Five-pattern readout and eventual additivity](cloitre-conway/fibonacci-collars.md#five-legal-bit-patterns-and-eventual-vanishing-of-a-local-interaction)** |
| See a complete geometric selector code and the remaining real-orbit constraint | **[Seven terminal symbols](cloitre-conway/fibonacci-collars.md#seven-terminal-symbols-and-the-full-geometric-selector-code)** · **[Growing defects and occupation](cloitre-conway/fibonacci-collars.md#growing-actual-defects-and-the-remaining-occupation-problem)** |
| See what is proved and what remains open | **[Current status](STATUS.md)** |

Click a link to read its document, then use your browser's Back button to
return here. The PDF has a GitHub preview; if it does not load, use
**Download raw file** (the download-arrow button). You can ignore the Code
button and the file list. Comments and proposed arguments are welcome in our
existing email thread; there is no need to learn GitHub Issues or pull requests.

## What is proved

**Campbell's recurrence.** The [PDF](campbell/note.pdf) gives an explicit
formula organized by powers of three. The prescribed inner orbit reaches a
fixed point or two-cycle after at most four transient steps. The ratio has
liminf 2/5 and limsup 3/4.

**Cloitre's recurrence.** The [global proof](cloitre-conway/golden-proof.md)
establishes the Hofstadter G lower bound, the exact equality set (including
11, 24, 25 and 59), Fibonacci identities and orbit landing, a Fibonacci-block
upper cap, and liminf C(n)/n=1/phi. This is a computer-assisted theorem:
the general induction and its exact finite premises are stated separately.
The [collar proof](cloitre-conway/fibonacci-collars.md) then bounds all cycle
periods near Fibonacci indices, classifies offsets -2 through +2, and proves
ratio convergence throughout sublinear-width Fibonacci neighborhoods.
The maintained notes now also give a shorter finite-certificate theorem and
the improved global upper bound 8900/13459 for n>=349525, together with exact
values and complete nearby cycles in the band -12<=t<=32 for all high-order
Fibonacci indices. See [current status](STATUS.md) for the thresholds and evidence.

The [growing positive collar theorem](cloitre-conway/fibonacci-collars.md#every-fixed-positive-offset-eventually-becomes-linear)
now proves the exact linear value at every fixed positive offset for all
sufficiently large orders, with an explicit threshold. Arithmetic selected
endpoints are also proved on a domain whose width grows with the order.
The wider Fibonacci-block centers remain open.

The [dispersion criterion](cloitre-conway/fibonacci-collars.md#size-biased-martingales-and-the-four-generation-dispersion-criterion)
gives a concrete route to a decay bound through two exact martingales.
Its implication is proved and finite actual checks support it, but the
uniform dispersion inequality remains open. A shared geometric counterfamily
shows that geometry and terminal values alone are insufficient.
Taking the worst phase in the prescribed-start basin gives a proved lower
envelope, supported by exact finite checks through131071. This is a route
to the missing inequality that does not require the precise depth phase;
the basin and its profiles still need certification across all orders.
For the asymptotic proof, another route may choose any split that preserves
the actual scalar value and child blocks. The same two martingales hold,
even when that split is transient under the original inner map. This
removes orbit qualification from the sufficient policy criterion; its
uniform dispersion premise is still open.

The [nonconvergent-extension theorem](cloitre-conway/fibonacci-collars.md#finite-prefixes-and-exact-collars-do-not-force-convergence)
now identifies a stronger obstruction. Explicit scalar extensions can agree
with any prescribed finite actual prefix, retain the same golden lower bound,
upper cap, exact equality set and proved fixed collars, and inherit any
certified ratio envelope after a sufficiently late cutoff, yet have a
nonconvergent ratio. Their fixed five-pattern interactions also vanish.
For the cutoff F_25=75025, the first difference is 75067: the extension
gives 46410, while the prescribed nested recurrence gives 46407.
This isolates the missing global restriction on the actual profiles or
their selected dynamics; it does not refute convergence for actual C.

**Still open:** full convergence of C(n)/n, its decay rate, and the growth
of periods and landing times away from Fibonacci neighborhoods.
See [status and next questions](STATUS.md) for the precise scope.

For detailed reading routes and the recurrence definitions, use the
[Campbell guide](campbell/README.md) or [Conway guide](cloitre-conway/README.md).
Supporting lemmas remain at stable links; code and recorded evidence are
grouped in each example's `verification/` directory.

## Optional: reproduce the computations

<details>
<summary>Show verification instructions</summary>

From the repository's main folder, with Python 3.10 or newer:

```sh
python3 scripts/verify.py
```

This reruns eight checks, compares their exact JSON output with committed
evidence, and checks recorded source hashes. Use
`python3 scripts/verify.py --extended` to include the larger F_36 and shifted-family
audit. Run without `-O` or `PYTHONOPTIMIZE`; assertions perform mathematical checks.

Only the Python standard library is needed. Separate instructions and optional
PDF rebuilding are in the [Campbell guide](campbell/README.md#optional-computational-checks)
and [Conway guide](cloitre-conway/README.md#optional-computational-checks).
Recorded experiment reports describe their verification scope when generated;
the [status page](STATUS.md) gives the current theorem status.

</details>

## Attribution and research practice

Campbell and Cloitre are credited for their respective recurrence proposals.
No paper author list or journal submission is established here; the Campbell
note remains unsigned. AI assistance was used in exploration, proof development,
implementation and writing. No Lean formalization is claimed.

The related Grytczuk paper is *Another variation on Conway's recursive sequence*
(2004), [DOI: 10.1016/j.disc.2003.10.022](https://doi.org/10.1016/j.disc.2003.10.022).
Its relationship to this candidate and priority questions remain subjects for
literature review.

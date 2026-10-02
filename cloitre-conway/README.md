# Cloitre's variable-depth Conway recurrence

[Project home](../README.md) · [Results and open questions](../STATUS.md)

**The golden-ratio lower structure is proved. The full ratio limit remains
open.** Start with the definition and main result below; the technical map
is for readers who want to follow a particular research question.

## Definition

Set C(1)=C(2)=1. For n>=3, let T_n(x)=n-C(x), start at x_0=n-1,
and use exactly C(n-1) iterations:

$$
g=T_n^{\,C(n-1)}(n-1),\qquad C(n)=C(g)+C(n-g).
$$

The first terms are 1, 1, 2, 3, 3, 4, 5, 5, 6, 7. Benoît Cloitre
proposed this candidate. The starting point and exact iteration count
are part of the definition.

## What is proved, and what is missing?

Let phi=(1+sqrt(5))/2 and F_k be the Fibonacci numbers. We have proved

$$
C(n)\ge\lfloor(n+1)/\phi\rfloor,\qquad
C(F_k)=F_{k-1}\ (k\ge2),\qquad
\liminf_{n\to\infty} C(n)/n=1/\phi.
$$

The equality set and a global upper cap are also proved. These conclusions
use an induction with explicitly checked finite premises. They do not yet
show that C(n)/n converges: we must control the values between Fibonacci
indices, and then establish a decay rate.

## A reading route

1. **[Read the main proof](golden-proof.md).** Its opening theorem states
   the global results and identifies the finite premises.
2. **[Read what happens near Fibonacci indices](fibonacci-collars.md).**
   The ratio converges in sublinear-width neighborhoods. The
   [exact-neighborhood note](exact-collars.md) gives exact values and phases.
3. **[Read the remaining convergence problem](dispersion.md).** Exact
   martingale identities give a conditional decay theorem; the required
   uniform dispersion inequality is still open.

All notes can be read in your browser, without installing software.
The programs and JSON files are optional evidence, not part of this route.

## Technical research map

The route above is enough to start. Expand this index when you want a
particular theorem or are working on the recursive interface.

<details>
<summary>Show the technical topics and their prerequisites</summary>

A cap defect measures how far a value lies below the Fibonacci upper cap;
a profile records the defects across a neighborhood. The linked proofs give
exact definitions, domains and supplied inputs.

| Topic | Read in this order | Prerequisites |
|---|---|---|
| Global theorems | [Foundations](proof.md) → [Golden structure](golden-proof.md) | The definition; explicit finite certificates |
| Fibonacci neighborhoods | [Orbit bounds](fibonacci-collars.md) → [Exact values and phases](exact-collars.md) | Global theorems; stated finite seeds |
| Local cycles and actual recursive choices | [Five-window interface](five-window-closure.md) → [Inverse reconstruction](inverse-reconstruction.md) → [Recursive descent](recursive-descent.md) | Global structure; the supplied profiles and context in each theorem |
| Convergence and decay | [Martingales and dispersion](dispersion.md) | Additive child blocks; the stated scalar or moment conditions |
| Digit encoding and feature interactions | [Cloitre memory theorem](five-window-closure.md#exact-state-bit-order-for-every-bounded-cap-graph) · [Cloitre interactions](exact-collars.md#a-persistent-interaction-on-canonical-index-words) · [Campbell comparison](../campbell/scale-memory.md) | Fibonacci digits; exact neighborhood and ternary formulas |
| Supporting arithmetic and related variants | [Landing and shifted-family audit](landing.md) | Foundations |

For the current recursive-interface question, the
[child-cap allocation theorem](recursive-descent.md#actual-defect-allocation-and-phase-information)
replaces separate cycle and phase labels with one allocation parameter when
the lower profiles and parent value are supplied. That parameter is derived
at cap4; its general selection and construction of the required profiles
remain open. The [direct descendant decoder](exact-collars.md#additive-canonical-windows-and-a-direct-descendant-decoder)
handles a particular canonical family; it does not close the full recursion.
The [profile query theorem](recursive-descent.md#cap4-query-profiles-and-the-information-they-carry)
shrinks the required lower-profile interval and distinguishes its arithmetic
information from cycle-phase information.
The [propagated cap4 band](exact-collars.md#a-propagated-cap4-band-generates-its-own-profiles)
generates that profile and its selected descendants in a growing initial
region. A [canonical family](exact-collars.md#a-canonical-cap4-window-reaches-the-next-fibonacci-digit)
shows why even its first edge can need a higher Fibonacci digit in the output.
The [bounded-tail theorem](exact-collars.md#a-bounded-upper-shelf-and-a-wider-zero-allocation-corridor)
bounds the remaining responses near that band and derives zero allocation
in a wider region, including higher caps.
Its first thirteen translated-tail positions have the proved alphabet
{4,8,9}; the word is explicit, so order and gaps suffice for their descent.
Profiles beyond this arithmetic region remain open.
The [finite-alphabet extension](exact-collars.md#a-finite-alphabet-propagates-beyond-the-zero-allocation-corridor)
propagates a wider bounded response alphabet and zero allocation from one
seed. A high-cap spine has only finitely many strict position drops;
eventual flattening would require control of persistent high-member choices
on two-cycles. A local depth-parity shortcut fails in actual examples.
The [frontier reset rule](recursive-descent.md#an-even-landing-determines-a-frontier-phase)
replaces the full entry clock by a bit derived from a qualified even landing
and one tail response. The same phase bit transfers a five-pattern joint
interaction between scalar values and child indices. Generating the exterior
landing locally remains open.

The local interface theorems state exactly which context is supplied.
For a bounded natural-cap domain, the
[least recursive completion](five-window-closure.md#the-least-recursive-completion-adds-fibonacci-anchors)
adds Fibonacci anchors to the declared finite base; its actual value and
selected-split graphs have the proved state-bit order.
A candidate geometric cycle, a finite numerical test, and an actual selected
recursive orbit are distinct objects. The [status page](../STATUS.md) tracks
the unresolved full-interface and asymptotic questions.

</details>

## Optional computational checks

Programs and compact evidence live in [verification/](verification/).
With Python 3.10 or newer, run this from the repository root:

```sh
python3 scripts/verify.py
```

This reruns eight checks and compares exact JSON output and source hashes.
Only the standard library is needed. Run without `-O` or `PYTHONOPTIMIZE`.
The [verification guide](../CONTRIBUTING.md#reproduce-the-evidence) explains
the independent evaluators, finite certificates, and optional larger audit.

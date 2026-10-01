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

| Question | Note | Starting point |
|---|---|---|
| Is the sequence well defined, and does its depth reach a cycle? | [Foundations](proof.md) | The definition |
| What global golden bounds and Fibonacci identities are proved? | [Global golden structure](golden-proof.md) | Foundations and explicit finite certificates |
| How are cycles captured near Fibonacci indices? | [Orbit bounds](fibonacci-collars.md) | Global golden structure |
| Which nearby values, cycles, and selected phases are exact? | [Exact collars](exact-collars.md) | Capture and stated finite seeds |
| What closes a local reflection window, and what phase information does an output need? | [Profiles and five-window closure](five-window-closure.md) | Global structure and profile identities |
| Can candidate cycles be reconstructed and qualified? | [Inverse reconstruction](inverse-reconstruction.md), including the [unique odd-window decoder](inverse-reconstruction.md#golden-defect-words-give-a-uniform-cyclic-decoder) | Reflection-window equations; ordered golden defects for the conditional decoder |
| What information closes recursive descent and selects its children? | [Recursive descent](recursive-descent.md), including the [cap budget](recursive-descent.md#a-quadratic-enclosure-for-every-bounded-cap-level), [modular decoder](recursive-descent.md#a-modular-symbolic-selector-with-small-working-memory) and [child-cap allocation seed](recursive-descent.md#actual-defect-allocation-and-phase-information) | Profiles and certified entrance for the modular decoder; parent scalar and allocation for the periodic seed |
| What would prove a global decay rate, and what dispersion is already proved? | [Martingales and dispersion](dispersion.md), including the [logarithmic horizon](dispersion.md#a-logarithmic-horizon-from-one-retained-child) and [two-split moment policies](dispersion.md#two-split-moment-policies-and-cycle-average-dispersion) | Profile identity, additive child blocks and the stated scalar or moment conditions |
| How much memory does canonical digit recognition require? | [Cloitre bounded-cap graphs](five-window-closure.md#exact-state-bit-order-for-every-bounded-cap-graph) · [Campbell comparison](../campbell/scale-memory.md) | Cap budget; exact plateau; Campbell's formula |
| When does a canonical window have a persistent feature interaction, and how do its descendants change context? | [Cloitre family](exact-collars.md#a-persistent-interaction-on-canonical-index-words) · [Additive table and direct descendant decoder](exact-collars.md#additive-canonical-windows-and-a-direct-descendant-decoder) · [Campbell comparison](../campbell/scale-memory.md#five-pattern-interaction-on-ternary-scale-interiors) | Unit-defect arithmetic descent; ternary formula |
| What arithmetic supports the global induction and shifted-family tests? | [Supporting arithmetic and audit](landing.md) | Foundations |

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

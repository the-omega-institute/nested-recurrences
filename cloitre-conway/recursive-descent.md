# Recursive descent, shared selectors, and information budgets

[Project home](../README.md) · [Research map](README.md#technical-research-map)

This note extends [one-row reconstruction](inverse-reconstruction.md)
to descendants. Shared physical indices reduce selector labels; a forest
basis and descent code account for cross-row parameters and layouts.
These qualified reconstruction results do not establish a uniform occupation
or dispersion bound for actual C.

An actual closed arithmetic subclass is now available on the
[moving negative plateau](exact-collars.md#exact-moving-negative-plateau-and-arithmetic-closure).
Its exact gap range0..floor(2k/3)-3 grows with the anchor order. Fixed-point
rows retain their gap; the newly added two-cycle endpoint gives child gaps
v-1 and1. Every child remains in the lower-order plateau, so five-row words
need zero residual selectors with order and gaps supplied, down to finite
base orders9/10. Scale, gap encoding and base-table costs remain separate;
the full actual-C minimum in wide arches is still open.

The [unit-defect sublevel theorem](exact-collars.md#the-unit-defect-sublevel-set-and-its-arithmetic-spine)
extends this actual closure to a nonconstant profile family. A cap defect1
follows a single first-child spine, while every second child is in the zero
plateau. Order and gaps determine shifts0,1,2 and both boundary phases,
so zero residual selector labels still suffice down to finite orders18/19.
The same domain has a proved
[quadratic basin dispersion bound](dispersion.md#quadratic-basin-dispersion-in-the-unit-defect-family).
Full context costs and dispersion in the wider block interiors remain open.

The [higher-cap theorem](exact-collars.md#two-higher-cap-levels-and-their-phase-selected-closure)
extends those arithmetic selectors through cap defect3. The general
cap-budget theorem below confines every bounded cap level to a polynomial
Fibonacci neighborhood, even when its support has holes.

## Contents

- [Recursive windows with a parameter at every row](#recursive-windows-with-a-parameter-at-every-row)
- [A quadratic enclosure for every bounded cap level](#a-quadratic-enclosure-for-every-bounded-cap-level)
- [A modular symbolic selector with small working memory](#a-modular-symbolic-selector-with-small-working-memory)
- [Sharing selectors at repeated physical indices](#sharing-selectors-at-repeated-physical-indices)
- [A shared parameter network and its forest basis](#a-shared-parameter-network-and-its-forest-basis)
- [Generating the layout from a sublinear shared descent code](#generating-the-layout-from-a-sublinear-shared-descent-code)
- [A conserved budget for multiscale inverse labels](#a-conserved-budget-for-multiscale-inverse-labels)
- [Seven terminal symbols and the full geometric selector code](#seven-terminal-symbols-and-the-full-geometric-selector-code)
- [Growing actual defects and the remaining occupation problem](#growing-actual-defects-and-the-remaining-occupation-problem)
- [Actual defect allocation and phase information](#actual-defect-allocation-and-phase-information)

### Recursive windows with a parameter at every row

A constant-parameter five-cycle does not generally descend to two
constant-parameter cycles. The exact closed class is larger: a periodic
row-indexed window with parameters `A_0,...,A_(p-1)`. Child offsets need not
be distinct, and the row clock is inherited rather than independently
rotated. This gives a structural recursive closure theorem, while the size
and verification of the selector information remain separate questions.

**Recursive window theorem.** Fix j>=6, p>=1 and a word of natural-block
offsets `0<=u_i<=F_(j-1)`, satisfying

$$
u_{i+1}=A_i-P_j(u_i)\qquad(i\bmod p). \tag{9.4}
$$

For the actual selected split of `n_i=F_j+u_i`, write

```text
a(n_i)=F_(j-1)+r_i,       q_i=u_i-r_i.
```

Then the intersected capture bounds give

$$
\max(0,u_i-F_{j-3})\le r_i\le\min(u_i,F_{j-2}). \tag{9.5}
$$

In particular `0<=r_i<=F_(j-2)` and `0<=q_i<=F_(j-3)`. Define

$$
\alpha_i=r_{i+1}+P_{j-1}(r_i),\qquad
\beta_i=q_{i+1}+P_{j-2}(q_i).
$$

The two children are natural-block windows of the same length p at orders
j-1 and j-2, with

$$
r_{i+1}=\alpha_i-P_{j-1}(r_i),\qquad
q_{i+1}=\beta_i-P_{j-2}(q_i),\qquad
\alpha_i+\beta_i=A_i. \tag{9.6}
$$

The nonnegative profile defects split exactly, row by row and in total.
No independent Fibonacci carry word or child rotation label is required.

**Proof.** For `0<=u_i<F_(j-1)`, apply (1.4) to the selected point of
`T_(F_j+u_i)`. Its lower and upper limits, relative to `F_(j-1)`, are
exactly the two ends in (9.5). At the remaining endpoint
`u_i=F_(j-1)`, the index is F_(j+1), whose selected split is F_j by
Fibonacci landing. Thus `r_i=F_(j-2)` and `q_i=F_(j-3)`, and (9.5) still
holds. The profile identity gives

```text
P_j(u_i)=P_(j-1)(r_i)+P_(j-2)(q_i).
```

Adding the two definitions in (9.6), and using `r_(i+1)+q_(i+1)=u_(i+1)`,
gives `alpha_i+beta_i=u_(i+1)+P_j(u_i)=A_i`. The child transitions are
their defining equations, including the last-to-first edge. Subtracting the
profile identity from `u_i=r_i+q_i` proves defect additivity. The bounds
place both children in their natural blocks; an upper endpoint is simply
the next Fibonacci anchor, represented in the closed interval. QED.

Repeat this theorem at every child of order at least six. The order drops
by one or two at every edge, so a root of order j reaches leaf orders four
or five after at most j-5 edges. At these leaves use the same defining
formula `P_h(v)=C(F_h+v)-F_(h-1)`; their indices are at most F_6=8. This proves
termination of the structural window descent, without assuming order-uniform
defects or a finite alphabet. The two children retain the parent's row
indexing throughout. If one chooses to canonicalize a child by rotation, its
rotation must be restored before using the rowwise complement identity.

For the first arch at n=196, the canonical parent offset word is
`(26,31,27,28,29)` at profile order 11, with all A_i=52. Its children are

```text
r     = (10,20,16,12,18),       q    = (16,11,11,16,11),
alpha = (29,31,26,29,26),       beta = (23,21,26,23,26).
```

Both parameter words vary, and each row sums to 52. They are exact closed
nonautonomous windows; neither is thereby a constant-parameter lower C orbit.
The verifier recursively replays all thirteen public five-window roots and
additional boundary words of lengths 1,2,3,5,6 down to the small leaves,
preserving row alignment, profile identities and defect sums. Selected splits
used in the trees are independently checked by literal iteration at their
physical indices, with no phase shortcut.

For the minimum-information question, the consequence is specific. Store one
child parameter word alpha; beta is derived from `A-alpha`. The seed/fiber
theorems apply unchanged to the first child word. Block alignment and the
row clock add no independent labels. What is still needed is a certificate
that the recovered r_i are the actual selected splits of the physical n_i,
including their prescribed basins and entry-aligned phases. The row clock
of (9.4) is not the iteration phase in those separate physical orbits.

An arbitrary raw decomposition may fail (9.5). The interval can therefore
be added to each candidate domain at no extra coordinate cost; it preserves
the actual word but does not prove inverse uniqueness or selected validity.
The raw domains of the earlier collision examples remain exactly as stated.
The binary descent tree may also have many nodes: termination is not a bound
on a compact certificate's total size. Campbell's ternary endpoint templates
already provide uniform branch and prescribed-phase information; the new
C theorem establishes the recursive coordinate class, while that comparable
compression remains open.

At the upper edge of a natural block, the
[single-seed negative collar](exact-collars.md#large-natural-block-defects-with-no-residual-selector-labels)
now gives a closed arithmetic subclass: for u_i=F_(j-1)-v_i its selected
child offsets are r_i=F_(j-2)-v_i and q_i=F_(j-3), with no residual selector
labels above the seed boundary. Its natural defects F_(j-3)-v_i grow without
bound. This is an actual-C example in which the sufficient defect budget
does not measure a necessary branch-information cost; the scale, row clock,
and collar qualification remain supplied context.

### A quadratic enclosure for every bounded cap level

The upper-anchor cap defect is different from the natural profile defect
used later in the inverse-label budget. Let

$$
Q_k(v)=F_{k-1}-C(F_k-v),\qquad0\le v\le F_{k-2}.
$$

Define P_9=13 and, for k>=10,

$$
P_k=\left\lfloor\frac{(k-2)^2}3\right\rfloor-3k+30.
$$

**Cap-budget theorem.** On every full closed block at k>=9,

$$
Q_k(v)=0\ \Longrightarrow\ v\le L_k=\lfloor2k/3\rfloor-3,
\qquad
Q_k(v)>0\ \Longrightarrow\boxed{v\le Q_k(v)P_k}. \tag{C.1}
$$

Since L_k<=P_k, for every integer m>=1 the entire sublevel Q_k<=m
is contained in0..mP_k, regardless of any holes. The enclosure is
O(mk^2), rather than an exact support classification.

**Proof.** The zero case is the proved moving-plateau theorem.
At orders9/10 the full gap lengths are13/21, so positive integral
defects prove (C.1) immediately; there is no new finite sequence premise.
For k>=11, the closed-block capture and scalar identity give actual
child gaps r,q in their natural blocks and child cap defects e_1,e_2 with

$$
v=r+q,\qquad e=Q_k(v)=e_1+e_2,\qquad e_1,e_2\ge0. \tag{C.2}
$$

The budget satisfies

$$
P_k=P_{k-1}+L_{k-2}\ge P_{k-2}+L_{k-1}. \tag{C.3}
$$

The equality follows from
sum_(j=0)^M floor(2j/3)=floor(M^2/3). The inequality is immediate
at k11; subsequently P_(k-1)-P_(k-2)=L_(k-3)>=3, whereas
L_(k-1)-L_(k-2)<=1.
If both child defects are positive, induction gives
v<=e_1P_(k-1)+e_2P_(k-2)<=eP_k. If only e_1 is positive,
v<=eP_(k-1)+L_(k-2)<=eP_k, since e>=1. If only e_2 is
positive, use v<=L_(k-1)+eP_(k-2)<=eP_k. These are all cases
when e>0. QED.

Thus for v>L_k we have Q_k(v)>=ceil(v/P_k). For fixed m,
all indices with cap defect at mostm approach the golden ratio
uniformly over that entire sublevel. More precisely, if F_k>mP_k,
write alpha=1/phi. Since
F_(k-1)-alpha F_k=(-1)^k alpha^k, (C.1) gives

$$
\left|\frac{C(F_k-v)}{F_k-v}-\alpha\right|
\le\frac{m(\alpha P_k+1)+\alpha^k}{F_k-mP_k}. \tag{C.4}
$$

The right side is O(mk^2/F_k). The conclusion also holds for growing
m=m_k whenever m_k k^2=o(F_k). This is a consequence for bounded
cap sublevels, not a proof that the full sequence stays in such levels.

Integer conservation in (C.2) has a separate
[dispersion consequence](dispersion.md#cap-adaptive-quadratic-dispersion).
Before encountering a zero-cap child or cap at most3, both positive
child caps are strictly smaller than the parent. A stopped lower envelope
therefore reaches the arithmetic low-cap kernel in a cap-dependent
number of generations. It proves a quadratic bound, allowing every
scalar-valid geometric high-cap split without entrance or phase data.
This sufficient information for dispersion does not select the actual
child indices required by the decoder below.
An [explicit nonconvergent extension](dispersion.md#exact-small-cap-closure-still-does-not-force-convergence)
preserves these cap budgets, the exact cap0..3 closure and their local
prescribed selection. Global convergence still requires actual orbit
restrictions beyond that domain.

The [one-child transfer theorem](dispersion.md#a-logarithmic-horizon-from-one-retained-child)
shortens the sufficient variance horizon to O(log(e+1)), with a
cap-dependent constant. At a positive-cap branch, one child has at
most half the parent cap. The parent's local variance controls the gap
ratio if only that child is retained. Thus each candidate dispersion
certificate needs one weighted spine per row; full two-child window
reconstruction remains a different information requirement.

**A compact local selector interface.** For sufficiently high k at
fixed m, mP_k<=F_(k-4). Let K(m) be the first k>=11 satisfying
this inequality; it then persists. Indeed P_(k+1)<=3P_k/2,
because P_k>=2L_(k-1), while F_(k-3)>=3F_(k-4)/2. Exponential
Fibonacci growth ensures K(m) exists. The inequality P_k>=2L_(k-1)
starts at k10 and persists because L increases by at most1 whereas
P increases by at least3. In particular K(4)=17.

For any qualified root N=F_k-v with2<=v<=mP_k, supply the two
lower cap-profile tables Q_(k-1),Q_(k-2) on gaps0..v and the
predecessor cap defect z=Q_k(v+1). The depth is d=F_(k-1)-z.
Also supply a certified first-entry pair (mu,r_0): at clockmu the
prescribed orbit first enters I=[F_(k-1)-v,F_(k-1)] at
F_(k-1)-r_0. Put

$$
\Omega_v(r)=v-Q_{k-1}(r),\qquad
r_d=\Omega_v^{\,d-\mu}(r_0). \tag{C.5}
$$

The anchor-drop bound0<=Q_(k-1)(r)<=floor(2r/3) makes0..v
invariant. Therefore the actual split and parent defect are exactly

$$
g=F_{k-1}-r_d,\qquad
Q_k(v)=Q_{k-1}(r_d)+Q_{k-2}(v-r_d). \tag{C.6}
$$

All children lie in the two supplied natural blocks. A functional-graph
walk of at most v+1 distinct gaps determines the transient and period;
integer division then evaluates the exact, possibly enormous depth.
The prescribed depth reaches the cycle by the established global theorem.
The same tables recover both child profiles and the row-indexed parameters
of any five-row word; the second parameter word is derived by subtraction.
They do not require a single-spine assumption: positive cap defects may
split between two children while preserving (C.2).

The period and number of candidate selected gaps are at mostv+1<=mP_k+1.
With the cycle supplied, a selected-gap label uses at most
ceil(log_2(mP_k+1)) bits; its exact readout quotient can be smaller.
The paired exterior contraction bounds mu by twice the pair budget
from dist(N-1,I), hence mu=O(k). The numerical inputs z,r_0,mu
therefore use O(log m+log k) bits per distinct physical root.
For five roots the order is unchanged. The two profile tables cost
O(mk^2 log(mk)) bits; Fibonacci arithmetic, root indices, and verification
of the exterior trace are separate resources. This is a conditional
selector interface, not an autonomous recognizer or a global minimum.
Computing the exact depth uses Theta(k)-bit Fibonacci integers; the
selector-field bound does not assert that the whole decoder uses only
O(log k) working memory.

The [modular symbolic decoder](#a-modular-symbolic-selector-with-small-working-memory)
below computes the phase and returns indexed gaps without materializing
these large integers.

**Why the entrance certificate remains explicit.** With A=F_(k-1),
B=F_(k-2), J=F_(k-4), the first two prescribed points are

$$
x_1=B-v+z,\qquad
x_2=A+J-v+Q_{k-2}(v-z). \tag{C.7}
$$

Usually x_2>A, outside the supplied negative-window profiles.
Starting (C.5) at clock2 would therefore give a wrong orbit.
The decoder uses the certified entrance clock and point; a theorem
deriving them from local tables alone would require a further argument.

**A nonconstant three-phase obstruction.** An actual cap4 root
is k24,v83,N46285. Its cycle, in increasing physical order, is

```text
28578 -> 28582 -> 28583 -> 28578.
```

The three scalar cap readouts are8,9,4, respectively. The actual
depth28648 selects28583 and gives C(N)=28653. On this supplied
cycle, unrestricted scalar or selected-gap readout has exactly three
phase classes, requiring2 fixed-width bits. Even clocks0,2,4 from
the same cycle start already give all three outputs, so parity is
insufficient for that contract. These clock choices are not three
alternative prescribed depths at this physical index. If the cap4
qualification itself is supplied, only the readout4 is compatible;
it would be incorrect to count2 additional phase bits again in that
smaller qualified contract.

**Cross-family scope.** Campbell's recurrence has no corresponding
additive two-child identity, so this cap-budget proof does not transfer
from the common reflection map alone. Its
[ternary formula](../campbell/README.md) determines the basin and phase
arithmetically, with at most four transient steps and periods1/2.
What transfers is the distinction between supplied arithmetic context,
cycle readout classes, and an independently certified entrance. The
autonomous FIB scale-memory counts remain a separate contract.

The checker verifies (C.1)/(C.2) on all complete blocks9..30,
reconstructs actual small-cap roots through this local interface, and
checks selected endpoints literally. It also records the full finite
level4 supports with their holes; their exact infinite classification
remains open. [Evidence](verification/collar-check.json) distinguishes
the general proof from those finite support and phase witnesses.

### A modular symbolic selector with small working memory

The local selector can be evaluated without constructing the exact depth
F_(k-1)-z or storing a trajectory. This is a uniform decoder relative
to the supplied read-only profiles and certified entrance. It uses
standard Floyd cycle detection and Fibonacci doubling identities.

**Contract and theorem.** Let m>=1, k>=11, N=F_k-v, with
Q_k(v)<=m and 2<=v<=min(mP_k,F_(k-4)). Supply the actual predecessor
defect z=Q_k(v+1), the first-entry clock and gap (mu,r_0), and
read-only random access to Q_(k-1)(0..v). For recovering scalar child
values also supply Q_(k-2)(0..v). The entrance is into the same
interval I=[F_(k-1)-v,F_(k-1)] as in (C.5).

A decoder returns the actual selected gap r_d and symbolic child indices

$$
(k-1,r_d),\qquad(k-2,v-r_d), \tag{C.8}
$$

where (h,r) means F_h-r, using

$$
\boxed{O(\log m+\log k)\text{ working bits}} \tag{C.9}
$$

and O(v+log k) bounded-integer operations and profile queries, excluding
the read-only tables and their construction. Two further table reads
return the child cap defects. These symbolic indices retain inherited
anchor orders, including gap0 aliases. Materializing their binary integer
values would require Theta(k) output bits.

**Find the local cycle.** Omega_v(r)=v-Q_(k-1)(r) maps0..v into itself.
Starting at r_0, Floyd's tortoise-and-hare algorithm finds the cycle-entry
gap c, local transient tau and period p using a constant number of gap
registers and counters. The graph has v+1 vertices, so tau+p<=v+1;
this takes O(v) profile reads. The decoder stores no cycle word or visited
set. The global theorem guarantees that the prescribed depth reaches a
cycle, so d=F_(k-1)-z>=mu+tau. Its selected phase is exactly

$$
\rho=\big(F_{k-1}\bmod p-z-\mu-\tau\big)\bmod p,
\qquad r_d=\Omega_v^{\,\rho}(c). \tag{C.10}
$$

Walking rho<p steps gives the required gap. At p=1 the residue is0.
This handles periods beyond two without replacing their phase by parity.

**Compute only the Fibonacci residue.** Maintain
(a,b)=(F_t,F_(t+1)) modulo p while reading the binary digits of k-1.
The standard doubling identities are

$$
F_{2t}=F_t(2F_{t+1}-F_t),\qquad
F_{2t+1}=F_t^2+F_{t+1}^2.
$$

For digit0 use (F_(2t),F_(2t+1)); for digit1 use
(F_(2t+1),F_(2t)+F_(2t+1)), always modulo p. There are O(log k)
updates. Residues are smaller than p and intermediate products have
O(log p) bits. The exact Fibonacci number is never formed.

The depth-in-cycle inequality also admits a small-register check. Set
S=z+mu+tau and compute min(F_(k-1),S) by saturating both entries of
the elementary Fibonacci recurrence at S, stopping once its first entry
reaches S. It returns S exactly when d>=mu+tau. This takes
O(log(S+1)+1) additions, or fewer if k-1 is reached first. It checks
this numerical inequality; it does not certify the supplied entrance or
predecessor value.

**Space accounting.** The anchor-drop bound gives
0<=z<=floor(2(v+1)/3), and first-entry contraction gives mu=O(k).
The graph registers, tau and p have O(log(v+1)) bits; S has
O(log(v+k+1)) bits; the order and binary control have O(log k) bits.
Since v<=mP_k=O(mk^2), this constant-size collection gives (C.9).
Lower profile values and addresses have the same bit order. Formula
(C.6) then returns Q_(k-1)(r_d) and Q_(k-2)(v-r_d). QED.

**Five-row reconstruction.** Apply this decoder to five supplied roots
N_i=F_k-v_i at the same order, retaining row indices modulo5. Put
r_i=r_d(N_i), q_i=v_i-r_i, e_(1,i)=Q_(k-1)(r_i) and
e_(2,i)=Q_(k-2)(q_i). The parent and two child parameter words are

$$
\begin{aligned}
\sigma_i&=F_{k-1}-v_{i+1}-e_{1,i}-e_{2,i},\\
\alpha_i&=F_{k-2}-r_{i+1}-e_{1,i},\\
\beta_i&=F_{k-3}-q_{i+1}-e_{2,i}.
\end{aligned} \tag{C.11}
$$

Their small gap corrections use the same working-bit order. The identity
r_(i+1)+q_(i+1)=v_(i+1) gives alpha_i+beta_i=sigma_i, so only one
child parameter word need be retained once the parent word is supplied.
A fixed five rows change the register count by a constant factor.
This reconstructs row-aligned windows; the five physical roots need not
form a single inner period-five orbit.

For v=0 or1, established anchor/predecessor identities already give
r_d=v and complementary gap0, without entrance or phase data. At fixed
m, every higher-order bounded-cap root satisfies the local width condition
once k>=K(m); the remaining orders form a finite base.

**Clock compression.** After the cycle is known, z and mu affect decoding
only through (z+mu) mod p. This correction can replace their exact fields
for decoding if entrance validity and the depth-in-cycle inequality are
certified separately. On a fixed supplied cycle, p residues give p
distinct selected gaps. Thus ceil(log_2 p) fixed-width phase bits are
necessary and sufficient for that variable-phase endpoint contract.
Scalar-output qualification may collapse this quotient, as the cap4
example above shows. The prescribed depth at one physical index is unique;
this conditional phase minimum is not a full recursive minimum.

For an actual period-five example, k16,v79,N908 has z19, mu4,
tau5, p5 and cycle-entry gap67. Since F15 mod5=0, (C.10) gives
rho=(-19-4-5) mod5=2 and selected gap66. The child indices are
(15,66) and (14,13), representing544 and364. The checker verifies
this endpoint by literal iteration. Its period-five orbit is distinct
from the five legal digit-window letters.

**Campbell comparison.** The same residue selection applies to Campbell's
certified affine orbit templates. For n>=9, d=b(n-1)>=4 and
d=n mod2 by the proved parity law. The points x_4,x_5 are already periodic,
so a two-cycle selects x_4 for even n and x_5 for odd n; a fixed point
has no phase distinction. Smaller cases are handled by the
[complete proof](../campbell/note.pdf). Campbell supplies its entrance
arithmetically; the Cloitre decoder uses certified profile/entrance data
and a Fibonacci residue. This common operation transfers, while orbit
qualification remains family-specific.

The [checker](verification/collar_check.py) compares the Floyd/modular
decoder with exact-depth trajectory evaluation on actual cap-defect<=16
roots, and checks modular arithmetic independently by matrix powering.
Huge-order arithmetic concerns only Fibonacci residues and saturation,
not evaluated C values or verified entrances at those orders.

Tables, predecessor and exterior-entrance provenance, and their verification
are supplied resources. The decoder does not construct the tables or
derive the actual entrance from local data. Its working-space bound uses
a different contract from autonomous graph recognition. Full online
evaluation, a complete minimum interface and wider-block dispersion remain
open.

### Sharing selectors at repeated physical indices

Recursive windows have an additional exact restriction that costs no new
coordinate: equal parent offsets refer to the same physical integer and must
have the same selected split. If `u_i=u_h`, then `r_i=r_h` and `q_i=q_h`.
The independent Cartesian domains used for the earlier gap theorem can
therefore be too large after descent. This restriction uses the deterministic
definition of C; it does not require an orbit-phase calculation.

Write `c_i` for the physical-index label of row i. Within one profile order
these labels can simply be the offsets u_i. Assume equal labels have the same
candidate domain R_c and lower profile H_c, and restrict words by
`r_i=r_h` whenever `c_i=c_h`. The alpha map is still

```text
alpha_i = r_(i+1) + H_(c_i)(r_i).
```

Its parameter entries also agree whenever the ordered parent-input pairs
`(c_i,c_(i+1))` agree. Store one alpha value per distinct directed pair and
recover the full word from the already supplied parent labels. This removes
duplicate parameter entries as well as duplicate selector choices; no edge
labels need to be added. A nonconstant binary five-window has at most four
such pairs, while a constant window has one. This is exact sharing, not a
claim that the remaining parameter entries are all independent or minimal.

**Shared-row gap theorem.** An alpha collision between two such words exists
if and only if there is a nonzero closed gap word d_i with:

1. Each edge `d_i -> d_(i+1)` has a witness r,s in R_(c_i) satisfying
   `s-r=d_i` and `H_(c_i)(r)-H_(c_i)(s)=d_(i+1)`.
2. Whenever `c_i=c_h`, both `d_i=d_h` and
   `d_(i+1)=d_(h+1)` hold, with indices read modulo p.

**Proof.** Subtract the alpha equations of a collision and put
`d_i=s_i-r_i`. A zero gap would propagate around the entire window, so all
gaps are nonzero. Sharing both words gives the equality of incoming gaps;
sharing their profile values gives equality of outgoing gaps. This proves
necessity. Conversely, choose one edge-witness pair for each physical label.
Both its gap and its outgoing gap are identical at every occurrence of that
label, so reuse this pair at all its rows. The two resulting words obey the
sharing restriction and have equal alpha at every row by the edge equation.
They are distinct. This proves reverse completeness. QED.

Thus the original signed-gap alphabet is sufficient: impose equality on the
gap positions for repeated rows and their successors. Independent edge
witnesses must be replaced by one witness per physical label. Keeping only
one unconstrained path per endpoint can lose this condition; the checker
retains the assignments to the equality classes while constructing paths.
The existing odd-window bound `0<|d_i|<=floor(E/2)` remains valid.

**Finite sign obstruction.** Form equality classes of row positions by merging
both i with h and i+1 with h+1 whenever `c_i=c_h`. For each row whose profile
is nondecreasing on its candidates, join its incoming and outgoing classes
by an undirected edge. If this graph is not bipartite, the shared alpha map
is injective. There are at most p vertices, hence at most five for a five-window,
with no defect-budget bound needed.

**Proof.** In a collision every class has a nonzero gap. A nondecreasing
profile makes the signs of its incoming and outgoing gaps opposite:
`d_(i+1)=H_c(r_i)-H_c(s_i)` has the opposite sign to `d_i=s_i-r_i`;
zero outgoing gaps are impossible. The gap signs would therefore give a
two-colouring of the graph. A self-loop or any odd undirected cycle
contradicts that colouring. QED.

This is a sufficient criterion, not an exact replacement for the numerical
gap relations when the sign graph is bipartite. It can prove inverse
uniqueness with only some candidate profiles nondecreasing, because sharing
identifies gap positions. Profile-domain verification and the parameter word
are still supplied context. The small qualitative graph does not give a
complete finite-state classification of C or a selected-orbit certificate.

The independent candidate count now falls from `product_i |R_(c_i)|` to
`product_c |R_c|`. Given alpha and the same supplied profile/candidate context,
the exact conditional seed budget uses the maximum fiber on this restricted
domain. Empty or singleton fibers need no inverse branch label. These are
conditional inverse statements: they do not certify that a surviving word
has the prescribed basin and phase. Sharing between different tree nodes,
including alternative Fibonacci representations of a boundary index, also
requires additional consistency; this theorem handles one aligned window.

**Two-label theorem.** For an odd cyclic window with at most two distinct
physical labels, a shared-row collision exists exactly when the sets

$$
S_c=\{s-r\ne0:r,s\in R_c,\ H_c(r)-H_c(s)=s-r\}
$$

have a common element. In particular the alpha map is injective if the
profile is nondecreasing on the candidate domain of either label. A parent
defect of zero or one supplies that monotonicity under the existing integer
defect boxes.

**Proof.** With one label all row gaps already agree. With two labels let
their shared gaps be d_a and d_b. If either label is followed by both labels,
the outgoing-gap equality forces d_a=d_b. If each label instead has a unique
successor, the cyclic word containing both labels must alternate; it would
have even length. Thus odd length again forces every gap to be the same d.
Every row then needs a self-loop edge `d -> d`, exactly the common-element
condition. The shared-row gap theorem proves sufficiency. A nondecreasing
profile cannot supply a self-loop at a nonzero gap. Finally, when
`0<=r-H_c(r)<=1`, two increasing integer candidates differ in their profile
values by at least `(s-r)-1>=0`. QED.

This removes a genuine part of the sufficient seed budget at n=196. Its
order-nine child has offsets `(16,11,11,16,11)` and defects `(4,1,1,4,1)`.
Both distinct offsets have four candidates. Independent rows would allow
`4^5=1024` words, while sharing allows only `4^2=16`. The two-label theorem
proves injectivity without enumeration because offset 11 has defect one.
Given its first-child alpha `(15,15,16,15,16)`, the reconstructed word is
`(9,8,8,9,8)`. The defect-residue rule allowed a three-bit sufficient seed
label (`E=11`, modulus 6); no seed label is needed in this shared domain.
The three distinct directed parent pairs `(16,11),(11,11),(11,16)` carry
alpha values `(15,15,16)`, which reconstruct the five entries. The supplied
parameter data shrink from five entries to three; their validity proof is
still required.

The [maintained checker](verification/selector_payload_check.py) tests all
52 equality partitions of a five-window against complete consistent alpha
fibers for small shared capped profiles. It also descends every prescribed
period-five orbit through n=4096: 147 roots give 12,208 distinct internal
contexts, of which 11,534 have repeated rows. Sharing reduces 437 raw
collision pairs to three pairs in two contexts. These are finite counts,
not a universal separation theorem.
The sign obstruction certifies 11,404 of the repeated-row contexts, including
299 with a descending candidate row, so requiring every profile restriction
to be nondecreasing would miss some certified cases. The two-label
small-defect rule applies to 2,398 contexts. Across all 12,208 internal
contexts, directed-pair sharing recovers 61,040 alpha entries from 52,479
stored entries; this counts scalar entries, not their bit cost or minimum
proof size.

For a concrete remaining collision, an order-fourteen descendant of n=2012
has offsets `(101,104,101,99,106)`. The two words

```text
(51,56,51,64,49),       (53,54,53,62,48)
```

both respect repeated rows and have alpha `(102,101,110,104,97)`. They
remain valid profile-value decompositions but neither is the actual word,
which is `(53,54,53,53,55)`. At offset 99 the only periodic candidate is 53,
so that local periodicity check excludes both. The distinction is useful:
sharing is necessary family information and gives exact inverse reductions,
while periodicity and prescribed selection still have separate roles.

### A shared parameter network and its forest basis

Sharing can be imposed between windows, rather than only between rows of
one window. The useful coordinates are absolute physical indices. Let s(N)
denote the prescribed inner endpoint used to compute C(N). At a row of an
order-j window, put `N=F_j+u_i` and `M=F_j+u_(i+1)`. Then

$$
K_{NM}:=\alpha_i+F_j=s(M)+C(s(N)). \tag{9.15}
$$

Indeed `r_i=s(N)-F_(j-1)` and
`P_(j-1)(r_i)=C(s(N))-F_(j-2)`, while the next row contributes
`r_(i+1)=s(M)-F_(j-1)`. Their sum differs from the right side of (9.15)
by F_j. Thus repeated physical edges share K even across different
Fibonacci representations. The known anchors supply the normalization;
no new carry coordinate is needed.

Fix a finite collection of labelled cyclic windows. Form a directed graph G
whose vertices are their physical indices and whose edges are their directed
row transitions. Each edge lies on a closed walk, so every weak component
is strongly connected: the closed walk returns along every edge, giving
paths in both directions along a weakly connecting chain. Supply a
nonempty candidate domain D_N for each physical index, intersecting its
physical domains across occurrences. For actual C, the canonical natural
block gives its geometric/value candidates, including the exact anchor
endpoints. The following statements concern this fixed graph and supplied
profile/domain data.

**Parameter forest theorem.** Make a bipartite graph B with a source copy
and a target copy of every vertex of G, and an edge from source N to target
M for each physical edge of G. If B has c components, all K parameters
are recoverable from a spanning forest of B. This forest has
`2|V(G)|-c` edges, the exact rank of the universal linear parameter map

```text
K_(N,M) = h_N + z_M.
```

This rank treats h and z as independent formal potentials. It is not a
lower bound for the narrower nonlinear family `h_N=C(z_N)`, nor a bit
count or a minimum full C certificate size.

**Proof.** Set one potential to zero in each bipartite component. Along
each forest edge, the known sum determines the next potential by subtraction.
Every omitted edge is then recovered as the sum of its endpoint potentials.
For example, a four-cycle imposes

```text
K_(N,M)+K_(P,L) = K_(N,L)+K_(P,M).
```

Longer bipartite cycles give the corresponding alternating sums. The kernel
of the full linear map is exactly one freedom per component: add a constant
to its source potentials and subtract that constant from its target
potentials. Its rank is therefore the vertex count minus c. Forest edges
are independent and attain that rank. Integer forest weights recover
integer potentials without division. QED.

The remaining translations have a precise meaning. Write h^0_N,z^0_N
for the potentials recovered from the forest, and b_S(N),b_T(N) for the
bipartite components containing the two copies of N. Every selector
assignment with that parameter image has the form

$$
z_N=z^0_N+\gamma_{b_T(N)},\qquad
C(z^0_N+\gamma_{b_T(N)})=h^0_N-\gamma_{b_S(N)},\qquad z_N\in D_N.
\tag{9.16}
$$

Conversely these equations reconstruct an assignment with exactly the
given edge parameters. They reduce inverse reconstruction to constrained
integer translations; they do not assume these translations are free after
the C equations are imposed.

**One seed per component.** Given the joint parameter image and one
admissible z value at one vertex of a strong component, propagate

```text
z_M = K_(N,M) - C(z_N)
```

along directed paths. Every vertex is reached. Check its domain and every
edge, including alternative paths. This reconstructs the whole component
or rejects the seed. Thus one seed per shared component suffices, even if
that component contains many windows. Its conditional minimum branch label
is determined by the complete joint fibers, not the separate local fibers.

There is also an exact reverse-complete collision test on this network.
For each source N, merge all its successors into one gap class; take the
transitive closure of these equalities. Let g(N) be the class of N, and
o(N) the common class of its successors. In a component, two assignments
with a common parameter image are distinct exactly when there are nonzero
integer class gaps d satisfying, at every N,

$$
\exists r,s\in D_N:\quad
s-r=d_{g(N)},\qquad C(r)-C(s)=d_{o(N)}. \tag{9.17}
$$

**Proof.** Subtract (9.15). A zero gap propagates forward to every vertex
of a strong component, making the assignments equal there. Otherwise all
gaps are nonzero. All successors of a source have the same outgoing gap,
giving the class constraints and (9.17). Conversely choose one witness
pair per physical N in (9.17). Every edge then has equal K in the two
assignments, and each physical index uses the same pair at all occurrences.
This proves reverse completeness. QED.

A singleton domain therefore proves joint injectivity throughout its
component: its gap is zero and propagates. The monotonicity sign obstruction
also extends to the network classes. In components not certified by either
rule, the complete finite relations in (9.17) can be tested by constraint
propagation and exhaustive branching. Removing unsupported values is safe;
branching over every remaining value preserves completeness.

**Finite joint inverse theorem.** Use the same 147 prescribed five-cycle
roots through 4096 and all their internal descendant windows as above.
Their 12,208 windows contain 1,300 physical indices and 6,514 distinct
absolute edges. The bipartite graph has 292 components, so **2,308 forest
parameters recover all 61,040 row parameters**, conditional on this supplied
layout. The actual forest is decoded independently and every recovered edge
and Fibonacci normalization is checked.

All 37 selector components have injective joint parameter maps on their
supplied independent canonical geometric/value domains. Ten are certified
by singleton domains, fourteen further components by the sign graph, and
the remaining thirteen by complete empty nonzero-gap searches. Thus this
joint inverse needs **zero branch-label bits**, for every parameter image
in this finite context. Independent seed enumeration also recovers the
actual joint assignment uniquely in each component. No periodicity
qualification is needed for this particular joint inverse theorem.

The n=2012 local collision has a short cross-window separation. Its offset-99
row has physical index N=476. Elsewhere in the supplied network, N=489 has
the singleton domain D_489={292}. The edge 489 -> 476 has K=483 and C(292)=197,
so it forces `s(476)=483-197=286`, normalized offset 53. The two local
collision words instead use offsets 64 and 62 at that row, hence physical
splits 297 and 295. They cannot share the same full parameter image. This
uses a shared parameter constraint and the supplied value domain, rather
than an extra local phase label.

The checker independently verifies forest ranks for all 512 subgraphs of a
3-by-3 bipartite graph using rational elimination. It checks network gaps
and one-seed decoding against complete Cartesian fibers in 954 small
strongly connected profile contexts, comprising 24,030 assignments. The
general forest and gap proofs are distinct from the finite C premises.

The conditioning matters. This fixes a bag of physical row labels. A
different candidate selector assignment may generate a different child
layout under descent. Neither the forest theorem nor the finite joint
inverse encodes that missing layout, its profile/domain proofs, or the
prescribed basin and phase. Even the actual stored forest is a scalar-entry
count, not a total information minimum. Campbell's proved ternary endpoint
templates provide such layouts and selections by uniform arithmetic rules;
the comparable C-family rules and the marked-leaf occupation estimate
remain open. The next target is to recover the layout arithmetically while
retaining this shared interface, rather than treating supplied labels as
free total certificate data.

### Generating the layout from a sublinear shared descent code

The fixed-layout qualification can be removed from the structural payload.
Instead of supplying the child labels, record a geometric split only at the
first visit to each physical integer. Subsequent occurrences reuse it.
This generates the layout and its values, rather than assuming them as
free inverse context. It still requires a separate proof that the recorded
endpoints obey the prescribed inner iteration.

Use the canonical block `F_j<=N<F_(j+1)`, j>=6, and put u=N-F_j. The
geometric interval for the larger child a is

$$
L_N=F_{j-1}+\max(0,u-F_{j-3}),\qquad
U_N=F_{j-1}+\min(u,F_{j-2}). \tag{9.18}
$$

For actual C, its selected endpoint belongs to this interval by the proved
intersected capture theorem. A canonical anchor has u=0 and a forced split.
Alternative closed-block representations use that same physical endpoint.

**Balanced-split lemma.** Every a in (9.18), with b=N-a, satisfies

$$
\frac N2\le a\le\frac{8N}{11},\qquad
\frac{3N}{11}\le b\le\frac N2. \tag{9.19}
$$

**Proof.** The identity `F_j+F_(j-3)=2F_(j-1)` shows L_N>=N/2, by
splitting into u<=F_(j-3) and u>=F_(j-3). Also
`F_(j-3)<=2F_(j-2)/3` for j>=6: equivalently
`F_(j-3)<=2F_(j-4)`, which follows from the Fibonacci recursion.
Thus `F_j<=8F_(j-2)/3`. If u<=F_(j-2), then b>=F_(j-2) and
`N<=11F_(j-2)/3`. If u>=F_(j-2), then b>=u and `N<=11u/3`.
These give b>=3N/11 and a<=8N/11. QED.

Stop value descent at N<=8, using the fixed table
`C(1),...,C(8)=(1,1,2,3,3,4,5,5)`. Consider any finite rooted forest
obeying (9.18), with a single split shared at every repeated physical N.
Let R be the sum of its **distinct supplied root indices**, and let D be
the number of distinct reached internal indices N>=9.

**Shared-descent size theorem.** For every integer B>=8,

$$
D\le B-8+\left\lfloor\frac{11R}{3B}\right\rfloor. \tag{9.20}
$$

In particular `B=max(8,ceil(sqrt(11R/3)))` gives D=O(sqrt(R)).

**Proof.** Unfold the shared forest, keeping only one copy of each supplied
root, and cut it whenever a node first becomes at most B. Every cut leaf
under a larger root is greater than 3B/11 by (9.19). Child sizes sum to
their parent, so the number of these cut leaves is less than 11R/(3B).
The number of occurrence nodes greater than B is at most the number of
cut leaves, since each cut tree is a full binary tree. This bounds the
number of distinct large indices by floor(11R/(3B)). Small internal
indices lie in the integer set {9,...,B}, of size B-8. Add the bounds.
QED.

This argument uses global sharing of physical integers, not a uniform
defect bound. All branches also have logarithmic depth because their sizes
contract by at most 8/11 at each step.

**Generative code theorem.** Supply the root indices and their row order.
Visit roots in that order, descending the smaller child first. At the
first encounter with N>=9, write the ordinal of its split in (9.18),
using `ceil(log_2(U_N-L_N+1))` bits; a forced split writes none. Reuse
the cached split at subsequent encounters. The decoder performs exactly
this traversal, discovering the child indices from each new ordinal.
It computes values bottom-up by `V(N)=V(a)+V(N-a)`, using only the table
through eight. No child addresses, lower profile table, alpha words or
parameter graph are additional input.

For fixed roots, the unqualified code is a bijection with the reachable
shared geometric split dictionaries. It is prefix-free: once a bit prefix
determines all traversals and reaches their end, no additional choice is
left to read. Out-of-range ordinals, premature ends and extra bits are
rejected. The code body has at most

$$
D\lceil\log_2 N_{\max}\rceil
=O(\sqrt R\log N_{\max}) \tag{9.21}
$$

bits, including the generated layout and its numeric chosen endpoints.
For a five-window plus its outer index n, R<=6n. Its root metadata have
O(log n) size under the existing one-scale payload, so the total structural
representation has an O(sqrt(n) log n) upper bound. This is a sufficient
representation bound, not a minimum bit count or a bound on the complete
selected-validity proof.

If the input already specifies an outer cycle, the outer endpoint can
instead be recorded as an ordinal in that cycle. After decoding, check
the cycle transitions using the generated values and check that the outer
endpoint belongs to it. This qualification narrows the structural class
and does not certify the cycle's prescribed basin or the exact selected
phase. The body-length metadata used by the byte-packed evidence adds
only O(log n) bits; the reported body lengths exclude root headers and
optional evidence hashes.

The seven terminal histograms are also computable on the shared structure.
Cache them by `(profile order, physical index)`, adding the two child
histograms at each internal node. A physical index has at most two
representations in the closed natural blocks, so there are at most
`2(D+6)` such cache nodes. Their marked counts give the exact profile
defects as before. Large occupation counts need not require enumerating
all their repeated terminal occurrences.

The earlier Theta(F_j) lower capacity bound concerned arbitrary geometric
trees with independently positioned leaves. The present upper bound is
for the smaller globally shared class containing actual C descents. Many
arbitrary leaf layouts do not give the same split and value at repeated
physical indices. Thus the two bounds have different domains; the earlier
geometric lower bound does not apply to this generative code.

**Checked examples.** At n=196, the five cycle points
`(115,120,116,117,118)` have a 105-bit body and 35 distinct internal indices.
Add the outer root 196 and record its endpoint in the supplied five-cycle:
the body has **112 bits**, with 37 internal indices. The decoder recovers
the cycle-point values `(76,80,79,78,81)`, selected outer split 118 and
C(196)=134. The root cycle is checked from these generated values. No
C table beyond the first eight terms is supplied to the decoder.

The same 147-root family through 4096 has 882 supplied row/outer root
occurrences, representing 689 distinct roots. Its **9,427-bit body** visits
1,471 distinct internal indices and generates the earlier 12,208 internal
windows, 6,514 absolute edges and 2,308-entry parameter forest. Those
parameters are derived outputs here. The compact evidence contains the
one-scale root-cycle header and the actual packed body; `replay_descent_packet`
decodes that saved packet without generating a C prefix.

At the already checked Fibonacci knees:

| Root N | Distinct internal indices | Body bits | Marked-leaf count |
|---:|---:|---:|---:|
| 24,476 | 233 | 1,228 | 1,597 |
| 39,603 | 287 | 1,558 | 2,546 |
| 64,079 | 311 | 1,765 | 4,166 |
| 103,682 | 424 | 2,577 | 6,870 |

The linearly growing defects proved above are compatible with this
sublinear structural replay: repeated subtrees carry occupation multiplicity.
These numerical code sizes are examples, not optimality claims or an
empirical replacement for the general bound.

The checker independently enumerates 55,408 complete shared layouts over
25 small root sets, including repeated five-row roots. Every bitstream
recovers its dictionary, agrees with literal expanded value descent and
reconstructs the boundary-alias histograms. The streams are prefix-free
and reject truncated or appended data; 905,301 histogram cache nodes are
checked. Actual saved packets independently recover the values and splits
used to produce them, including all four knees in the existing prefix.

**Selected-validity boundary.** Even a perfectly shared code with an actual
cycle and basin can select the wrong phase. At N=11 the valid geometric
body `01` records split 7 and computes V(11)=C(7)+C(4)=8. But the actual
orbit from 10 reaches cycle `(6,7)` after three steps, and depth C(10)=7
selects 6, giving C(11)=C(6)+C(5)=7. Split 7 is periodic and lies in that
same prescribed basin. With the cycle supplied as root data, its qualified
one-bit body `1` also passes the cycle checks and gives eight. The remaining
distinction is the phase.

A verifier that insists on proving the exact depth at every point from
another pointwise predecessor recurrence, using only the base table through
eight, must certify every index 9,...,N: depth at N requires C(N-1), and
that dependency repeats. This observation concerns that verification
contract, not all possible proofs. The exact collar theorem already avoids
depth values when the output is phase independent. Short complete
certificates therefore need arithmetic phase rules, value-equivalence
arguments or proved profile ranges, as Campbell's ternary templates supply.
The generative code removes free child-layout and value-table inputs from
the structural representation; the full minimum proof interface and the
occupation estimate for convergence remain open.

### A conserved budget for multiscale inverse labels

Defect conservation gives more than termination. Consider the selected
recursive tree of an odd-length root window at profile order j, and let
E be its total profile defect. At every node v, write E_v for that node's
total defect. By (9.6), the two children have nonnegative costs with
`E_left+E_right=E_v`. Hence any disjoint frontier has total cost at most E.

At an internal node, the first-child defects lie in the parent row boxes:
`0<=r_i-P_(h-1)(r_i)<=e_i`. Given its alpha word and candidate/profile
context, the defect-seed theorem therefore needs at most

```text
b_v = ceil(log_2(floor(E_v/2)+1))
```

additional bits to recover the first child. The second child is then the
coordinatewise difference from the known parent word, so it needs no second
seed label. When E_v<=1, b_v=0 and every alpha fiber is already a singleton.

Put D_v=floor(E_v/2). For D_v>=1, `D_v+1<=2^D_v`, so b_v<=D_v; this
also holds at zero. On every frontier of internal nodes,

$$
\sum_v b_v\le\sum_v\lfloor E_v/2\rfloor\le\lfloor E/2\rfloor. \tag{9.7}
$$

The number of nodes that could require a nonzero inverse label is likewise
at most floor(E/2) on any frontier. Since there are at most j-5 internal
depth levels, the entire tree needs at most

$$
(j-5)\lfloor E/2\rfloor \tag{9.8}
$$

conditional seed-label bits. The same bound counts potentially ambiguous
internal nodes. Its proof does not require enumerating their alpha fibers.
The signed-gap capacity also satisfies
`sum_v 2*floor(E_v/2)<=2*floor(E/2)` on each frontier, per row layer.
Thus a per-root gap alphabet and inverse-label budget do not proliferate
with the number of descendants, even though the raw tree can branch.

These are bounds on **residual inverse labels after the local parameter words
and contexts are supplied**. They exclude the cost of those parameter words,
the profile/qualification certificates and the prescribed basin/phase proofs.
They do not bound the whole certificate, and E need not be uniform across
roots or Fibonacci orders. In particular, zero inverse-label cost does not
make an unspecified child parameter word or its selected validity free.

The recursive audit checks the bound at every depth and decodes each odd
internal node with its adaptive residue, after the geometric candidate
restriction (9.5). This makes the multiscale inverse budget independently
testable alongside the row-aligned window representation.

### Seven terminal symbols and the full geometric selector code

The tree has a fixed shape: an order-j node has children of orders j-1 and
j-2, stopping at four and five. For j>=6 its leaf counts are

```text
a=F_(j-5) leaves of order 4,    b=F_(j-4) leaves of order 5.
```

There are a+b=F_(j-3) leaves per row. At order four the offset v is 0,1,2
and `P_4(v)=(0,1,1)`; at order five v is 0,1,2,3 and
`P_5(v)=(0,1,2,2)`. These are just the defining values through eight.
Consequently the leaf alphabet consists of seven pairs `(height,v)`, and
the leaf defect is one exactly at `(4,2)` or `(5,3)`, zero otherwise.

**Terminal-code theorem.** In the actual selected tree of `F_j+u`, the
sum of leaf offsets is u, and

$$
\lambda_j(u):=u-P_j(u)
=\#\{\text{leaves labelled }(4,2)\text{ or }(5,3)\}. \tag{9.9}
$$

This follows by induction from offset and defect additivity. To recover
the entire arithmetic selector tree, retain the positions of the terminal
letters in a fixed traversal, not just their histogram. For definiteness
visit the j-2 child before the j-1 child. Every internal offset is the sum
over its descendant leaf offsets; its profile is offset minus the number
of marked descendants. Thus the positioned leaf word recovers all splits
and, for aligned window rows, every alpha/beta parameter word.

There is an exact reverse statement for the **geometric** code class. Assign
any permitted offset to each leaf of the fixed shape and sum upward. Each
subtree's maximum offset is its natural-block bound F_(h-1). The child sums
therefore satisfy (9.5) at every internal node. Conversely, every tree obeying
this geometry gives one such positioned leaf word. This is a bijection.
The class does not yet impose equality of profile values at repeated physical
indices or the actual prescribed-orbit choice. Actual C trees satisfy those
additional conditions; the geometric code alone is not their proof.

Let E be the number of marked leaves. The exact number of geometric codes
with given j,u,E is

$$
N_j(u,E)=[z^u w^E]
(1+z+z^2w)^a(1+z+z^2+z^3w)^b. \tag{9.10}
$$

Hence the full geometric tree, including its internal parameter data, has
conditional fixed-width capacity `ceil(log_2 N_j(u,E))` bits. Ordering the
words lexicographically gives a lossless ordinal code; suffix coefficient
counts decode it without enumerating all words. For a p-row window with the
root offsets and defects fixed, the geometric code count is the product of
the p coefficients. This is the exact minimum for the stated geometric class,
not a minimum for the narrower C family after its profile and phase constraints.

This full arithmetic capacity has a sharp worst-case growth order. Put
L=a+b=F_(j-3). Every leaf has at most four choices, so 2L bits always
suffice for one geometric row. Even with E=0, choose only offsets zero and
one and set u=floor(L/2). There are at least `binomial(L,floor(L/2))`
codes. The largest binomial coefficient is at least `2^L/(L+1)`, so at
least `L-log_2(L+1)` bits are needed in this context. Thus the worst-case
geometric selector capacity is Theta(F_j), including contexts whose
conditional residual seed budget is zero. Even a fixed histogram can retain
this growth: choose half of each leaf type to have offset one; positional
multiplicity is at least `2^L/((a+1)*(b+1))`. These are geometric-class
lower bounds, not lower bounds for the actual selected C family. A short
family certificate must restrict or describe positions arithmetically.

The coefficient is positive exactly for the consecutive integer interval

$$
\max(0,u-F_{j-2})\le E\le
\min\left(F_{j-3},\left\lfloor\frac u2\right\rfloor,
\left\lfloor\frac{u+a}3\right\rfloor\right). \tag{9.11}
$$

**Proof of support.** Write x,y for marked order-four/five leaves, so
x+y=E. Their minimum offset cost is 2E+y. The unmarked leaves supply every
integer from zero to `(a-x)+2(b-y)`. Thus the maximum total offset is
`a+2b+E=F_(j-2)+E`, independent of x,y. Minimize y subject to the available
leaf counts: `y=max(0,E-a)`. Feasibility is exactly
`0<=E<=a+b` and `2E+max(0,E-a)<=u<=F_(j-2)+E`, which rearranges to
(9.11). The converse assigns the remaining offset among the unmarked leaves
and uses the reverse geometric construction. QED.

The seven histogram counts themselves have only three free coordinates once
j,u,E are known. In the order `(4,0),(4,1),(4,2),(5,0),(5,1),(5,2),(5,3)`,
write them as `(h0,h1,h2,k0,k1,k2,k3)`. Choosing y=k3,z=k2,v=k1 gives

```text
h2=E-y,       h1=u-2E-y-v-2z,
h0=a-u+E+2y+v+2z,       k0=b-y-z-v.
```

Keep choices for which every count is nonnegative. The four independent
constraints are the two leaf-type totals, total offset and marked count.
For one histogram the positional multiplicity is
`a!/(h0!h1!h2!) * b!/(k0!k1!k2!k3!)`. Summing these multiplicities gives
(9.10); a histogram still omits the positional ordinal.

A small actual C example separates value data from selected-tree data.
At n=15=F_7+2, leaf order is `(5,4,5)`. The words `(2,0,0)` and `(0,0,2)`
have the same histogram and zero defect. They give root splits 8 and 10;
all their lower internal splits are the actual selected ones and their
arithmetic profiles agree with C. Both root splits lie on the cycle `[8,10]`
and both give `C(15)=10`. The prescribed depth is 9 and entry time is 3,
so the actual split is 8. Their first child parameters are 0 and 4. Thus
even zero residual inverse bits do not make an unspecified parameter word
free; the histogram determines the value here but not the prescribed split.

The checker compares coefficient counts, ordinal encoding and reverse tree
reconstruction with all 28,284 geometric words through order nine, and
checks support through order thirteen. It encodes/decodes the 65 actual
public five-window rows, recovering all 2,815 internal split rows. At n=196
the five geometric code coefficients have joint capacity 158 bits, conditional
on the root offsets and defects. This includes internal arithmetic parameter
data, whereas the earlier 29-bit sufficient seed budget assumes those local
parameter words and contexts are supplied. Neither figure measures selected
validity proof costs or the minimum for C's more restricted family.

### Growing actual defects and the remaining occupation problem

The root defect budget is genuinely unbounded in C. At the Fibonacci knee
`n=F_j+F_(j-2)`, the baseline is F_j. The already proved envelope
`C(n)<=2n/3` for n>=16384 gives

$$
\lambda_j(F_{j-2})=F_j-C(F_j+F_{j-2})
\ge\left\lceil\frac{F_{j-3}}3\right\rceil. \tag{9.12}
$$

It grows linearly in F_j. The sharper envelope H=8900/13459 gives, whenever
the knee is at least 349525, the stronger bound
`ceil((4559*F_j-8900*F_(j-2))/13459)`. These are universal consequences of
the existing certified envelopes, not extrapolations of the leaf census.

There is also a cycle-wide statement. Put `n=2b`, `b=F_(k-1)>=16384`,
and `h=F_(k-3)`. Every inner cycle lies in `[b,b+h]`. For a period-p cycle
with vertices x_i, sum `C(x_i)=n-x_(i+1)` and use C(x_i)<=2x_i/3:
`sum(x_i)>=3pn/5`. Its normalized total defect is
`E=2*sum(x_i-b)-p*h`. Therefore every such cycle satisfies

$$
\frac Ep\ge\frac{2b}5-h. \tag{9.13}
$$

The right side divided by b tends to `2/5-1/phi^2>0`. Thus the mean cycle
defect is also forced to grow linearly at these centers, regardless of its
period. This does not assert that proper five-cycles occur at infinitely many
centers or that inverse fiber sizes grow. It does show that the E-based
sufficient label/alphabet budgets cannot be uniformly bounded on the full
recursive class. Family-specific arithmetic compression can still be smaller.

Geometry and terminal consistency do not select the correct occupation.
The existing upper-cap function U has natural profiles
`Q_j(u)=min(u,F_(j-2))`, including the same seven terminal symbols. It has
a globally consistent geometric split rule

```text
r=min(F_(j-2),max(0,u-F_(j-4))),       q=u-r.
```

These splits obey (9.5) and
`Q_(j-1)(r)+Q_(j-2)(q)=Q_j(u)`. To check the identity, below
`u=F_(j-2)` both child offsets are at or below their linear/plateau thresholds;
above it both child profiles are on their plateaus, whose heights add to
F_(j-2). Endpoint cases are included. Thus this family realizes the minimum
marked count in (9.11), has the Fibonacci identities and obeys G<=U.
But it fails the prescribed nested recurrence already at n=11: its formula
gives U(11)=8, while depth U(10)=7 selects 6 and gives U(6)+U(5)=7.
Its block maximum ratio tends to `(5+sqrt(5))/10`, rather than 1/phi.
This is a counterexample to deriving the full limit from geometric closure
and terminal data alone, not a counterexample to convergence of C.

For actual C let M_j(u) be its marked-leaf count from (9.9). The Fibonacci
identity `F_(j-1)-alpha*F_j=(-alpha)^j` gives exactly

$$
C(F_j+u)-\alpha(F_j+u)
=(1-\alpha)u-M_j(u)+(-\alpha)^j. \tag{9.14}
$$

Consequently full ratio convergence is equivalent to the uniform occupation
law `sup_u |M_j(u)-(1-alpha)*u|/F_j -> 0` over the natural block. Since
C>=G already supplies the matching one-sided estimate up to a bounded
rounding term, the unresolved direction is a sufficiently large marked
count throughout the arch. A decay rate would require a quantitative bound
on that occupation deficit. The positioned terminal code now identifies
precisely where the missing selector and phase restrictions must act; seven
symbols alone do not constitute a uniform finite-state classification.

### Actual defect allocation and phase information

Parent cap conservation does not by itself specify the two child caps.
There is, however, a sharper supplied-profile interface: one child-cap
allocation determines the selected periodic point, with no independent
cycle, entrance, depth-phase or inverse label.

**Allocation-seed theorem.** Let K>=22, N=F_K-v, 0<=v<=F_(K-2),
and supply the actual parent cap e=Q_K(v)>=4 and lower profiles on
the captured child blocks. Let b be the actual second-child cap. Then

$$
0\le b\le e-4,\qquad r_0=v-(e-b). \tag{D.1}
$$

The seed r_0 is on the actual selected gap cycle. Iterating
r->v-Q_(K-1)(r) from this seed to its first return, the last gap r
is the selected one. Its children and readouts are

$$
a=F_{K-1}-r,\quad N-a=F_{K-2}-(v-r),\quad
C(a)=F_{K-2}-(e-b),\quad C(N-a)=F_{K-3}-b. \tag{D.2}
$$

With b supplied, the iteration needs at most v+1 profile queries and
O(log(v+2)) working bits for the current gap and counter. Profile storage,
context integers and certification of the supplied parent cap/allocation
remain separate costs.

**Proof.** The [cap4 tail argument](exact-collars.md#two-higher-cap-levels-and-their-phase-selected-closure)
applies to every e>=4. Put W=Z_(K-1). The only case v=W+4 with
e>=4 is the excluded cap3 frontier, where e=4 and the selected first
cap is4. Otherwise v>=W+5 and every captured cycle has first-child
cap at least4. Hence its selected first cap is e-b>=4, proving the
range in(D.1). The selected gap r has successor v-Q_(K-1)(r)=r_0.
Its prescribed depth is periodic by the foundations theorem, so r_0 is
periodic too. A cycle has one periodic predecessor of a given point,
which proves the decoder and(D.2). Only a gap and counter are needed
to wait for the seed's return. QED.

**Exact allocation alphabet in this contract.** Consider all captured
periodic phases whose two scalar readouts sum to the supplied C(N).
Their possible second caps form a set B(N,e). Each b in this set
corresponds to exactly one periodic phase, even across different cycles:
its first cap is e-b and its successor is the fixed seed in(D.1).
Two cycles cannot share that seed, and one cycle cannot have two periodic
predecessors of it. Conversely each such phase gives its second cap.
Thus allocation labels are a bijective code for these scalar-valid phases.

Consequently M=|B(N,e)|<=e-3. A fixed-length code distinguishing these
M options has the exact minimum ceil(log2 M) bits. If a particular cycle
of period p is supplied, restrict B to that cycle and M<=min(p,e-3).
The latter bound applies to a five-window with p=5. This is a code for
the declared periodic-phase options; it is not a lower bound on independent
inputs needed to evaluate the actual recurrence. An arithmetic theorem or
the prescribed depth can derive the selected allocation.

Given the two lower profiles, B can be constructed: for each0<=b<=e-4,
test whether its seed returns in the captured interval, take its periodic
predecessor r, and check Q_(K-2)(v-r)=b. The first profile then already
has Q_(K-1)(r)=e-b. This neither assumes a basin nor leaves an inverse
branch label, but it still needs a rule to choose among multiple allocations.
At e=4, b=0 is forced, recovering the cap4 zero-label decoder.

**A genuine five-cycle ambiguity.** At N=310, K=14 and v=67, the
actual cycle is(183,190,182,187,185). The parent value209 has cap24.
Exactly two phases on this cycle preserve209:

| First child | Second child | Scalar child values | Child caps |
|---|---|---|---|
|182|128|123,86|21,3|
|185|125|127,82|17,7|

Thus this supplied-cycle allocation alphabet has two symbols and its
phase code needs one bit. The prescribed depth206 selects182.
The K>=22 tail bound is not asserted at this small example; the periodic
seed uniqueness argument itself holds whenever the cap labels and captured
geometry are supplied. It gives the selected phase from second cap3,
and the other scalar-valid phase from second cap7.

At the high-order root N=17629=F_22-82, the prescribed depth10939
selects10875, with complement6754 and child caps(6,1), totaling7.
The same actual cycle(10870,10871,10875) also has scalar-valid phase10870,
whose child caps are(7,0). This shows that a parent scalar and a qualified
cycle can leave the allocation unresolved even at K>=22. Both witnesses
are independently checked by full-orbit/Brent evaluation and literal depth.
They do not prove that every allocation in(D.1) occurs, or that cap7 is
the first branching level in the infinite sequence.

The cap2/3 direct decoder and cap4 periodic seed give actual qualified
five-row closure with derived labels. Above cap4, the new interface isolates
one allocation parameter in place of separate cycle and phase data, conditional
on supplied scalar/profile context. Deriving that parameter and the profiles
in wide blocks remains part of the full minimum-interface problem.

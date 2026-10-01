# Exact Fibonacci collars and selected phases

[Project home](../README.md) · [Research map](README.md#technical-research-map)

This note proves exact values and cycle selection near Fibonacci indices,
including eventual linearity at every fixed positive offset. It builds on the
[global golden theorem](golden-proof.md) and [orbit capture](fibonacci-collars.md).
Finite seed premises are identified in each theorem. Global convergence remains open.

## Contents

- [6. Exact collars propagate from two seeds](#6-exact-collars-propagate-from-two-seeds)
- [A single negative collar seed is sufficient](#a-single-negative-collar-seed-is-sufficient)
- [Large natural-block defects with no residual selector labels](#large-natural-block-defects-with-no-residual-selector-labels)
- [The first negative boundary has an exact two-state interface](#the-first-negative-boundary-has-an-exact-two-state-interface)
- [Adjacent-gap parity closure and the entrance condition](#adjacent-gap-parity-closure-and-the-entrance-condition)
- [The prescribed basin and phase in a positive collar](#the-prescribed-basin-and-phase-in-a-positive-collar)
- [A saturated lower barrier and the exclusion of nearby proper cycles](#a-saturated-lower-barrier-and-the-exclusion-of-nearby-proper-cycles)
- [Every fixed positive offset eventually becomes linear](#every-fixed-positive-offset-eventually-becomes-linear)
- [Five legal bit patterns and eventual vanishing of a local interaction](#five-legal-bit-patterns-and-eventual-vanishing-of-a-local-interaction)

## 6. Exact collars propagate from two seeds

**Theorem.** Let K>=6 and let L,R be nonnegative integers with
L+R<F_(K-2). Suppose both orders j=K,K+1 satisfy

$$
C(F_j+t)=F_{j-1}+\max(0,t)\qquad(-L\le t\le R).
$$

Then the same identities hold for every order j>=K.

**Proof.** Induct on k>=K+2, assuming the profiles at k-1 and k-2.
For n=F_k+t, the capture theorem puts its selected cycle point at

$$
a=F_{k-1}+s,\qquad
\min(0,t)\le s\le\max(0,t).
$$

The complementary argument is b=F_(k-2)+(t-s). Both offsets s and t-s
belong to [-L,R], and both have the same weak sign as t. The width restriction
ensures positive indices and keeps these lower-order collars below the current
band. Applying their proved profiles gives

$$
\begin{aligned}
C(n)&=C(a)+C(b)\\
&=F_{k-2}+F_{k-3}+\max(0,s)+\max(0,t-s)\\
&=F_{k-1}+\max(0,t).
\end{aligned}
$$

This proves the induction. The selected orbit's phase does not affect the sum.
QED.

**All-cycle classification.** Under the same hypotheses, take k>=K+1 and
write A=F_(k-1). For every -L<=t<=R:

- If t<=0, the unique cycle at n=F_k+t is the fixed point A+t.
- If t>0, the cycles are precisely the pairs
  {A+s,A+t-s} with integers 0<=s<t/2, together with the fixed point A+t/2
  when t is even.

**Proof.** Capture puts all cycles in [A+min(0,t),A+max(0,t)], and every
orbit enters it. The now-established profile at order k-1 makes T_n constant
with value A+t on the negative interval, and the reflection
T_n(A+s)=A+t-s on the positive interval. All interval points are in the actual
domain. This proves the complete classification, including every starting state.
QED.

**Certified corollary.** The two seed orders K=23 and K+1=24 satisfy this
profile with L=12 and R=32. The [checker](verification/collar_check.py)
checks all 90 seed values with independently agreeing full-orbit and Brent
prefixes. The [recorded evidence](verification/collar-check.json) lists both
relative-value arrays. Since 44<F_21=10946, the theorem proves

$$
C(F_k+t)=F_{k-1}+\max(0,t)
\qquad(k\ge23,\ -12\le t\le32).
$$

For all k>=24, every orbit in these bands therefore lands in a fixed point
or a two-cycle, with exactly the cycles classified above. The checker also
enumerates every starting state in all 45 graphs at order k=24 as independent
finite corroboration. The two seed collars are premises; that graph enumeration
is not needed for the universal proof.

This two-seed theorem alone does not prove that suitable seeds exist for every
width. The growing-positive-collar theorem below establishes their existence
for every positive width. The single-seed result below extends the certified
negative width to 17; arbitrary negative widths remain open.
These neighborhoods do not control Fibonacci-block
centers or settle full ratio convergence.

### A single negative collar seed is sufficient

**Theorem.** Let K>=6 and 0<=L<F_(K-2). Suppose just one order satisfies

$$
C(F_K-v)=F_{K-1}\qquad(0\le v\le L).
$$

Then the same identities hold at every order k>=K. For every k>=K+1
and 0<=v<=L, every orbit of T_(F_k-v) reaches the unique fixed point
F_(k-1)-v, which is also the prescribed split. No positive collar or second
negative seed is needed.

**Proof.** Assume the collar at k-1, and put
n=F_k-v, A=F_(k-1), B=F_(k-2). Capture puts every cycle in
[A-v,A], and every orbit eventually enters this interval. All its points
belong to [1,n-1] under the width hypothesis. The preceding negative collar
gives C(A-r)=B for 0<=r<=v, so throughout the captured interval,

$$
T_n(A-r)=n-B=A-v.
$$

Thus the interval maps to the single fixed point A-v. The prescribed depth
is already proved to reach a cycle, hence selects A-v. Its complement is
exactly B, and the Fibonacci identity at B gives

$$
C(n)=C(A-v)+C(B)=B+F_{k-3}=A.
$$

This propagates one order at a time and proves the all-start claim. QED.

**Certified widening.** The existing width-12 collar holds for k>=23.
Only the following five additional scalar premises are needed to widen it:

| New gap v | Seed order K | Index F_K-v | Checked value C(F_K-v) | Values valid at | Unique fixed cycles valid at |
|---:|---:|---:|---:|---|---|
| 13 | 24 | 46355 | 28657 | k>=24, 0<=v<=13 | k>=25 |
| 14 | 26 | 121379 | 75025 | k>=26, 0<=v<=14 | k>=27 |
| 15 | 27 | 196403 | 121393 | k>=27, 0<=v<=15 | k>=28 |
| 16 | 29 | 514213 | 317811 | k>=29, 0<=v<=16 | k>=30 |
| 17 | 30 | 832023 | 514229 | k>=30, 0<=v<=17 | k>=31 |

At each row, all smaller gaps at that seed order are already supplied by
the preceding row or the proved width-12 collar. The new value completes
one full seed; the theorem propagates it to every higher order.
The [checker](verification/collar_check.py) independently regenerates these
values with full-orbit and Brent evaluators through F_30+34=832074, reusing
the prefix already required by the positive-collar audit. It also records
each whole seed collar as corroboration. In particular,

$$
C(F_k-v)=F_{k-1}\qquad(k\ge30,\ 0\le v\le17).
$$

For k>=31 the exact negative split is F_(k-1)-v. Conditional on the known
order, gap, and proved collar, no residual basin, phase, or child-selector
label is needed there. This does not remove the numerical scale or the cost
of establishing the collar. Together with the existing positive result,
the value band -17<=t<=32 is exact at k>=30; its full cycle classification
holds at k>=31.

### Large natural-block defects with no residual selector labels

The negative collar also gives a concrete closed class for the
[row-indexed recursive windows](recursive-descent.md#recursive-windows-with-a-parameter-at-every-row).
It is useful to express the result in their positive natural-block coordinates.
Write n=F_(h+1)-v=F_h+u, with u=F_(h-1)-v.
If a width-L negative seed is known at order K, then for h>=K and 0<=v<=L,

$$
P_h(u)=F_{h-2},\qquad
\lambda_h(u):=u-P_h(u)=F_{h-3}-v,
$$

and the actual split offsets in the two lower natural blocks are

$$
r=F_{h-2}-v,\qquad q=F_{h-3}.
$$

Indeed the prescribed split is F_h-v and the complement is F_(h-1).
Their profile values are F_(h-3) and F_(h-4), whose sum is F_(h-2).

For any cyclic row word v_0,...,v_(m-1) in this collar, including m=5,
the parent and child parameter words are therefore

$$
A_i=F_h-v_{i+1},\qquad
\alpha_i=F_{h-1}-v_{i+1},\qquad
\beta_i=F_{h-2},\qquad \alpha_i+\beta_i=A_i.
$$

The complement child is the same Fibonacci anchor in every row; the first
child retains its gap v_i and drops the anchor order by one. Repeating the
arithmetic split closes this descent down to the verified seed order K,
where the scalar values are known. The row clock is inherited. Conditional
on h, the gap word, and this collar qualification, zero residual child-selector
or physical-orbit phase labels suffice. No parameter word has to be guessed.
Recovering the deeper selected splits inside the finite seed prefix, if those
are requested, is a separate boundary-data task.

Yet lambda_h(u)=F_(h-3)-v is unbounded with h, even for one fixed gap.
Thus a large geometric defect budget can coexist with an exact arithmetic
selector in actual C. A budget-based sufficient code must not be interpreted
as a necessary selector cost. This complements the
[Campbell scale-memory bound](../campbell/scale-memory.md): a short physical
cycle can still require growing autonomous encoding memory. Both statements
keep the scale and supplied context separate from the conditional selector
payload. This collar class does not certify selectors in wide arch centers.

### The first negative boundary has an exact two-state interface

Define the nonnegative negative-side defect

$$
Q_h(r)=F_{h-1}-C(F_h-r)\qquad(0\le r<F_h).
$$

Nonnegativity follows from the nondecreasing upper cap. The proved
[anchor-drop bound](fibonacci-collars.md#quantitative-capture-and-a-short-exterior-certificate)
gives Q_h(r)<=floor(2r/3) for h>=5.

**Boundary theorem.** Let j>=7 and 2<=v<F_(j-3). Suppose only that the
preceding order is flat at every smaller gap:

$$
Q_{j-1}(r)=0\qquad(0\le r<v).
$$

Put A=F_(j-1), B=F_(j-2),
p=Q_(j-1)(v), and q=Q_(j-2)(p). Then

$$
0\le p\le\lfloor2v/3\rfloor<v,
\qquad 0\le q\le\lfloor2p/3\rfloor.
$$

If p=0, all orbits at n=F_j-v reach the fixed point A-v and Q_j(v)=0.
If p>0, all orbits reach the unique two-cycle

$$
\{A-v,\ A-v+p\}.
$$

The two current scalar outputs, expressed as defects, are exactly

$$
Q_j(v)=
\begin{cases}
p,&\text{selected split }A-v,\\
q,&\text{selected split }A-v+p.
\end{cases}
$$

Thus one phase copies the preceding defect at gap v; the other transfers
to gap p at the order two steps below, with strictly smaller defect q<p.
If that lower gap is flat, q=0 and the rule is copy or erase. Erasure cannot
be followed by reappearance: the smaller parent gaps are already flat by
single-seed propagation from order j-1, so erasure completes a full width-v
seed. No second basin label is needed in either case.

**Proof.** In captured gap coordinates, x=A-r with 0<=r<=v, the inner map is

$$
r\longmapsto v-Q_{j-1}(r)=
\begin{cases}
v,&r<v,\\
v-p,&r=v.
\end{cases}
$$

This proves the fixed-point/two-cycle classification. If the selected gap
is v, the first child contributes defect p and the complementary child is
the exact anchor B, giving Q_j(v)=p. If it is v-p, the first child has
smaller gap and is flat, while the complement is B-p and contributes q.
The anchor-drop bound at orders j-1 and j-2 proves the two displayed
inequalities, including q<p when p>0. QED.

**Absorbing-tail corollary.** Suppose K>=6, 2<=v<F_(K-2), and the entire
width-(v-1) negative collar is flat at order K. At the first update K+1,
the gap-v defect either copies Q_K(v) or transfers to a strictly smaller
defect. Thereafter, for every h>=K+2,

$$
Q_h(v)\in\{Q_{h-1}(v),0\}.
$$

Consequently the tail from K+1 either keeps one positive integer defect
forever or copies that defect until a single permanent erasure. There can
be no repeated contraction or reawakening after the first update.

**Proof.** The width-(v-1) seed propagates to all orders h>=K. In the boundary
formula for h>=K+2, p=Q_(h-1)(v)<v and the order h-2 is already flat at
that smaller gap p, so q=Q_(h-2)(p)=0. The formula gives the displayed rule.
If the defect becomes zero, it completes a width-v seed and stays zero.
QED. The corollary does not bound the erasure order or rule out perpetual
copying in the actual recurrence.

**Prescribed phase without a full transient counter.** Let tau be the first
entrance time into [A-v,A], d=C(F_j-v-1), and define the entrance flag

$$
\varepsilon=\mathbf1\{x_\tau>A-v\}.
$$

Then tau is even. When p>0, the actual readout is

$$
Q_j(v)=
\begin{cases}
p,&d\bmod2=\varepsilon,\\
q,&d\bmod2\ne\varepsilon.
\end{cases}
$$

**Proof.** Above A, the golden bound gives C(x)>=G(A+1)=B+1, so the
image is strictly below A-v. Below A-v, the cap gives C(x)<=B, so the
image is at least A-v. Exterior sides alternate until capture; the start
n-1 is above A, so the first entrance is at an even time. If the entrance
is A-v, the gap-v phase occurs at even clocks. Any other entrance has
gap r<v and maps to gap v one step later, so gap v occurs at odd clocks.
The prescribed depth reaches the cycle, making these parity statements
applicable even if the first captured point is transient. QED.

The following actual witnesses are independently replayed with exactly d
literal iterations; their alternate outputs are computed at the other
point of the same unique two-cycle:

| j | v | n | p | q | Entrance flag | Depth d | Actual C(n) | Other phase's output |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 24 | 13 | 46355 | 1 | 0 | 1 | 28656 | 28657 | 28656 |
| 25 | 14 | 75011 | 1 | 0 | 1 | 46367 | 46367 | 46368 |
| 26 | 14 | 121379 | 1 | 0 | 1 | 75024 | 75025 | 75024 |

**Conditional minimum.** With j,v,p,q and the flat-profile premise supplied,
p>0 has exactly two current-value classes, two continued-output states, and
two index-output states: the two distinct values alternate on the cycle.
One combined selected-phase bit is sufficient and necessary for an unspecified
cycle phase. For p=0 all three counts are one. If depth parity and a certified
entrance flag are supplied instead, the combined bit is derived from them;
it is not an additional independent stored label. A path certificate can
establish the flag within the proved logarithmic capture bound. Its profile
queries and validation cost are separate resources.

This does not prove eventual extinction at every negative gap. Unlike the
positive boundary, the exact depth reads the larger gap v+1:
d=A-Q_j(v+1). Its parity and the entrance flag still require actual sequence
information beyond the flat smaller-gap premise. Finite checks find p=1,
q=0, and entrance flag 1 in the 24 nonzero boundary contexts through order30;
these are observations, not uniform laws. The complete minimum interface
away from qualified collars, uniform dispersion, and full convergence remain
open. [Recorded evidence](verification/collar-check.json) separates these
finite checks from the general propagation and boundary proofs.

### Adjacent-gap parity closure and the entrance condition

The larger-gap depth read can be closed as a finite **parity envelope**.
This envelope allows every periodic phase at the adjacent physical index;
it does not assume that all those choices are realized by actual C.
It gives a precise sufficient entrance condition for negative-collar widening.

**Adjacent-gap theorem.** Let j>=7 and 3<=v with w=v+1<F_(j-3).
At n=F_j-w, let the preceding profile Q_(j-1) be flat at gaps r<v,
with defect p>0 at v and defect R at w. Suppose Q_(j-2) is flat at
all gaps below v. The anchor-drop bounds give

$$
p\le\lfloor2v/3\rfloor<v,\qquad
0\le R\le\lfloor2(v+1)/3\rfloor<v.
$$

In gap coordinates the adjacent inner map is

$$
r\longmapsto
\begin{cases}
w,&r<v,\\
w-p,&r=v,\\
w-R,&r=w.
\end{cases}
$$

Its complete cycle and scalar-readout classification is:

| p | R | Cycles in gap coordinates | Possible next adjacent defect |
|---|---|---|---|
| 1 | 0 | Fixed points v and w | 0 or 1 |
| 1 | 1 | Fixed point v | 1 |
| 1 | >1 | Fixed point v; two-cycle {w,w-R} | 0, 1, or R |
| >1 | 0 | Fixed point w | 0 |
| >1 | 1 | Three-cycle {w,v,w-p} | 0, 1, or p |
| >1 | >1 | Two-cycle {w,w-R} | 0 or R |

**Proof.** Every gap below v maps to w. The two exceptional images therefore
give exactly the displayed cycles, including every starting state. All their
complementary child gaps are among 0,1,p,R and are below v, so the lower
child contributes zero defect. The scalar readout is just the preceding
profile's defect at the selected periodic gap, giving the last column. QED.

**Minimum observable states for this envelope.** Fix p and the allowed
range 0<=R<=floor(2(v+1)/3). Observe current parity and all possible future
parity words under the last column, without supplying the Fibonacci clock.
For p=1 and v>=4, the exact equivalence classes are

$$
\text{even }R,\qquad R=1,\qquad\text{odd }R\ge3.
$$

Their class transitions are, respectively,

```text
even -> even or one
one -> one
other odd -> other odd, even, or one.
```

The even class includes zero. Every permitted class transition lifts from
every concrete member of its source class, so this quotient is reverse
complete for parity traces. The two odd classes have the same current
parity but differ after one step: an odd R>=3 can produce even parity,
whereas R=1 cannot. Even and odd classes differ immediately. Thus three
observable states are sufficient and necessary. When v=3 there is no
admissible odd R>=3, leaving two states.

For p>1, all even R are equivalent and all odd R are equivalent. Their
transitions are `even -> even` and `odd -> odd or even`, with every edge
lifting from every source member, including R=1. The distinct current
parities prove the exact two-state minimum. These minima concern this
transition envelope, not the smaller, still unclassified set of actual-C
histories or the exact numerical adjacent defect.

**Clock obstruction.** Suppose a width-(v-1) negative seed is known at
order K>=6, v<F_(K-2). While the gap-v defect has not erased after K+1,
the absorbing-tail result gives one constant amplitude p. Write
R_h=Q_h(v+1). At every h>=K+2 the adjacent-gap theorem applies, since
the smaller lower gaps have propagated from the seed. If the entrance
flag for the gap-v orbit is 1, persistence requires its copy phase and
therefore an odd depth. Since d=F_(h-1)-R_h, this forces

$$
R_h\bmod2=
\begin{cases}
1,&h\equiv1\pmod3,\\
0,&h\equiv0\text{ or }2\pmod3.
\end{cases}
$$

The envelope cannot support more than four consecutive values with these
parities when p=1, or more than three when p>1.

**Proof.** For p=1, an even R may remain even or move to the absorbing
state R=1. An odd R>=3 may remain odd, move to an even value, or move to1.
The longest clock-compatible history starts at residue1 with odd R>=3,
moves to an even value at residue2, stays even at residue0, then moves
to1 at residue1. The next required even parity is impossible. Starting
in either other class, or at another clock residue, shortens this bound.
The concrete envelope path `3,0,0,1` shows the four-value bound is sharp
when v>=4. For p>1, once R becomes even it stays even. There can be at
most one odd segment followed by an even segment; the clock allows at
most three successive values. The path `1,0,0` at residues1,2,0 attains
that bound. These are envelope witnesses, not actual-C orbit claims. QED.

With the clock supplied and persistence under consideration, parity is
already fixed. Only p=1 at residue1 may need the additional Boolean
qualification `R=1` to distinguish future envelope continuations. The two
odd classes have different next-step possibilities, so that Boolean cannot
be omitted there when both classes are allowed. For p>1 no extra amplitude
class is needed for this parity-survival diagnostic. This is separate from
the combined phase bit needed for the current scalar readout.

**Conditional widening theorem.** Under the seed and domain conditions above,
suppose the entrance flag is 1 whenever the gap-v boundary has a nonzero
preceding defect, for all orders h>=K+2. Then Q_h(v)=0 for every h>=K+6.
If the amplitude after the first update is greater than1, K+5 suffices.

**Proof.** If the defect survives through K+6, it has one positive amplitude
at all five orders K+2,...,K+6. All five entrance flags are1, so the
clock obstruction forbids their five successive adjacent parities. Erasure
must occur by K+6, and the resulting complete width-v seed is absorbing.
For amplitude greater than1, four successive values already contradict the
three-value bound. QED.

If this entrance property holds for every qualified boundary from some
order H onward, set M=max(30,H). The proved width17 base and induction give

$$
C(F_k-v)=F_{k-1}\quad
\text{for }v\ge17,\quad k\ge M+6(v-17).
$$

Equivalently, the conditional exact negative width grows at least as
17+floor((k-M)/6). The domain condition holds at the width18 base and
continues to hold as each six-order increment increases Fibonacci size
faster than the gap. The universal entrance premise is still open.

**What perpetual copying would require.** Without assuming this premise,
a perpetually surviving gap-v defect must have an entrance flag0 at least
once in every five consecutive orders above K+1; if p>1, every four orders
suffice. Each such flag gives an actual cap-hole witness: the preceding
exterior point x<A-v satisfies

$$
C(x)=B=C(A),\qquad C(A-v)=B-p<B,
\qquad A=F_{h-1},\ B=F_{h-2}.
$$

Indeed its next image is exactly the lower entrance endpoint A-v, forcing
the displayed equality. Thus a failure of fixed-width extinction needs
recurring holes on the prescribed entrance paths, with order density at
least1/5 (at least1/4 for p>1). Proving global top-plateau contiguity would
exclude these holes and is one sufficient route. The weaker path-based
entrance property, or a suitable bound on their recurrence, also suffices.

Complete finite blocks through order30 have contiguous top plateaus, and
all checked nonzero boundary entrances have flag1. Neither observation
establishes the universal entrance property. The envelope theorem and state
minima are proved; arbitrary negative-width extinction and the full actual-C
recursive minimum remain open. None of these fixed-width results supplies
the uniform dispersion estimate in wide arches.

### The prescribed basin and phase in a positive collar

The complete cycle list does not by itself determine which cycle the
prescribed start reaches. The golden lower bound and exact equality set
give that missing information on a smaller positive band.

**Selected-endpoint theorem.** Put n=F_k+t, A=F_(k-1), B=F_(k-2).
For every k>=24 and 1<=t<=21, the orbit from n-1 first enters [A,A+t]
at its upper endpoint A+t, at an even time. Its eventual cycle is
exactly {A,A+t}. Its prescribed endpoint s(n) is

$$
s(F_k+t)=
\begin{cases}
A+t,&A+t\text{ is odd},\\
A,&A+t\text{ is even}.
\end{cases}
$$

**Proof.** The nondecreasing upper cap gives C(x)<=B for every x<A.
For A+t<x<=A+32, the proved order-(k-1) collar gives
C(x)=B+x-A>B+t. We claim the same strict separation for all x>=A+33.
Write j=k-1>=23 and alpha=1/phi. The Fibonacci identity
B-alpha*A=(-alpha)^j and 34alpha-21=alpha^9 give

$$
\alpha(A+34)-B=21+\alpha^9-(-\alpha)^j.
$$

This lies strictly between 21 and 22, and adding alpha once or twice shows
G(A+33)=G(A+34)=B+21 and G(A+35)=B+22. For example
0.618<alpha<0.619, 0.013<alpha^9<0.014 and alpha^23<0.0001
suffice to justify all three floors. The indices A+33 and A+34 lie
strictly between F_j+1 and F_(j+1)-1 and exceed 59, so neither belongs
to the exact equality set Z. Hence C(A+33),C(A+34)>=B+22.
Monotonicity of G gives C(x)>=B+22 for every x>=A+35.
Since t<=21, C(x)>B+t throughout the high exterior x>A+t.

Thus a high exterior point maps strictly below A, and a low exterior
point maps to at least A+t. The invariant interval [A,A+t] can be
entered only from the low side, at A+t. The start n-1 is on the high
side. Capture guarantees eventual entry, while the exterior sides
alternate, so its entry time mu is even. Inside the interval the collar
makes T_n the reflection x -> 2A+t-x. The entry point A+t therefore
generates the outermost two-cycle, even when other two-cycles or a fixed
point are present. The prescribed depth is d=C(n-1)=A+t-1, and the
established entry theorem gives d>=mu. Since mu is even, x_d is A+t
when d is even and A when d is odd. This is the stated formula. QED.

The exact equality set is essential for the last offset t=21: G alone
allows equality at A+33 and A+34. This theorem claims the band 1..21;
it does not assume the same basin or phase throughout the larger value
collar 1..32. For -12<=t<=0 the complete classification already gives
the unique selected fixed point A+t.

**Recursive-window consequence.** Consider any aligned window, including
a five-row window, with physical inputs F_j+u_i, 0<=u_i<=21, j>=24.
Set r_i=s(F_j+u_i)-F_(j-1) and q_i=u_i-r_i. Every row obeys

$$
r_i=\begin{cases}
u_i,&F_{j-1}+u_i\text{ is odd},\\
0,&F_{j-1}+u_i\text{ is even},
\end{cases}\qquad q_i=u_i-r_i.
$$

At u_i=0 the anchor landing theorem supplies the same result. Each
child again has offset in 0..21, with order j-1 or j-2; the nonzero
offset is unchanged along its carrying branch. The parity of F_(j-1)
depends only on j mod 3: it is even exactly when j=1 mod 3. Thus
order mod 3 and the row's offset determine every high-order child split
and its actual selected validity, without a supplied inverse branch,
basin or phase label. For j>=25 both child profiles are linear, so the
row parameters of the recursive-window interface are

$$
\alpha_i=r_{i+1}+r_i,\qquad
\beta_i=q_{i+1}+q_i,\qquad
A_i=u_{i+1}+u_i=\alpha_i+\beta_i.
$$

Iterating these rules reaches boundary orders 22 or 23. Their selected
splits are fixed finite data, rather than free choices at every higher
order. The checker records all 44 boundary inputs with offsets 0..21
and checks their literal prescribed iterations. This consequence is for
nonautonomous row windows: the autonomous positive collar itself has
only periods one and two, so it contains no distinct five-cycle. It
does not classify five-cycles in the wider Fibonacci arches.

This supplies an actual C counterpart to Campbell's ternary endpoint
templates. The collar values already propagated independently of phase;
the new statement additionally proves the prescribed endpoint and the
arithmetic branch rule. It does not establish a minimum full certificate
size or extend the branch rule beyond the stated band.

The maintained checker compares full-orbit and Brent prefixes through
131071, then checks all 63 cases k=24,25,26, t=1..21 by literal prescribed
iteration. It checks the exterior separation and alternating sides, exact
outer cycle, even entry and predicted endpoint. All these finite entry
times happen to be 14; no uniform exact transient of 14 is asserted.
All 968 offset-pair edges at orders 25 and 26 check the arithmetic child
parameter formulas against actual selected splits and values. Additional
floor checks at Fibonacci scales near 10^100 use integer square roots and
introduce no new sequence premise.

### A saturated lower barrier and the exclusion of nearby proper cycles

The linear collar can be strengthened to a lower bound on the **entire**
positive natural block. This adds a position constraint to a proper
five-cycle and extends the arithmetic selected-endpoint rule.

**Saturation propagation theorem.** Let K>=6 and let W be an integer
with 0<=W<=F_(K-2). Suppose the two profiles at j=K,K+1 satisfy

$$
P_j(u):=C(F_j+u)-F_{j-1}\ge\min(u,W)
\qquad(0\le u\le F_{j-1}).
$$

Then the same bound holds for every j>=K on its closed natural block.
The upper cap also gives P_j(u)<=u, so P_j(u)=u for 0<=u<=W.

**Proof.** At the upper endpoint u=F_(j-1), Fibonacci landing gives
P_j(u)=F_(j-2)>=W. For all other offsets use the selected split
u=r+q in the two closed lower natural blocks. The established profile
identity and induction give

$$
P_j(u)=P_{j-1}(r)+P_{j-2}(q)
\ge\min(r,W)+\min(q,W)\ge\min(r+q,W).
$$

This proves the induction. It uses the actual recurrence and its capture
bounds, without requiring a particular selected phase. QED.

**Certified barrier.** The theorem holds with K=23 and W=32. Offsets
0..32 in the two seeds are already the certified exact collars. The
additional finite premises are only the **36 values** at offsets 33..50
in orders 23 and 24, each with relative value at least 32. The least is 32,
at F_23+33. For every j>=23 the Fibonacci identity gives

$$
\alpha(F_j+52)-F_{j-1}=52\alpha-(-\alpha)^j>32,
$$

since alpha>0.618 and alpha^23<0.0001. Thus G(F_j+51)>=F_(j-1)+32,
and monotonicity of G covers every larger offset in either seed. This
certifies their whole closed blocks without checking all their entries.
The propagation theorem proves

$$
\boxed{\min(u,32)\le P_j(u)\le u
\quad(j\ge23,\ 0\le u\le F_{j-1}).}
$$

The new finite premises are checked in the existing independently agreeing
full-orbit and Brent prefix; no larger prefix is needed. The lower bound
does not assert that P_j is monotone beyond the collar.

**Spatial cycle theorem.** Let an integer profile H on a cycle's domain
satisfy min(u,W)<=H(u)<=u, and let the transition be u -> t-H(u).
Every cycle of period p>=3 lies in

$$
W+1\le u\le t-W,\qquad p\le t-2W.
$$

**Proof.** Let m and M be the minimum and maximum cycle points. If m<=W,
then H(m)=m and H(u)>=m at every cycle point. Consequently
M=t-m. A predecessor v of m satisfies H(v)=t-m=M, while
H(v)<=v<=M. Hence v=M and H(M)=M. The two extremal points map to
each other, contradicting period at least three. Thus m>W. Every cycle
point now has H(u)>=W, so its image is at most t-W. The integer interval
{W+1,...,t-W} contains t-2W points, proving the period bound. QED.

For C, take n=F_k+t with k>=24 and 0<=t<F_(k-1). Intersected capture
already places every cycle point x=F_(k-1)+u in the natural domain of
P_(k-1). Combining its geometry with the saturated barrier shows that
every proper cycle lies in

$$
\max(33,t-F_{k-3})\le u\le\min(t-32,F_{k-2}).
$$

Its period is bounded by the number of integers in this intersection,
and in particular by t-64. Therefore offsets 0..66 have only fixed points
and two-cycles, and a five-cycle requires **t>=69**. This is a universal
exclusion near high-order anchors, not an assertion that a C five-cycle
exists at the first permitted offset.

The spatial bound is sharp in the abstract capped/saturated class.
For any W>=0 and p>=3 set t=2W+p. If p is odd, choose centred labels
`(1,-1,3,-3,...,p-2,-(p-2),p)`; if p is even, use
`(-(p-2),p-2,-(p-4),p-4,...,-2,2,0,p)`. Put
u_i=W+(p+z_i)/2 and H(u_i)=t-u_(i+1), using H(u)=u elsewhere.
The u_i permute {W+1,...,W+p}, every adjacent pair sums to at least t,
and H(u_i)>=W. Thus the profile has the required bounds and a genuine
p-cycle with p=t-2W. Its total defect is also exactly p. These examples
are not claimed to satisfy C's recurrence.

**Extended actual selector theorem.** For k>=24 and **1<=t<=32**, the
prescribed cycle is the outermost pair {A,A+t}, A=F_(k-1), and
the endpoint is still A+t when A+t is odd, otherwise A. For t<32,
first entry is at A+t at an even time. At t=32, it may instead enter
at A at an odd time; the same selected-endpoint formula holds.

**Proof.** Below A, C(x)<=B=F_(k-2). Above A+t but within the lower
linear collar, C(x)>B+t. Above that collar the new barrier gives
C(x)>=B+32; beyond its natural block, monotonicity of G and Fibonacci
landing give the same lower bound. Thus high exterior points map below A
when t<32, or to at most A when t=32; low exterior points map to at
least A+t. Until entry the sides alternate. Entry is therefore at A+t
at an even time or, only when t=32, at A at an odd time. Both cases
generate the outer pair. On that pair, even orbit clocks have value A+t
and odd clocks have value A. The exact depth d=A+t-1 is after entry,
giving the claimed selection by its parity. QED.

The recursive-window consequence above now applies to all offsets 0..32:
order mod 3 and offset parity determine the actual high-order splits,
and the two boundary orders 22/23 need 66 fixed input records in total.
The child parameter formulas remain valid at orders>=25. This phase
extension uses the 36 new lower-barrier premises; the earlier 1..21 theorem
did not need them.

For a genuine five-cycle, the known barrier supplies an exact shifted
interface. Set v_i=u_i-32, tau=t-64 and
Q(v)=P_(k-1)(32+v)-32. On the available natural domain, 0<=Q(v)<=v,
v_(i+1)=tau-Q(v_i), and every v_i is a positive integer at most tau.
The defect word is unchanged. All alternating closure, centroid and
reverse gap identities apply after this translation. The generic affine
dimension is unchanged; the improvement is a proved family domain, which
excludes impossible positions before inverse reconstruction. Recursive
child windows with varying row parameters are nonautonomous, so the
spatial period theorem must not be applied to their row clock.

Three actual boundary examples distinguish the remaining information:

- At n=F_24+33=46401, the prescribed cycle has offsets (1,32), transient 15
  and selected offset 1. Extending the collar endpoint formula would predict
  offset 0. Thus the first offset beyond 32 already needs a different basin
  rule. Both cycle phases nevertheless give the same root value 28690;
  value reconstruction and selected-layout reconstruction are different tasks.
- At n=F_25+42=75067, the cycle offsets are (42,0), both with zero local
  defect, but their candidate root values are 46410 and 46407. The prescribed
  depth 46409 selects the lower endpoint and gives 46407=F_24+39.
  Its complementary child has P_23(42)=39. A pure reflection cycle does
  not make the root value phase independent across two different lower orders.
- At n=F_25+43=75068, that nonlinear predecessor changes the actual depth
  to 46407, whereas the linear prediction is 46410. The prescribed cycle is
  still the outer pair (43,0), entered at time 14, but the selected offset is 0
  rather than the 43 predicted by the collar parity formula. Here the basin
  is correct and the missing information is the depth parity.

All three endpoints are checked by literal prescribed iteration. They show
why a wider closure interface must track basin, the relevant depth residue
and whether cycle phases have equivalent outputs separately. Short cycles
and zero cycle defects alone do not supply those data.

The checker exhausts 4375 small capped/saturated profiles, checks 282 proper
cycles and 30 sharp constructions, and corroborates the C domain bound on
53,779 selected proper cycles through 131071, including 4753 five-cycles.
An additional 102 all-start graphs at offsets 33..66 contain 8,259,671 vertices
and have no period above two. Literal iteration verifies the 33 additional
phase cases at orders 24..26, including lower-endpoint odd entry at
F_24+32, and 22 additional boundary records. Full convergence, the wider-arch
prescribed phase and the minimum complete five-window interface remain open.

### Every fixed positive offset eventually becomes linear

The fixed-width seed condition can now be advanced by one offset at a time.
A defect at the new offset can only persist by copying the same defect
from two orders below. The actual selected phase restricts that copy by
Fibonacci parity, and this restriction eventually kills every such chain.
This is an infinite proof, not an extrapolation from larger seed searches.

**One-offset persistence lemma.** Fix u>=1 and K>=6, with
u<=F_(K-2). Suppose

$$
P_h(v)=v\qquad(h\ge K,\ 0\le v<u).
$$

Write D_h=u-P_h(u)>=0. For every j>=K+2, a surviving defect satisfies

$$
D_j>0\Longrightarrow
\left\{
\begin{aligned}
D_j&=D_{j-2}>0,\\
D_{j-1}&=0,\\
F_{j-1}+u&\text{ is even}.
\end{aligned}
\right.
$$

**Proof.** Capture places the actual selected split at F_(j-1)+r,
0<=r<=u. At every interior offset v<u the preceding profile is the
identity. At its last offset put p=P_(j-1)(u). The cap gives p<=u,
and G(F_(j-1)+1)=F_(j-2)+1 gives p>=1 by monotonicity of G.

If p<u, the captured map sends 0 to u and sends u to u-p in
{1,...,u-1}. All interior points follow the reflection v -> u-v.
Neither 0 nor u is periodic: no point maps to 0, since every profile value
is strictly below u. The prescribed depth is on a cycle, so0<r<u.
Both child offsets are smaller than u, and their proved profiles give
P_j(u)=r+(u-r)=u. Thus a surviving defect requires p=u, or D_(j-1)=0.

In that case the whole captured interval is reflection. If r>0, its
first child has profile value r, including r=u, and its complementary
offset is smaller than u. Again P_j(u)=u. The only remaining case is
r=0, giving P_j(u)=P_(j-2)(u), hence D_j=D_(j-2).

It remains to use the prescribed phase. Write A=F_(j-1), B=F_(j-2).
For x<A the cap gives C(x)<=B; for x>A monotonicity of G gives
C(x)>=G(A+1)=B+1. Exterior sides relative to [A,A+u] therefore alternate
until entry. If the selected split is A, the prescribed cycle is the
outer pair {A,A+u}, so first entry is A+u at an even clock or A at an
odd clock. On that pair, even clocks select A+u and odd clocks select A.
The exact depth is C(F_j+u-1)=A+u-1 by the smaller-offset hypothesis.
Selection of A consequently requires A+u even. QED.

**Finite extinction.** If u is even, a defect copy is allowed only at
j=1 mod 3. If u is odd, it is allowed only at j=0 or 2 mod 3.
No new defect can appear; every surviving value is copied along steps
of two. Three such steps visit all order classes and include a forbidden
class. The first order after which all possible copies have died is:

| K mod 3 | Increment when u is even | Increment when u is odd |
|---:|---:|---:|
| 0 | 2 | 6 |
| 1 | 4 | 5 |
| 2 | 3 | 4 |

For example, when K=2 mod 3 and u is odd, the value at K+2 is zero.
The value at K+3 may copy the second initial defect, but K+4 copies
the already zero value at K+2, and K+5 is forbidden. All later values
are zero. When K=0 mod 3 and u is even, both first updates K+2,K+3
are forbidden and the whole tail is zero. The other table entries follow
by the same two-step copy check. The table is exact for this necessary
rule envelope; it is not a claim that every permitted history occurs in C.

**Growing positive collar theorem.** Define K(u)=23 for 0<=u<=32, and

$$
K(u)=23+3(u-32)+((u-32)\bmod2)\qquad(u\ge33).
$$

Then for every fixed u>=0 and every j>=K(u),

$$
\boxed{C(F_j+u)=F_{j-1}+u.}
$$

**Proof.** The certified band 0..32 starts the induction. Its threshold 23
has order class 2. The next odd offset needs four more orders, giving
class 0; the next even offset needs two more, restoring class 2. These
increments alternate, yielding exactly the displayed formula. The size
condition u<=F_(K-2) holds at u=33 and is preserved as K rises by at
least two at each new offset. Apply the persistence lemma and extinction
table successively. No additional sequence seeds are required. QED.

Equivalently, for j>=23 the exact positive collar has the proved width

$$
L_j=32+2\left\lfloor\frac{j-23}{6}\right\rfloor
+\mathbf1_{\{(j-23)\bmod6\ge4\}}.
$$

In particular, every finite positive width R eventually has two consecutive
exact seed collars, with the previously certified negative width 12.
This answers the positive-width seed-existence question. It does not
establish arbitrary negative widths or full ratio convergence.

**Growing actual selector domain.** Put W_j=max(32,G(L_j)), using the
ordinary Hofstadter G. The whole closed natural profile obeys

$$
\min(u,W_j)\le P_j(u)\le u\qquad(j\ge23).
$$

For u<=L_j this follows from its exact value. For u>=L_j+1, the
Fibonacci floor identity gives
G(F_j+u)-F_(j-1)>=G(L_j): the extra alpha between
alpha(L_j+2)-(-alpha)^j and alpha(L_j+1) exceeds the tiny signed error.
Combine this bound with the already proved saturated width 32. The displayed
formula gives L_j<=F_(j-2), first at j=23 and then by its growth of at
most one per order, so the domains fit inside their natural blocks.
Thus W_j/j tends to alpha/3, so these domains grow without bound.

At n=F_k+t, k>=24, every 1<=t<=W_(k-1) has the proved outer prescribed
cycle and selected endpoint A+t if A+t is odd, otherwise A.
The saturation/entry proof above applies with W=W_(k-1); the exact depth
is available because W_(k-1)<=L_(k-1)<=L_k. A proper p-cycle instead
requires t>=2W_(k-1)+p, with the corresponding interior spatial domain.
These are growing family domains computable from the order, rather than
additional row selectors, basin labels or phase residues.

For recursive windows the arithmetic gate applies separately at a row of
order j when its offset is at most W_(j-1). At j>=25 both lower profile
values are known too, since W_(j-1)<=L_(j-2). The same child parameter
formulas alpha_i=r_i+r_(i+1) and beta_i=q_i+q_(i+1) therefore apply.
Descent lowers the order and
can leave this growing gate. The remaining boundary depends on the offset;
it must not be treated as the fixed 66-record boundary of the width 32 case.
The general five-window inverse and prescribed-phase questions outside
the gate remain open. Campbell's ternary templates provide the comparison:
its arithmetic rules cover whole ternary sectors, while the present exact
C domains have width of order log(F_j), not a fixed fraction of F_j.

The checker exhausts local capped top-value pairs and all periodic split
witnesses, verifies all six finite extinction envelopes, and checks the
threshold recurrence through u=1000. Conditional persistence is also
checked directly in the small C prefix. Independent full-orbit and Brent
evaluation through 832074, within the already published 2^20 range, checks
the first new thresholds u=33 at orders 27..30 and u=34 at orders 29..30;
their selected endpoints are rechecked by literal iteration. These are
corroboration of the infinite argument, not its finite premises.

### Five legal bit patterns and eventual vanishing of a local interaction

The five legal patterns in a three-bit Zeckendorf window are
`000,100,010,001,101`. They are a digit alphabet, distinct from the five
points of a period-five inner orbit. The representation and its carry
interface are developed in [FIB relational continuation geometry, Sections
14-17](https://github.com/the-omega-institute/trureturing/blob/c71e2e9599ea407fae545287b024590c444b03ef/docs/develop/theory/FIB_RELATIONAL_CONTINUATION_GEOMETRY.md).
The following elementary interpolation gives an explicit connection to the
fixed-offset theorem above, without identifying these two uses of five.

**Five-pattern interpolation.** Every real-valued function on this alphabet
has the unique expansion

$$
f(x)=b+a_1x_1+a_2x_2+a_3x_3+\kappa x_1x_3,
$$

where b=f(000), a_i=f(e_i)-b and

$$
\kappa=f(101)-f(100)-f(001)+f(000).
$$

Indeed the empty pattern and the three singleton patterns determine the
first four coefficients; the last pattern then determines kappa. Conversely,
substitution recovers every value. Thus observing only the first four
patterns leaves exactly one scalar degree of freedom for an unrestricted
function. An additive model assumes kappa=0; that assumption does not follow
from those four observations.

**Actual C readout.** For j>=7 the five numbers

$$
F_j,\quad F_j+2,\quad F_j+3,\quad F_j+5,\quad F_j+7
$$

have the same higher Zeckendorf digits and unit bit zero; only their lowest
window varies over these five patterns. Define f_j(x)=C(F_j+2x_1+3x_2+5x_3).
The corresponding interaction is therefore the actual sequence difference

$$
\kappa_j=C(F_j+7)-C(F_j+2)-C(F_j+5)+C(F_j).
$$

The certified positive collar gives, for every j>=23,

$$
f_j(x)=F_{j-1}+2x_1+3x_2+5x_3,\qquad \boxed{\kappa_j=0}.
$$

This is an infinite consequence of the collar theorem. At lower orders the
interaction need not vanish: at j=9 the five C values, in the order above,
are (21,23,24,25,28), giving kappa_9=1. The zero observed at j=11 does
not yet persist: kappa_12=1. These small values can be checked by literal
iteration and do not supply the infinite premise.

**Any fixed window.** Fix i>=0 and put
w_1=F_(3i+3), w_2=F_(3i+4), w_3=F_(3i+5), R=w_1+w_3.
For j>=max(3i+7,K(R)), the five canonical words with a fixed higher
digit F_j and this window varying give

$$
C(F_j+w_1x_1+w_2x_2+w_3x_3)
=F_{j-1}+w_1x_1+w_2x_2+w_3x_3.
$$

All five offsets lie in 0..R, where K is nondecreasing, so the fixed-offset
theorem proves the formula and zero interaction. More generally, any fixed
legal lower-digit context with numeric contribution h>=0 satisfies the
same conclusion for j large enough to separate F_j from the context and
j>=K(h+R), provided all five window choices are legal in that context.
The fixed-context condition matters: it does not allow a window growing
arbitrarily with j or erase cross-window seam restrictions.

Vanishing of this scalar interaction is not a certificate of inner-orbit
closure or selected phase. For example, order25 already has kappa_25=0,
but at F_25+42=75067 the outer two phases give different root values
46410 and46407, as checked above. The window response and the recurrence's
basin/depth interface answer different questions. The checker records the
twenty lowest-window responses at orders7..26, reconstructs3125 exact
five-pattern functions, and verifies the four high-order linear responses
inside its existing independently checked prefix.

# Exact Fibonacci collars and selected phases

[Project home](../README.md) · [Research map](README.md#technical-research-map)

This note proves exact values and cycle selection near Fibonacci indices,
including eventual linearity at every fixed positive offset. It builds on the
[global golden theorem](golden-proof.md) and [orbit capture](fibonacci-collars.md).
Finite seed premises are identified in each theorem. Global convergence remains open.

## Contents

- [6. Exact collars propagate from two seeds](#6-exact-collars-propagate-from-two-seeds)
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
for every positive width with the already proved negative width 12; arbitrary
negative widths remain open. These neighborhoods do not control Fibonacci-block
centers or settle full ratio convergence.

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

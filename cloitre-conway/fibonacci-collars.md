# Fibonacci collars: bounded periods and exact nearby dynamics

This note derives new consequences of the [global golden-structure proof](golden-proof.md).
It uses its proved G lower bound, exact equality set and upper cap. Sections 1–4
introduce no additional finite premise. The [exact-collar note](exact-collars.md)
proves wider-band identities from stated finite seed premises.
The universal conclusions inherit the global proof's computer-assisted
foundations. No Lean formalization is claimed.
Use F_0=0, F_1=1 and alpha=1/phi.

[Project home](../README.md) · [Research map](README.md#technical-research-map)

## 1. All cycles near a Fibonacci index

**Theorem.** Let k>=6, let t be any integer with n=F_k+t>=3, and set
A=F_(k-1). Every cycle of T_n(x)=n-C(x) on [1,n-1] lies in

$$
I_{k,t}=[A+\min(0,t),\ A+\max(0,t)].
$$

Every orbit eventually enters this interval. Consequently every cycle has
period at most |t|+1, including the cycle selected by the defining depth.

**Proof.** Apply the proved cycle-capture lemma at the anchor
(A,B)=(F_(k-1),F_(k-2)). Since n-B=A+t, its capture interval is exactly
I_(k,t). Its intersection with the actual domain is invariant, and outside
it the integer distance decreases within every two iterations. Thus every
orbit enters it. A cycle visits distinct integer points, so its period is at
most the interval's |t|+1 integer points. The chosen depth is already known
to reach a cycle. QED.

This result does not bound periods uniformly across all n: in the middle of
a Fibonacci block, the distance |t| to the nearest anchor is of order n.
For any fixed offset, however, the period bound is independent of k.

### Quantitative capture and a short exterior certificate

The distance decrease in the capture proof can be strengthened to a uniform
contraction. First, for every `j>=5` and `1<=d<F_j`,

$$
F_{j-1}-C(F_j-d)\le\left\lfloor\frac{2d}{3}\right\rfloor. \tag{1.1}
$$

**Proof.** Write `A=F_j`, `B=F_(j-1)`, and `alpha=1/phi<5/8`. The G lower
bound and `G(A)=B` give

```text
B-C(A-d) <= G(A)-G(A-d) <= ceil(alpha*d).
```

If `d>=24`, then `ceil(alpha*d)<alpha*d+1<5*d/8+1<=2*d/3`, proving
(1.1). For `j>=11` and `2<=d<=23`, the point `A-d` is outside the exact
equality set: the previous Fibonacci-plus-one is at distance
`F_(j-2)-1>=33`, and the largest exceptional zero 59 is at distance at
least 30. Hence `C(A-d)>=G(A-d)+1`, giving
`B-C(A-d)<=ceil(alpha*d)-1<alpha*d<2*d/3`. For `d=1`, the already proved
anchor bound gives `C(A-1)=B`. For the remaining `j=5,...,10`, use the proved
integer lower bound `C(x)>=G(x)+1` outside the equality set and `C(x)=G(x)`
inside it. The 130 cases are direct floor/equality-set arithmetic on
`1<=x<=54`; the collar verifier checks each inequality with this lower bound,
without substituting a newly computed C-value. There is no additional
sequence-prefix premise. QED.

Now let `I` be the capture interval between `A` and `n-B`, and let
`rho(x)=dist(x,I)` for any integer `1<=x<n`. Then

$$
\rho(T_n^2(x))\le\left\lfloor\frac{2\rho(x)}3\right\rfloor. \tag{1.2}
$$

To prove it for either sign of `D=n-A-B`, put
`L=A+min(0,D)` and `R=A+max(0,D)`. A point `x=L-d` below the interval
has `T_n(x)>=L` and

```text
T_n(x)-R = min(0,D)+B-C(x)
           <= min(0,D)+floor(2*(d-min(0,D))/3)
           <= floor(2*d/3).
```

A point `x=R+d` above the interval maps to `[L-d,R]` by the monotone
1-Lipschitz cap. Thus each exterior step switches sides or enters the
interval; the below-to-above step contracts by (1.1), and the above-to-below
step does not increase distance. Invariance handles points already inside.
Combining two steps proves (1.2). The factor is attained at `A=5`, `n=8`,
`x=2`: the interval is `{5}`, the initial distance is three, and
`T_8^2(2)=3` has distance two.

Define the integer budget

```text
Q(0)=0,
Q(d)=1+Q(floor(2*d/3))   for d>=1.
```

If the starting distance is `d_0`, the first entrance time `tau` satisfies
`tau<=2*Q(d_0)`. For `d_0>=1`,
`Q(d_0)<=1+floor(log_(3/2)(d_0))`, so capture needs `O(log(d_0+1))`
steps. For the prescribed start `n-1` at `n=F_k+t`,

```text
d_0 = max(0, F_(k-2)+min(0,t)-1).
```

For example, at n=8 this distance is two, `Q(2)=2`, and the trajectory
`7,3,6,4,5` has transient length four, attaining the entrance bound.
This gives a short exterior certificate: relative to verified C-values,
record the actual path through its first point in `I`. It uses at most
`2*Q(d_0)+1` states and fixes the entrance point and entrance time. The
bound alone does not identify that point; the checked path is still needed.

If the eventual period is `ell`, at most `|t|+1-ell` further transient
points can occur inside `I`. Therefore the full preperiod obeys

$$
\mu+\ell\le2Q(d_0)+|t|+1. \tag{1.3}
$$

In particular, `mu=O(k+|t|)`. Along any sublinear neighborhood
`|t_k|=o(F_k)`, both `mu=o(F_k)` and `mu/C(F_k+t_k-1)->0`: asymptotically
almost all of the prescribed iterations take place on the cycle. This does
not imply logarithmic full landing in a wide arch; its interior transient
is a separate problem.

### Intersecting the anchor bounds

The two adjacent anchors give a stronger global consequence. Write
`n=F_k+t`, `0<=t<F_(k-1)`, `k>=6`, and put `a=F_k`, `b=F_(k-1)`,
`c=F_(k-2)` and `h=F_(k-3)=b-c`. The capture intervals from anchors b and a
intersect in

$$
J_n=[\max(b,n-b),\ \min(n-c,a)]. \tag{1.4}
$$

Every earlier anchor interval contains `[b,n-c]`, and every later one
contains `[n-b,a]`. Thus J is the intersection of **all** eligible Fibonacci
anchor intervals. Its width is exactly

```text
w = min(t,h,b-t).
```

Relative to the anchor b, these are three affine domain shapes:

| Offset range | Normalized core `J-b` | Width |
|---|---|---|
| `0<=t<=h` | `[0,t]` | t |
| `h<=t<=c` | `[t-h,t]` | h |
| `c<=t<=b` | `[t-h,c]` | b-t |

The formulas agree at shared boundaries. This arithmetic domain restriction
needs no additional stored coordinate once the scale and offset are known.
It gives a bound `period<=w+1` on all cycles, not a claim that actual periods
attain it. Campbell's ternary domain templates additionally determine the
orbit endpoints and phase; for C, the lower-profile dynamics inside these
Fibonacci domains still have to be certified.

Distance to an intersection of overlapping intervals is the maximum of their
distances. Applying (1.2) to each anchor therefore proves the same two-step
contraction for J. At the prescribed start its distance is
`d_J=max(c,t)-1`, and the full orbit budget satisfies

$$
\mu(n)+\ell(n)\le2Q(d_J)+w+1. \tag{1.5}
$$

Set `beta=(3-sqrt(5))/4=1-1/(2*alpha)`. Within a block, the largest value
of `w-beta*n` occurs at the start of the width plateau, `t=h`, `n=2b`.
Its value is `(b-alpha*a)/alpha`, of absolute value less than one by the
Fibonacci identity. Therefore `w<beta*n+1`, and, for all `n>=8`,

$$
\mu(n)+\ell(n)<\frac{3-\sqrt5}{4}n+2Q(d_J)+2.
$$

Since `d_J<=n`, the second term is `O(log n)`. Thus
`limsup (mu(n)+ell(n))/n <= (3-sqrt(5))/4`, improving the elementary
`17*n/32+4` bound for this joint orbit budget. It does not prove sublinear
periods or transients throughout all arches.

In the exact collar `k>=24`, `-12<=t<=32`, the interior simplifies further.
For `t>=0`, every captured point is already on the reflection cycle, so
`mu=tau`. For `t<0`, the map sends every captured point to the unique fixed
point on its next step, so `mu<=tau+1`. A verified exterior path therefore
completes the basin certificate with at most one further transition. For a
positive reflection pair, the entry point and `C(n-1)-tau mod 2` identify
the selected split; for a fixed point no phase label is needed. If only the
value C(n) is wanted, the collar's two-child sum is phase-independent, so
no basin or phase label is needed beyond the proved capture and collar data.
Campbell's explicit templates make a stronger family-specific reduction:
his full prescribed transient is at most four, while here the certificate
has a logarithmic exterior and, outside the collar, an unresolved interior.

The interior term cannot be removed from a generic capped-profile argument.
For any fixed integer `W>=0` and `m>W`, take the interval `{0,...,2m}` and

```text
H(u)=u-1   for W<u<=m,
H(u)=u     otherwise.
```

This profile is nondecreasing, `0<=H(u)<=u`, its defects are only zero or one,
and it is exactly identity on `{0,...,W}`. For `Psi(u)=2m-H(u)`, an orbit
starting at m alternates downward through the low side and upward through the
high side until it reaches the terminal two-cycle `(2m-W,W)`. Its preperiod
is exactly `2*(m-W)-1`. For W=0, `mu+period=2m+1`, attaining the interval's
cardinality; for W=32, a fixed identity collar still leaves linearly long
interior transients as m grows. This is an abstract profile counterexample,
not a C instance. It shows that bounded defects, monotone branches and small
periods do not by themselves bound the number of individual basin transitions.
A stronger interior-time bound must use additional family information. The
following return certificate distinguishes this time bound from the size of
a proof that encodes many transitions arithmetically.

### A ratio strip for high-order cycles

The global envelopes also confine interior cycles without constructing
their profiles. Put

$$
\ell=21/34,\qquad b=8900/13459,\qquad
L=\frac{1-b}{1-\ell b}=\frac{77503}{135353},\qquad
H=\frac{1-\ell}{1-\ell b}=\frac{174967}{270706}.
\tag{R.1}
$$

**Ratio-strip theorem.** Every cycle whose points are at least F_28
lies in[LN,HN] for T_N(x)=N-C(x). In particular this applies when
the two-anchor capture core has lower endpoint at least F_28.
If the whole strip is above that threshold, its integer points are
invariant under T_N. This narrows the cycle search domain; it does
not select a basin or phase.

**Proof.** First, ell*n<=C(n)<=b*n for all n>=F_28=317811.
For the lower bound, alpha>55/89 because5*89^2>199^2. Thus
C(n)>=G(n)>=(55/89)(n+1)-1>=(21/34)n for n>=1156.
For the upper bound above349525 use the established
[global ratio certificate](golden-proof.md#8-shorter-certificates-and-the-global-limsup).
Between F_28 and349525, the upper cap is n-F_26, and
4559*349525<=13459*F_26. This gives the same b bound there,
without a new finite premise.

Let m and M be the minimum and maximum points of a cycle. Since
its images are the same set,

$$
m\ge N-bM,\qquad M\le N-\ell m.
$$

Combining gives m>=LN and then M<=HN. For a point in the strip,
the same scalar bounds give N-b*HN=LN<=T_N(x)<=N-ell*LN=HN.
Integer images therefore remain between ceil(LN) and floor(HN).
QED. The statement is about every qualified cycle, not only the
one reached from the prescribed start.

### Defect-plateau return certificates

Long transients need not require long certificates. Let `Psi(u)=t-H(u)` on
an invariant integer domain, and write `lambda(u)=u-H(u)`. Suppose the
verified profile has constant defect a on an interval A and constant defect
b on an interval B. The paired return cell is

$$
K=A\cap[t+a-\max B,\ t+a-\min B]. \tag{1.6}
$$

For every u in K, the first image is `t-u+a` in B, so

$$
\Psi^2(u)=u+b-a. \tag{1.7}
$$

Put `v=b-a` and `K=[L,U]`. If v is positive, the first exit from K under
these paired steps occurs after
`q=floor((U-u)/v)+1` pairs; if v is negative, after
`q=floor((u-L)/(-v))+1` pairs. In either case

```text
Psi^(2*j)(u)   = u+j*v,              0<=j<=q,
Psi^(2*j+1)(u) = t+a-u-j*v,          0<=j<q.
```

Every starting point for those q pairs is in K. The last endpoint may lie
outside K, but its last pair is still certified. For a smaller requested
depth D, use only `min(q,floor(D/2))` pairs and, if necessary, one further
literal step. If v is zero, `Psi^2(u)=u` immediately: the point is fixed
when `Psi(u)=u`, otherwise it lies on a two-cycle. These formulas prove the
entire run from two checked defect intervals, its start and one integer
division. The run length is derived from those data, rather than an extra
independent phase or branch coordinate.

One can concatenate these blocks, and record the exact number of elapsed
iterations. Revisiting the same block-boundary state certifies a positive
return time equal to the difference of the two elapsed times; reduce the
remaining depth modulo that return time. The least period may divide it.
At a zero-drift cell only parity remains. This
computes the exact selected point at the prescribed depth, preserving entry
alignment even when some literal path states were not individually stored.
The profile intervals must themselves be verified; endpoint values alone do
not establish constant defect throughout an interval.

For the abstract long-tail profile above, A is `[W+1,m]`, B is
`[m+1,2m]`, a=1 and b=0. Thus K=A, v=-1 and q=m-W. One translation block
from m reaches W after 2q steps, followed by the certified reflection pair
`(W,2m-W)`. The first cycle entry occurs one step earlier, at time 2q-1.
For any depth D the selected point is exactly

```text
max(W,m-D/2)             if D is even,
min(2m-W,m+(D+1)/2)      if D is odd.
```

The orbit can therefore have a linear transient and still have a certificate
with two blocks, independently of m; its integer parameters require
`O(log m+log(D+1))` bits. The earlier linear-tail example rules out a short
literal path, not a short arithmetic certificate. Campbell's endpoint
templates likewise supply arithmetic basin and phase information. For C,
the three Fibonacci core shapes determine the domain, but do not determine
its defect intervals or a short sequence of return blocks.

A genuine C witness occurs at n=248. Using `d(x)=x-C(x)` on the inner
state domain, d=56 on `[157,160]` and d=55 on `[144,148]`. The paired cell
is `[157,160]`; its drift is -1. From 160, four pairs reach 156:

```text
160 -> 144 -> 159 -> 145 -> 158 -> 146 -> 157 -> 147 -> 156.
```

The prescribed depth is C(247)=158, and the complete block certificate in
the [verifier evidence](verification/collar-check.json) selects 156, agreeing
with the independent full-orbit evaluator. The verifier checks every selected
split through n=131071, as well as all starts and depths through `2*t+7`
for every capped integer profile on `[0,t]`, `0<=t<=5`. It also checks the
two-block abstract formula at m=`10^12` and `10^18+7` without constructing
the long orbit. In the finite C audit only 581 indices admit a nontrivial
plateau jump, and the longest observed jump is four pairs. This audit gives
limited compression from constant defect plateaus; it proves no uniform
short C certificate. Larger certified return relations remain an open part
of recursive closure.

## 2. Two additional Fibonacci identities

**Proposition.**

$$
C(F_j+2)=F_{j-1}+2\quad(j\ge5),\qquad
C(F_j-2)=F_{j-1}\quad(j\ge8).
$$

**Proof.** Write q=F_j, p=F_(j-1). The exact identity
alpha q-p=(-1)^(j-1)alpha^j gives

$$
G(q+2)=p+1\quad(j\ge5),\qquad G(q-2)=p-1\quad(j\ge8).
$$

For the first floor, 3alpha-alpha^j lies above 1 and 3alpha+alpha^j
lies below 2 when j>=5. For the second, -alpha plus either signed alpha^j
is strictly between -1 and 0.

Neither q+2 (j>=5) nor q-2 (j>=8) belongs to the proved equality set Z.
For q+2, j=5 gives 7, the disallowed predecessor of the even anchor F_6;
for j>=6 it lies strictly more than one from either adjacent Fibonacci
number. For q-2 and j>=8 the same separation holds. Neither sign meets
the four exceptions: check j=5..10 for the plus sign (7,10,15,23,36,57) and
j=8..10 for the minus sign (19,32,53); subsequent indices exceed 59.

Their integer defects are therefore at least one. The upper cap yields
C(q+2)<=p+2, since U is 1-Lipschitz and U(q)=p, and C(q-2)<=p,
since U is nondecreasing. Combining both sides proves the identities. QED.

The negative-offset threshold matters: j=5,6,7 gives q-2=3,6,11 and
C-values 2,4,7, rather than the proposed 3,5,8.

## 3. Complete cycle classification for five offsets

Let k>=9, A=F_(k-1) and B=F_(k-2). The preceding identities and the
already proved neighboring identities give

$$
C(A-2)=C(A-1)=C(A)=B,\qquad
C(A+1)=B+1,\qquad C(A+2)=B+2.
$$

The capture interval from Section 1 and these values classify **all** cycles,
not only the orbit starting at n-1:

| n | Cycles of T_n | Eventual behavior of every orbit |
|---|---|---|
| F_k-2 | Fixed point A-2 | Reaches A-2 |
| F_k-1 | Fixed point A-1 | Reaches A-1 |
| F_k | Fixed point A | Reaches A |
| F_k+1 | Two-cycle A <-> A+1 | Reaches that two-cycle |
| F_k+2 | Fixed point A+1 and two-cycle A <-> A+2 | Reaches one of those two cycles |

**Proof.** At offset -2 the entire interval [A-2,A] maps to A-2. At
offset -1 the interval [A-1,A] maps to A-1. At zero its single point is
fixed. At offset +1, the two points map to one another. At offset +2,
T_n(A+s)=A+2-s for s=0,1,2, giving the displayed reflection. All of these
points belong to the domain, and every orbit enters the relevant interval.
QED.

The rows at offsets -1,0,+1 already hold for k>=6; offset +2 holds for
k>=6 as well. The common k>=9 threshold is needed only for the -2 row.
We do not assert which of the two +2 cycles the prescribed initial orbit
selects at every k. At all five offsets, its nesting depth retains at most
parity information once the orbit has reached a cycle.

## 4. Convergence within sublinear neighborhoods

**Theorem.** Suppose k tends to infinity and t_k is any integer sequence with
|t_k|/F_k -> 0. Then, for n_k=F_k+t_k,

$$
\frac{C(n_k)}{n_k}\longrightarrow\alpha.
$$

**Proof.** The G lower bound gives, for every positive n,

$$
C(n)-\alpha n\ge-\alpha^2.
$$

Write p=F_(k-1), q=F_k. Since U(q)=p and U is nondecreasing and
1-Lipschitz, its upper bounds give

$$
C(q+t)-\alpha(q+t)\le
\begin{cases}
\alpha^2t+(-1)^k\alpha^k,&t\ge0,\\
\alpha|t|+(-1)^k\alpha^k,&t<0.
\end{cases}
$$

For t>=0 use U(q+t)<=p+t; for t<0 use U(q+t)<=p. In both cases
p-alpha q=(-1)^k alpha^k. Dividing by q+t proves the limit, since
q+t is asymptotic to q. QED.

These estimates also give uniform convergence on every window
|n-F_k|<=h_k with h_k=o(F_k). They do not settle the full limit of C(n)/n:
indices a fixed fractional distance from the anchors remain uncontrolled by
this shrinking-window argument. A global limsup proof and a logarithmic
decay rate are still open.

## 5. Reproduction

The [two-collar propagation theorem](exact-collars.md#6-exact-collars-propagate-from-two-seeds)
strengthens the nearby dynamics: for all k>=23 the whole band
-12<=t<=32 has C(F_k+t)=F_(k-1)+max(0,t). For k>=24, all its cycles are
fixed points or two-cycles. Its additional finite premises are two explicitly
checked collars, recorded by the same checker.

The [collar checker](verification/collar_check.py) verifies the neighboring identities,
the selected-orbit localization through 131071, and **all starting states**
of the functional graphs at offsets -2..2 around F_6 through F_26. It
compares independently generated full-orbit and Brent prefixes and a literal
prefix. Its [recorded output](verification/collar-check.json) is finite corroboration;
the universal arguments are those above.

From the repository's main folder:

```sh
python3 cloitre-conway/verification/collar_check.py
python3 scripts/verify.py
```

## Related topics and preserved links

The following sections now have dedicated notes. Their original anchors remain
here so previously shared links still lead to the corresponding argument.
Use the [research map](README.md#technical-research-map) for a guided route.

## 6. Exact collars propagate from two seeds

[Read this section in its topic note](exact-collars.md#6-exact-collars-propagate-from-two-seeds).

### The prescribed basin and phase in a positive collar

[Read this section in its topic note](exact-collars.md#the-prescribed-basin-and-phase-in-a-positive-collar).

### A saturated lower barrier and the exclusion of nearby proper cycles

[Read this section in its topic note](exact-collars.md#a-saturated-lower-barrier-and-the-exclusion-of-nearby-proper-cycles).

### Every fixed positive offset eventually becomes linear

[Read this section in its topic note](exact-collars.md#every-fixed-positive-offset-eventually-becomes-linear).

### Five legal bit patterns and eventual vanishing of a local interaction

[Read this section in its topic note](exact-collars.md#five-legal-bit-patterns-and-eventual-vanishing-of-a-local-interaction).

## 7. Fibonacci profile renormalization and defect dynamics

[Read this section in its topic note](five-window-closure.md#7-fibonacci-profile-renormalization-and-defect-dynamics).

### First exact five-cycle certificate

[Read this section in its topic note](five-window-closure.md#first-exact-five-cycle-certificate).

## 8. Five-window closure interface

[Read this section in its topic note](five-window-closure.md#8-five-window-closure-interface).

### The exact minimum phase interface depends on the readout

[Read this section in its topic note](five-window-closure.md#the-exact-minimum-phase-interface-depends-on-the-readout).

## 9. Common closure theorem and generic minimality

[Read this section in its topic note](five-window-closure.md#9-common-closure-theorem-and-generic-minimality).

### Seed reconstruction and the remaining branch information

[Read this section in its topic note](inverse-reconstruction.md#seed-reconstruction-and-the-remaining-branch-information).

### A universal seed label from the parent defect budget

[Read this section in its topic note](inverse-reconstruction.md#a-universal-seed-label-from-the-parent-defect-budget).

### Local cycle admissibility and what it does not prove

[Read this section in its topic note](inverse-reconstruction.md#local-cycle-admissibility-and-what-it-does-not-prove).

### Minimal periodicity checks for inverse reconstruction

[Read this section in its topic note](inverse-reconstruction.md#minimal-periodicity-checks-for-inverse-reconstruction).

### A bounded gap automaton with reverse completeness

[Read this section in its topic note](inverse-reconstruction.md#a-bounded-gap-automaton-with-reverse-completeness).

### Minimum defect cost of a proper cycle

[Read this section in its topic note](inverse-reconstruction.md#minimum-defect-cost-of-a-proper-cycle).

### Recursive windows with a parameter at every row

[Read this section in its topic note](recursive-descent.md#recursive-windows-with-a-parameter-at-every-row).

### Sharing selectors at repeated physical indices

[Read this section in its topic note](recursive-descent.md#sharing-selectors-at-repeated-physical-indices).

### A shared parameter network and its forest basis

[Read this section in its topic note](recursive-descent.md#a-shared-parameter-network-and-its-forest-basis).

### Generating the layout from a sublinear shared descent code

[Read this section in its topic note](recursive-descent.md#generating-the-layout-from-a-sublinear-shared-descent-code).

### A conserved budget for multiscale inverse labels

[Read this section in its topic note](recursive-descent.md#a-conserved-budget-for-multiscale-inverse-labels).

### Seven terminal symbols and the full geometric selector code

[Read this section in its topic note](recursive-descent.md#seven-terminal-symbols-and-the-full-geometric-selector-code).

### Growing actual defects and the remaining occupation problem

[Read this section in its topic note](recursive-descent.md#growing-actual-defects-and-the-remaining-occupation-problem).

### Size-biased martingales and the four-generation dispersion criterion

[Read this section in its topic note](dispersion.md#size-biased-martingales-and-the-four-generation-dispersion-criterion).

### A phase-free lower bound from the prescribed basin

[Read this section in its topic note](dispersion.md#a-phase-free-lower-bound-from-the-prescribed-basin).

### Additive dispersion policies without orbit qualification

[Read this section in its topic note](dispersion.md#additive-dispersion-policies-without-orbit-qualification).

### Finite prefixes and exact collars do not force convergence

[Read this section in its topic note](dispersion.md#finite-prefixes-and-exact-collars-do-not-force-convergence).

### A quantitative scale-memory obstruction from Campbell's ternary law

[Read this section in its topic note](../campbell/scale-memory.md#a-quantitative-scale-memory-obstruction-from-campbells-ternary-law).

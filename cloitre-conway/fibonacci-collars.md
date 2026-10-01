# Fibonacci collars: bounded periods and exact nearby dynamics

This note derives new consequences of the [global golden-structure proof](golden-proof.md).
It uses its proved G lower bound, exact equality set and upper cap. Sections 1–4
introduce no additional finite premise. Section 6 proves a two-seed propagation
theorem and an exact wider-band corollary using 90 checked seed values.
The universal conclusions inherit the global proof's computer-assisted
foundations. No Lean formalization is claimed.
Use F_0=0, F_1=1 and alpha=1/phi.

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

The [two-collar propagation theorem](#6-exact-collars-propagate-from-two-seeds)
below strengthens the nearby dynamics: for all k>=23 the whole band
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

This theorem propagates any width whose two seeds satisfy the stated profile;
it does not prove that suitable seeds exist for every width. A fixed band still
does not control Fibonacci-block centers or settle full ratio convergence.

## 7. Fibonacci profile renormalization and defect dynamics

The collar formula has a useful two-scale form that also explains why the
first period-five orbit appears outside the certified collar. For `k>=6` and
`F_k+t>=3`, define

$$
P_k(t):=C(F_k+t)-F_{k-1},\qquad
D_k(t):=P_k(t)-\max(0,t).
$$

Let `a=F_(k-1)+s` be the selected split for `n=F_k+t`. The capture
theorem gives

$$
s\in[\min(0,t),\max(0,t)],
$$

and the complementary argument is `F_(k-2)+(t-s)`. Therefore the recurrence
itself gives the exact profile identity

$$
P_k(t)=P_{k-1}(s)+P_{k-2}(t-s). \tag{7.1}
$$

The two offsets `s` and `t-s` have the same weak sign as `t`, so the
baseline is additive. The upper cap (C <= U), together with the fact that
`U` is nondecreasing and 1-Lipschitz at every Fibonacci anchor, gives

$$
D_k(t)\le0,qquad
D_k(t)=D_{k-1}(s)+D_{k-2}(t-s). \tag{7.2}
$$

Thus a zero defect splits into two zero defects; there is no cancellation in
(7.2). This is a rigorous two-scale defect tree. It is the precise sense in
which the Fibonacci collars have a self-similar or fractal skeleton. The
selector `s` still depends on the inner orbit, so (7.1) is not a claim that
the whole sequence is generated by one finite substitution system.

The same identity gives an exact normalized branch map on the captured
interval. For `x=F_(k-1)+u`, put

$$
\Theta_{k,t}(u):=t-P_{k-1}(u).
$$

Then

$$
T_{F_k+t}(F_{k-1}+u)=F_{k-1}+\Theta_{k,t}(u). \tag{7.3}
$$

Writing `e_(k-1)(u)=-D_(k-1)(u) >= 0`, the positive arch interval becomes

$$
\Theta_{k,t}(u)=t-u+e_{k-1}(u)qquad(0\le u\le t). \tag{7.4}
$$

The collar case has `e=0`, hence pure reflection and only fixed points or
two-cycles. A cycle of period at least three must therefore visit a positive
defect. This gives a direct bridge to the Trureturing five-cycle method: the
local branch alphabet is the finite set of defect values visited by a chosen
arch, while (7.2) records how those values descend through the two Fibonacci
scales.

### First exact five-cycle certificate

The first selected period-five orbit occurs at

$$
n=196=F_{12}+52,qquad C(196)=134.
$$

Here `F_11=89`, the selected split is `a=118=F_11+29`, and the
complement is `78=F_10+23`. The profile identity is checked exactly by

$$
P_{12}(52)=45=P_{11}(29)+P_{10}(23)=26+19.
$$

The captured five-cycle, written as offsets from `F_11`, is

$$
31\to27\to28\to29\to26\to31.
$$

For the five states, the lower profile values and the normalized map are:

| `u` | `P_11(u)` | `D_11(u)` | `Theta_12,52(u)` |
|---:|---:|---:|---:|
| 31 | 25 | -6 | 27 |
| 27 | 24 | -3 | 28 |
| 28 | 23 | -5 | 29 |
| 29 | 26 | -3 | 26 |
| 26 | 21 | -5 | 31 |

The corresponding orbit in original coordinates is

$$
[120,116,117,118,115].
$$

The defect word `e=-D` along this cycle is `6,3,5,3,5`. It is a finite
local branch certificate, analogous to a closed word in the formalized
Trureturing graph, but it is not a global finite classification: through
`2^20` there are 52,828 selected period-five indices and their sorted gap
signatures are all distinct. The exact finite census and the collar proof
therefore support a local renormalization program, not a claim of universal
finite-state behavior.

This identity suggests a concrete next question. Can the defect trees arising
from arch centres be covered by finitely many certified local types, with a
reverse completeness map as in the Trureturing proof? The present theorem
settles the zero-defect collar and supplies the first nontrivial five-cycle
type; it does not yet answer that finiteness question.

## 8. Five-window closure interface

The Trureturing period-five classification suggests separating three kinds of
information when a local recursion is closed:

1. **One-scale closure:** On a positive arch the closure equations are

   ```text
   u_(i+1) = t - u_i + e_i   (i mod 5).
   ```

   Composing the five reflections gives the single closure equation

   ```text
   2*u_0 = t + e_0 - e_1 + e_2 - e_3 + e_4.
   ```

   Consequently a five-cycle can be reconstructed from `t`, one starting
   offset `u_0`, and four defects `e_0,...,e_3`: generate `u_1,...,u_4`,
   compute `e_4` from the displayed equation, and then check the five profile
   values and all branch inequalities. This is the compressed one-scale
   payload. The fifth defect and the other four offsets are consistency data,
   rather than independent closure inputs. In a black-box profile each of
   `u_0,e_0,...,e_3` can change the generated word, so this compression does
   not remove a generic input without adding a family-specific relation.

   Summing the five transition equations gives a useful centroid identity,

   ```text
   2 * (u_0 + ... + u_4) = 5*t + (e_0 + ... + e_4).
   ```

   Hence the mean offset is `t/2 + (e_0+...+e_4)/10`. The zero-defect collar
   is centered at `t/2`; every positive-defect five-cycle is shifted upward by
   exactly one tenth of its total defect. This turns the defect sum into a
   direct arch-center observable for the slow-convergence question, while the
   profile cocycle still controls how that sum descends across Fibonacci scales.

   The same calculation separates odd and even window lengths. For a reflection
   word of length `p`, composing

   ```text
   u_(i+1) = t - u_i + e_i
   ```

   gives, when `p` is odd, one scalar equation
   `2*u_0 = t + e_0 - e_1 + ... + e_(p-1)` (alternating signs), which fixes
   the starting offset once the defect word is known. When `p` is even, the
   starting offset cancels and closure instead requires the alternating defect
   sum to vanish. Thus an odd window carries a phase-bearing fixed-point
   equation, while an even window carries a translation constraint. The
   five-window interface is the `p=5` instance of this parity rule; Campbell's
   eventual period-one/two collapse is its even-window counterpart, with the
   ternary endpoint templates supplying the remaining branch data.

2. **Cross-scale closure:** five child split offsets `r_i`, giving
   `e_i = e_i^(1) + e_i^(2)` through the Fibonacci defect identity. These are
   the witnesses needed to descend the five-window to orders `k-1` and `k-2`.

3. **Selected-value closure:** certify the cycle reached from the prescribed
   start `n-1`, with actual depth `d=C(n-1)`, transient length `mu`, and
   `d>=mu`. If the first entry point has position `j` in the stored cycle,
   the selected position is `j+d-mu (mod 5)`. Ordering the cycle from its first
   entry point sets `j=0`; only in that aligned representation does `d-mu`
   alone give the stored phase. A canonical cycle needs an entry-alignment
   certificate or the already combined selected residue. One total residue
   modulo five suffices to label the selected point, once its prescribed-basin
   and phase certificate is established. Closure data alone do not establish
   that alignment or basin.

Each item has a separate role. The defects determine the normalized transition;
the child splits make the certificate inductive; and the phase connects an
arbitrary periodic cycle to the prescribed value `C(n)`. Omitting any one of
these leaves one of those three conclusions undetermined.

For the first arch, `n=196=F_12+52`, the exact payload is:

| offset `u_i` | defect `e_i` | child split `r_i` | child offsets | next offset |
|---:|---:|---:|---:|---:|
| 31 | 6 | 20 | 11 | 27 |
| 27 | 3 | 16 | 11 | 28 |
| 28 | 5 | 12 | 16 | 29 |
| 29 | 3 | 18 | 11 | 26 |
| 26 | 5 | 10 | 16 | 31 |

The child defect pairs are respectively `(5,1), (2,1), (1,4), (2,1), (1,4)`.
The selected orbit has `C(195)=131`, transient length `8`, period `5`, and
phase `131-8 = 3 (mod 5)`. This is a complete local five-window certificate,
with the displayed word starting at the first entry offset `31`, while
remaining only one local type. With the canonical cycle
`[115,120,116,117,118]`, the entry point `120` instead has position `j=1`,
and the selected position is `1+3=4 (mod 5)`, giving split `118` and
`C(196)=134`. Applying phase three directly to the canonical cycle would
select `117` and give `C(117)+C(79)=131`, the wrong value. The selector
verifier contains this exact alignment certificate.

The first three full-block audits now give a finite reverse-completeness result.
For every starting state in the three blocks, exact enumeration checks 466
functional graphs and 174,983 vertices. The block totals are:

| Fibonacci order | index range | graphs | vertices | period-five indices |
|---:|---:|---:|---:|---|
| 12 | `144..232` | 89 | 16,643 | `196` |
| 13 | `233..376` | 144 | 43,704 | `304, 307, 310, 313, 316` |
| 14 | `377..609` | 233 | 114,636 | `431, 500, 507, 513, 523, 535, 550` |

The combined cycle histogram is not treated as a global law; the exact per-block
histograms and all thirteen payloads are in the recorded JSON. In the first
block, the cycle histogram is

```text
period 1: 55    period 2: 111    period 3: 5
period 4: 5     period 5: 1
```

The unique period-five graph in the first block is the one at `n=196`, and its
payload is the table above. These are complete finite statements for the three
audited blocks, not a global finite-state claim. The [dedicated checker](verification/five_window_check.py)
now reconstructs every one of the 13 period-five words from the compressed
payload and the [recorded certificate](verification/five-window-check.json)
replays those checks from the exact evaluator. It also enumerates every legal
two-scale split with the same parent defect: 57 of the 65 public parent rows
have more than one candidate split, with a maximum of 29 candidates in one
row. The orbit-selected `r_i` is therefore an actual closure witness, not a
redundant decomposition label.

Campbell's ternary-scale formula passes the same interface with a smaller
payload. At scale `s=3^k`, parity and a low/middle/high zone determine one of
six endpoint templates for `(x_4,x_5)`; the orbit then satisfies `x_6=x_4`.
The exact dilation `b(3n)=3b(n)` replaces the two-child Fibonacci defect
descent, and the depth needs only a parity phase because the eventual period is
at most two. Thus the arithmetic changes from Fibonacci two-scale addition to
ternary homogeneity, but the closure contract is the same:

```text
scale coordinates + branch label + affine transition + closure phase
```

The recursive extension below keeps a separate parameter at every row. It
closes the representation under descent without claiming that a child word
is an autonomous lower period-five orbit. A uniform small branch alphabet and
short selected-value certificates remain open.

## 9. Common closure theorem and generic minimality

The preceding interface can be stated independently of the source recurrence.
Fix a scale coordinate `t`, a window length `p>=1`, and a defect word
`e_0,...,e_(p-1)`. Suppose the normalized offsets obey

```text
u_(i+1) = t - u_i + e_i   (i mod p).
```

Writing `A_i=t+e_i` and expanding the recurrence gives

```text
u_p = (-1)^p u_0 + sum_{i=0}^{p-1} (-1)^(p-1-i) A_i.
```

Therefore closure has exactly two parity forms:

```text
p odd:   2*u_0 = t + e_0 - e_1 + e_2 - ... + e_(p-1),
p even:  0    =     e_0 - e_1 + e_2 - ... - e_(p-1).
```

For either parity, a uniform lossless encoding is

```text
Q_p = (t, u_0, e_0, ..., e_(p-2)).
```

Generate `u_1,...,u_(p-1)` from the transition and set
`e_(p-1)=u_0+u_(p-1)-t`; the last transition then closes automatically. The
encoding has `p+1` affine coordinates including the scale and exactly `p`
additional coordinates beyond `t`. In the unrestricted black-box reflection
model these coordinates are independent: the exact symbolic feature map
`Q_p -> (t,u_0,...,u_(p-1),e_0,...,e_(p-1))` has rank `p+1`. Thus no generic
lossless affine payload can use fewer coordinates. This is a statement about
semantic closure data; integer compression or relations special to a particular
recurrence can reduce it only after additional family information is supplied.

For odd `p`, an equivalent encoding stores `t` and all `p` defects and derives
`u_0` from the fixed-point equation. For even `p`, the alternating defect
constraint is required and one offset remains as the translation phase. The
five-window payload in Section 8 is exactly
`Q_5=(t,u_0,e_0,e_1,e_2,e_3)`, with `e_4` derived. The exact check for
`p=1,...,8` is in
[`closure_interface.py`](verification/closure_interface.py), whose output
records rank `p+1` in every case.

This also isolates Campbell's apparent compression. His eventual period-one/two
orbits use the even case `p=2`, whose generic condition is `e_0=e_1` and whose
payload would be `(t,u_0,e_0)`. Campbell's parity, ternary scale and low/middle/
high endpoint template determine those coordinates within his specific family;
only the parity phase remains for the prescribed value. The six endpoint
templates therefore compress the generic `p=2` contract by a proved family
relation; they do not invalidate the rank count for a black-box reflection
window.

The Fibonacci cross-scale requirement is separate from this one-scale rank.
For each row, let `R_i` be the set of legal child splits compatible with the
parent profile value and its two lower profiles. A recursive certificate needs
one selector witness `r_i in R_i` for each window position, together with the
child-domain inequalities; the parent defects alone do not identify those
witnesses. The public three-block audit has more than one legal split in 57 of
65 parent rows, with a maximum of 29 candidates, so a parent-only selector
cannot be complete on the audited data. This is an exact finite necessity
result, not a claim that the number of selector types is globally bounded.

There is also a local product lemma. Once the parent word and the two lower
profiles are fixed, the decomposition equation for row `i` contains only
`r_i`; no `r_j` with `j!=i` occurs. Hence the complete row-local witness set is
exactly

```text
R_0 x R_1 x R_2 x R_3 x R_4.
```

This is the precise sense in which five selector positions are required at the
cross-scale interface. A future lower-window closure theorem may impose extra
relations between these choices, but those relations are additional arithmetic
information and cannot be assumed at the parent decomposition layer. The public
selector verifier enumerates all 69,064 row-local combinations and checks every
child-defect equation.

There is one exact coupling between the two lower branches that is useful for
future compression. Write `q_i=u_i-r_i` and, for a parent of order `k`, let
`t=n-F_k`. Define

```text
alpha_i = r_(i+1) + P_(k-2)(r_i)
beta_i  = q_(i+1) + P_(k-3)(q_i).
```

The Fibonacci profile identity and the parent transition give

```text
alpha_i + beta_i = t.
```

Indeed, the two profile terms sum to `P_(k-1)(u_i)`, while
`u_(i+1)=t-P_(k-1)(u_i)=r_(i+1)+q_(i+1)`. The identity is checked on all 65
public parent rows in the [selector audit](verification/selector-payload-check.json).
It means that if both lower-map parameters are recorded, one is determined by
the other and the parent scale. It does not make either `r` or `q` a lower
reflection cycle, and it is not a global nonlinear selector-compression
theorem; it is an exact row-level complement relation derived from the profile
identity.

The complement relation does not lower the affine selector budget on the public
certificate. Using one row per public period-five payload, the parent features
`(t, five offsets, five nonnegative defects, 1)` have rank `7`. Appending the
five child splits, or instead the five `alpha_i`, or the five `beta_i`, raises
the rank to `12`; appending both `alpha` and `beta` still has rank `12` because
`beta_i=t-alpha_i`. This is a finite exact diagnostic on the 13 public
payloads, so it supports five affine directions for the audited family but is
not a global lower-bound theorem.

The same conclusion holds at the exact combinatorial level for the public
row-local witness sets. Across all `69,064` elements of the audited Cartesian
products `R_0 x ... x R_4`, the map

```text
(r_0,...,r_4) |-> (r_(i+1) + P_(k-2)(r_i))_(i=0,...,4)
```

has `69,064` distinct images and maximum fiber `1`. Thus `alpha` is a lossless
reparameterization of the five selectors on the public certificate; the
complementary `beta` tuple is then recovered coordinatewise from `t-alpha`.
This is stronger than the rank check but has the same finite scope.

When the two lower profiles are already available, the numeric split `r_i` can
be represented without storing its value: sort the exact candidate set `R_i`
and store the ordinal `sigma_i` with `r_i=R_i[sigma_i]`. This is a lossless
representation of the same five selector positions, not a new mathematical
relation. The public audit shows why the candidate set must remain in the
context: 56 of its 65 individual sets are non-contiguous, so an interval
endpoint or a defect value cannot recover the selector. At `n=431` the five
candidate-set sizes are `(6,8,8,7,17)`, giving 45,696 Cartesian choices before
any cross-row restriction; a fixed-width ordinal encoding of that raw space
uses 16 bits. The [selector audit](verification/selector-payload-check.json)
records the exact rank words and separates the row-local product check from any
future constraints on the two lower five-windows. It also recovers all 65
numeric child splits from their ordinals and rechecks all 65 parent transitions,
so the ordinal representation is sufficient for the audited recursive
certificate.

### Seed reconstruction and the remaining branch information

There is a sharper inverse description once the `alpha` tuple is given. Fix
the parent word, candidate sets `R_i` and lower profiles. For a window of
length `p`, allow a profile `H_i` at each position and write

```text
alpha_i = r_(i+1) + H_i(r_i),   i mod p.
```

For C, `p=5` and every `H_i` is `P_(k-2)`. Given one seed `r_0`, the entire
word is forced by

```text
r_(i+1) = alpha_i - H_i(r_i).
```

Retain the seed exactly when each generated value belongs to the corresponding
`R_i` and the last value equals `r_0`. This gives a bijection between the
admissible seeds and the complete fiber of `alpha`. Thus an inverse search
needs at most `|R_0|` seeds, rather than `|R_0|*...*|R_(p-1)|` independent
combinations. Starting from another position gives the analogous bound, so
the fiber size is at most `min_i |R_i|`.

This identifies the exact *conditional* branch budget. If the largest fiber
in the context has size `M`, any fixed-width label that recovers the word from
`alpha` and that context needs at least `ceil(log_2 M)` bits; that many bits
suffice by storing the ordinal of the seed in the sorted admissible-seed set.
The lower bound is the pigeonhole principle, and the inverse recurrence proves
sufficiency. The candidate sets and profiles remain part of the context. This
does not reduce the five affine `alpha` coordinates to one coordinate, and it
does not prove that `M` stays bounded as the Fibonacci order grows.

Odd windows also impose a useful obstruction to collisions. Suppose two
distinct words `r` and `s` have the same `alpha`, and put

```text
delta_i = s_i-r_i,
h_i = H_i(s_i)-H_i(r_i).
```

Subtracting the two inverse recurrences gives `delta_(i+1)=-h_i`. No
`delta_i` can vanish: equality at one position forces equality at all following
positions and hence around the full window. Therefore all secants
`h_i/delta_i` are defined and nonzero, and multiplication yields

```text
product_i (h_i/delta_i) = (-1)^p.
```

For odd `p`, an odd number of these profile secants must be negative. In
particular, if every `H_i` is nondecreasing on its candidate set, `alpha` is
injective. A nontrivial odd-window fiber must cross a descending profile
branch somewhere. For even `p`, the product is positive; monotonicity alone
does not force injectivity. This distinguishes the five-window inverse from
Campbell's period-two interface, where the proved parity/domain endpoint
templates supply additional information.

More generally, suppose `R_i` is covered by `b_i` subsets on each of which
`H_i` is nondecreasing. For an odd window, fix one such subset at every
position. Two words in the same alpha fiber cannot both follow this subset
itinerary, since all their secants would then be nonnegative. Therefore each
itinerary contains at most one word and

```text
|fiber(alpha)| <= b_0 * ... * b_(p-1).
```

A branch itinerary and alpha consequently suffice for inverse reconstruction.
This is a conditional branch-cover theorem, valid for arbitrary candidate
sets; it does not assert that C has a uniform bound on the `b_i`. Finding such
profile covers would turn a family-specific branch description into a bound
on the conditional selector budget.

A compact C witness shows that a simple fixed residue is insufficient. At
`n=7739`, order `20`, the cycle offsets are `(498,512,500,503,513)`. The
complete fiber of `alpha=(605,678,576,520,518)` consists of

```text
(255,368,344,255,283)
(260,364,341,258,274).
```

Their differences are `delta=(5,-4,-3,3,-9)` and
`h=(4,3,-3,9,-5)`, with exactly one negative secant. The two seeds have the
same residue modulo `5`. Hence neither `alpha` alone nor `(alpha,r_0 mod 5)`
is a globally lossless code. One fiber ordinal bit does distinguish these two
words after this particular `alpha` and its profiles are fixed. The maintained
[selector verifier](verification/selector_payload_check.py) tests all 20 seed
candidates to establish that the displayed fiber is complete, checks both
independent sequence evaluators, and recovers the 13 public selected words by
the same seed procedure.

Nor is a uniform three-class monotone cover available. At `n=12898`, order
`21`, the candidate set for parent offset `1013` contains the increasing
splits `659,660,661,662`, with strictly decreasing lower-profile values
`599,597,595,589`. Each nondecreasing part contains at most one of these
four points. The public verifier also constructs a four-part nondecreasing
partition of the entire 18-element candidate set, so its minimum is exactly
four. This refutes a uniform three-class cover; it does not refute binary
alpha fibers, and it does not prove a uniform four-class cover.

### A universal seed label from the parent defect budget

The two-child defect identity supplies an arithmetic label without assuming
a uniform branch count. Work in a positive-offset parent context, with
nonnegative integer parent defects `e_i`, and require every `r_i in R_i` to
satisfy

```text
lambda_i(r_i) = r_i-H_i(r_i),   0 <= lambda_i(r_i) <= e_i.
```

For C these inequalities follow from (7.2): the two nonnegative child
defects add to `e_i`, and `lambda_i` is the first child's defect. The inverse
transition can therefore be written

```text
r_(i+1) = alpha_i-r_i+lambda_i(r_i).
```

For odd `p`, alternating summation around a closed word gives

```text
2*r_0 = A + sum_i (-1)^i lambda_i(r_i),
A = sum_i (-1)^i alpha_i.
```

Indeed, the coefficients of `r_1,...,r_(p-1)` cancel in the alternating
sum of `r_i+r_(i+1)=alpha_i+lambda_i`; the coefficient of `r_0` is two.
For `p=5`, every admissible seed lies in the explicit integer interval

$$
L=\left\lceil\frac{A-e_1-e_3}{2}\right\rceil,
\qquad
U=\left\lfloor\frac{A+e_0+e_2+e_4}{2}\right\rfloor. \tag{9.1}
$$

Put `E=sum_i e_i` and `B=floor(E/2)+1`. The unrounded interval has length
`E/2`, so `U-L<=floor(E/2)=B-1`. Consequently **alpha and `r_0 mod B`
recover the entire word**, relative to the same parent, candidate and profile
context. This is a universal sufficient label, with at most `ceil(log_2 B)`
bits. It is adaptive to the given defects, rather than a fixed modulus inferred
from a finite search.

For a residue `0<=zeta<B`, there is at most one compatible seed in the interval.
Compute it directly as

```text
r_0 = L + ((zeta-L) mod B).
```

Reject when this exceeds `U`, fails candidate membership, or fails any of the
forced transitions or final closure. Otherwise this recovers the unique
compatible word. Rotating the window gives an interval `[L_j,U_j]` for each
`r_j`. In particular, for a fixed alpha,

```text
|fiber(alpha)| <= min(B, min_j |R_j intersect [L_j,U_j]|).
```

The exact conditional minimum remains the logarithm of the actual fiber
maximum, as proved above. `B` can be larger. At `n=7739` the parent defects are
`(36,38,29,42,37)`, `E=182`, and `A=501`. Formula (9.1) gives `[211,301]`
and `B=92`; it distinguishes seeds 255 and 260, whereas one fiber ordinal
bit suffices for that particular two-word fiber. The public verifier checks
the interval on all 69,064 public Cartesian words and decodes the 13 selected
words and both higher-order witnesses.

There is also a defect-based branch cover. Partition `R_i` by the integer
`floor(lambda_i(r)/2)`. If `r<s` lie in the same part, the two defects differ
by at most one, and

```text
H_i(s)-H_i(r) = (s-r)-(lambda_i(s)-lambda_i(r)) >= 0.
```

Thus `b_i<=floor(e_i/2)+1` nondecreasing parts suffice. Combined with the
earlier branch theorem, this gives the additional bound
`|fiber(alpha)|<=product_i (floor(e_i/2)+1)`. In particular, if every
`e_i<=1`, an odd-window alpha has at most one preimage: no branch label is
needed. This does not bound these budgets uniformly in the Fibonacci order.

The bound `B` is sharp in the abstract interface with position-dependent
profiles and no other family restrictions. For any integer `m>=1`, take
every `R_i={m,...,2m}`, `H_0(r)=2m-r`, and `H_i(r)=r` for `i=1,...,4`.
Use `e=(2m,0,0,0,0)` and `alpha=(2m,3m,3m,3m,3m)`. Its complete fiber is

```text
(m+d, m+d, 2m-d, m+d, 2m-d),   d=0,...,m.
```

All profiles are nonnegative on their domains, all defect boxes hold, and
there are exactly `m+1=B` seeds. This proves optimality for that abstract
defect-box information; it is not an example from C's common lower profile
or from a genuine C parent cycle.

For even `p`, the seed cancels from alternating summation, so this interval
argument is unavailable. For example, with `p=2`, `H_0(r)=H_1(r)=r`,
`e=(0,0)`, both candidate sets `{0,...,t}`, and `alpha=(t,t)`, the fiber is
`{(r,t-r):0<=r<=t}`. It has `t+1` elements despite zero defects. Campbell's
proved period-two endpoint templates supply the family information that a
zero defect budget alone cannot provide.

The Fibonacci collar supplies an exact restricted-context corollary. For
`k>=25` and candidate sets `R_i` contained in `{0,...,32}`, the collar formula
gives `H_i=P_(k-2)=identity`. Alpha then uniquely determines any admissible
odd-window word. The restriction on every candidate set is essential; this
does not show that all witnesses for an arch-centre word lie in the collar.

The remaining family question is now precise: can the defect or descending
branch budgets be controlled across Fibonacci orders, or can the actual
orbit-selected words be characterized by a stronger inverse condition?
The proved adaptive label need not have bounded size, and finite singleton
selected fibers do not establish uniform uniqueness or recursive closure.

### Local cycle admissibility and what it does not prove

The row-local decomposition equation is weaker than the defining recurrence's
orbit requirement. In the positive-offset setting, put
`m_i=F_(k-1)+u_i`, with `k>=7`. For the lower profile `H=P_(k-2)`, normalize
the row's own inner map as

```text
T_(m_i)(F_(k-2)+r) = F_(k-2) + Psi_i(r),
Psi_i(r) = u_i-H(r).
```

The cap gives `0<=H(r)<=r` for nonnegative offsets, so `[0,u_i]` is invariant.
The cycle-capture theorem places every cycle in this interval. Define

```text
R_i^per = {r in R_i : Psi_i^q(r)=r for some integer q>=1}.
```

The cycle-entry theorem proves that the actual selected split at `m_i` belongs
to `R_i^per`. Thus replacing each `R_i` by `R_i^per` loses no actual selector
word. For any alpha, the refined fiber is exactly the original fiber with all
nonperiodic coordinates excluded. The seed reconstruction and defect-budget
theorems continue to apply to the smaller candidate sets. This is a necessary
domain restriction, not an extra phase label. Computing it requires the lower
profile on the entire captured interval, rather than only at candidate points.

This distinction matters in the n=7739 counterexample. Its two seeds have
normalized first-row trajectories

```text
255 -> 261 -> 250 -> 264 -> 246 -> 261 -> ...
260 -> 257 -> 258 -> 252 -> 257 -> ...
```

Both seeds are transient. Hence neither complete word in the displayed
two-word fiber is locally cycle-admissible, and that particular alpha has an
empty refined fiber. The verifier checks every coordinate against an
independent full-domain cycle enumeration, preserves the actual selected word,
and applies the refinement to the 13 public five-window payloads. Their
periodic Cartesian domains contain 137 words instead of 69,064 row-local words.
This does not turn the earlier row-local counterexample into an ambiguity of
the actual selected recurrence word.

Periodicity alone still cannot establish alpha injectivity for arbitrary
profiles, even when the profile is shared across all positions and the parent
is a proper five-cycle. Here is an explicit abstract counterexample. Take
`t=100` and the following parent offsets, defects and two-child splits:

| `u_i` | `e_i=u_i+u_(i+1)-100` | `r_i` | `q_i=u_i-r_i` |
|---|---|---|---|
| 60 | 26 | 35 | 25 |
| 66 | 38 | 43 | 23 |
| 72 | 50 | 55 | 17 |
| 78 | 62 | 65 | 13 |
| 84 | 44 | 50 | 34 |

Set the parent profile at these offsets to `P(u_i)=u_i-e_i`; then
`100-P(u_i)=u_(i+1)` cycles through all five distinct offsets. Extend `P`
by identity elsewhere on `{0,...,100}`. Define two shared child profiles by
identity except for these overrides:

```text
H(r_i)=q_i,            H(r_i+1)=q_i-1,
K(q_i)=r_i-e_i,        K(q_i-1)=r_i+1-e_i.
```

Within each profile the override domains are disjoint. Every profile value
lies between zero and its argument. Both `r_i` and `r_i+1` are fixed points
of `Psi_i=u_i-H`, and both decompositions have the same parent value:

```text
H(r_i)+K(q_i) = H(r_i+1)+K(q_i-1) = u_i-e_i.
```

Nevertheless the two distinct locally periodic words

```text
(35,43,55,65,50)
(36,44,56,66,51)
```

have the same `alpha=(68,78,82,63,69)`. The verifier recovers their complete
two-word refined fiber. This is a counterexample within the abstract profile
interface, not within C. It proves that shared profiles, nonnegative child
defects, a parent five-cycle and local periodicity do not together guarantee
a zero-bit inverse branch budget. An injectivity theorem for C must use an
additional property of its recursively generated profiles.

There is a further necessary restriction: the row split must belong to the
terminal cycle reached from the prescribed start `m_i-1`, not just any cycle
of `Psi_i`. Once that terminal cycle is known with its first entry point as
phase zero, the exact selected point is specified by the lower row's depth
and its transient length, or equivalently by a depth-past-transient certificate
and one residue modulo that row's period. For a canonical cycle, include its
entry alignment in the total selected residue as in Section 8.
These are separate lower-row phases. A five-cycle of the parent does not make
its child cycles period five. This is the same distinction between cycle,
basin and selected phase that Campbell's endpoint templates resolve in his
period-one/two family.

### Minimal periodicity checks for inverse reconstruction

The number of necessary orbit qualifications can be smaller than the number
of rows. Fix the parent context, candidate sets R_i and profiles, and let
`A(r)_i=r_(i+1)+H_i(r_i)` be the alpha map on the raw product R. Write
`P(r)={i:r_i in R_i^per}`. For a set of tested positions S, retain

```text
R(S) = {r in R : S is a subset of P(r)}.
```

Every actual selector word lies in R(S), for every S, by cycle entry. There
are two different inverse claims:

1. **Injectivity after the tests.** Alpha is injective on R(S) exactly when,
   for every distinct raw pair r,s with A(r)=A(s),
   `S` is not a subset of `P(r) intersect P(s)`.
2. **Uniqueness even against raw candidates.** Every word retained in R(S)
   has a singleton raw alpha fiber exactly when, for every raw collision
   word r, `S` is not a subset of P(r).

The first equivalence says that at least one member of every collision pair
must fail a tested qualification. The second says that every collision word
must fail one. These are necessary and sufficient conditions, not estimates:
their failure directly supplies the retained ambiguous pair or the retained
word with a raw competitor. The minimum number of tested positions is thus
the minimum hitting-set size for the complements of the corresponding masks.
It can be zero in an already injective context, or no set can suffice in a
context with locally periodic collisions, such as the abstract example above.

In particular, one **adaptive pivot** j suffices for the first claim when
no raw collision pair has both j-th coordinates periodic. It suffices for
the second, stronger claim when no raw collision word has its j-th coordinate
periodic. Under either certificate, alpha has at most one inverse in the
qualified domain, so no residual inverse branch bit is needed there. Decode
by rotating the seed reconstruction to the pivot, trying its qualified seeds,
and checking the remaining candidate memberships and closure.

This counts orbit qualifications, not the full payload dimension, the cost of
finding the pivot, or the size of its lower-profile certificate. The pivot
may depend on the parent context. If a decoder needs it explicitly, supply
its position or a deterministic rule with a verified exclusion certificate.
Prescribed basin and selected phase remain additional tasks; a qualified
decomposition witness is not automatically the recurrence's selected word.

Two exact C contexts demonstrate that this distinction matters. Positions
below are zero-based, with the parent cycle starting at its smallest offset.

| Parent index | Canonical cycle offsets | Minimum tests for qualified injectivity | Minimum tests for raw uniqueness |
|---:|---|---|---|
| 11342 | `(197,202,201,198,206)` | one: position 3 or 4 | one: position 3 |
| 28996 | `(166,174,169,170,173)` | one: position 1 | two: positions 1 and 3 |

The first raw product has 9,939,375 words and 279 nontrivial alpha fibers;
the second has 27,264,384 words and 5,472 nontrivial fibers. All those fibers
are binary. The [selector verifier](verification/selector_payload_check.py)
enumerates them by the exact paired difference equations
`delta_(i+1)=-(H_i(s_i)-H_i(r_i))`, checks each full fiber again by seed
reconstruction, and independently verifies periodic candidate membership
against all-start lower functional graphs. It also checks preservation of
the actual selector word and replays every listed optimal qualification set.

At n=28996 the two raw words

```text
(57,49,48,20,76)
(58,47,47,21,75)
```

have equal alpha `(105,94,68,96,133)`. Both are periodic at positions
0,2,3,4 and transient at position 1. Thus checking those four other positions
still leaves a collision; the second row is necessary. The full fiber audit
proves that this row alone suffices for qualified injectivity. It does not
suffice for raw uniqueness: the alpha `(81,113,133,98,113)` has raw words
`(57,25,88,45,56)` and `(58,23,90,43,55)`, of which the first is periodic
at position 1 and the second is not. The qualification retains just one,
although its raw competitor still exists. Two tested rows, 1 and 3, are
necessary and sufficient for the stronger claim in this context.

The two contexts also rule out any universal **fixed** single pivot for
qualified injectivity: their admissible single-pivot sets `{3,4}` and `{1}`
are disjoint. This does not rule out a context-dependent pivot for C, and
does not claim ambiguity at an actually selected alpha tuple. Proving a
uniform adaptive qualification bound from the recursive Fibonacci profiles
remains open. Campbell's endpoint templates determine his basin and phase
from the arithmetic family; here the missing family theorem is now separated
from the exact conditional inverse test.

### A bounded gap automaton with reverse completeness

The collision test has an exact quotient that does not enumerate alpha fibers.
For a finite window of length p, define a directed relation at position i:

```text
d -> v   if there are r,s in R_i with
d=s-r != 0 and v=H_i(r)-H_i(s) != 0.
```

**Gap theorem.** There is a nontrivial alpha collision exactly when these p
relations admit a closed layered walk `d_0 -> ... -> d_p=d_0`.

**Proof.** A collision gives differences `d_i=s_i-r_i`. If one difference
were zero, its alpha equation would force the next to be zero, and repeating
around the window would make the two words equal. Thus every difference is
nonzero. Subtracting the alpha equations gives
`d_(i+1)=H_i(r_i)-H_i(s_i)`, hence the walk.
Conversely, choose an ordered witness pair `(r_i,s_i)` independently for each
edge of a closed walk. The paired differences then satisfy

```text
s_(i+1)-r_(i+1) = H_i(r_i)-H_i(s_i).
```

Thus `s_(i+1)+H_i(s_i)=r_(i+1)+H_i(r_i)` at every position, including the
closing edge. The chosen words have equal alpha and distinct coordinates.
This proves reverse completeness; the quotient creates no false collisions.
It uses the raw Cartesian candidate context. Additional cross-row constraints
would have to be incorporated before applying the reverse implication. QED.

For odd p under the defect boxes, put `E=sum(e_i)` and `D=floor(E/2)`.
The rotated seed intervals (9.1) contain both seeds of any collision and have
diameter at most D. Therefore every collision satisfies `0<|d_i|<=D`.
Keep only the common signed-gap alphabet

```text
G = {-D,...,-1,1,...,D}.
```

There are at most 2D gap states per layer, independently of the number of
Cartesian words. Restricting both ends of every edge to G preserves every
collision. On this alphabet form the Boolean transfer matrices M_i. The
alpha map is injective exactly when the product `M_0*...*M_(p-1)` has empty
diagonal, with matrix multiplication over the Boolean semiring. When D=0
there are no nonzero gap states and the inverse is already unique.

The minimum-qualification criteria above can be checked on the same graph:

- At a tested position, require **both** edge-witness coordinates to be
  periodic to test injectivity after qualifications.
- Require only the **first** coordinate to be periodic to test whether any
  retained word still has a raw competitor. Signed gaps keep track of which
  word is marked; this relation need not be symmetric under `d -> -d`.

The corresponding product must have empty diagonal. Testing the 32 subsets
of a five-window gives the exact minimum without computing the raw fibers.
The graph tests all alpha images simultaneously; it does not by itself decode
a specified alpha. After certification, use the seed reconstruction. Its
state bound and the profile/periodicity data remain context-dependent, so
this is not a global finite alphabet for C.

This is the reusable reverse-completeness step of the Trureturing period-five
classification: obtain exact legal edges and prove that every closed code
reconstructs the object being tested. Here the object is a collision pair,
and the alphabet consists of signed integer differences, rather than the
three global Tribonacci gap types. No identity between the two systems is
assumed. In an identity profile every edge is `d -> -d`: odd length cannot
close at a nonzero gap, while even length can. The zero-defect even-window
example therefore still requires family information, which Campbell's
endpoint templates provide in his recurrence.

For n=28996, the parent defect word is `(1,4,0,4,0)`, so E=9, D=4 and G
has only eight states. The five raw relations have 16,12,8,10,8 edges,
representing all 27,264,384 raw words and their possible alpha collisions.
There is also a short hand check of its optimal single qualified row:

1. The periodic candidates in row 1 are `(17,24,25)`. Under the gap bound
   D=4 only 24 and 25 can form a distinct qualified pair, so `d_1=+/-1`
   and `d_2=-d_1`.
2. Row 2 has zero defect, giving `d_3=-d_2=d_1`. At unit gap row 3 also
   has exactly the transition `d_4=-d_3=-d_1`.
3. Row 4 has zero defect, hence `d_0=-d_4=d_1`. Row 0 has defect at most
   one; its profile is nondecreasing on the candidates, and its nonzero
   output gap has the opposite sign from d_0. It cannot equal d_1=d_0.

Thus no qualified closed gap walk exists. Every small relation and the
periodic candidate set used here is checked in the maintained verifier.
The raw graph does have closed walks, and the reverse procedure reconstructs
their collision words. At n=11342 the same construction uses 28 signed states.
Both gap-based minima agree with the independent complete-fiber certificates.

### Minimum defect cost of a proper cycle

There is a further universal restriction on the parent budget. Let
`u_0,...,u_(p-1)` be distinct integers forming a reflection-defect cycle
`u_(i+1)=t-u_i+e_i`, with `e_i>=0` and p>=3. Then

$$
E=\sum_i e_i\ge p. \tag{9.2}
$$

For odd p and even t, E is even and the stronger bound is E>=p+1.
These bounds are sharp among capped integer profiles. In particular a proper
five-cycle needs E>=5, or E>=6 at even offset t. Its mean offset is at least
`t/2+1/2`, and at even t at least `t/2+3/5`, by the centroid identity.
The statement excludes periods one and two, which can have zero defects.

**Proof.** Sort the vertices as `v_1<...<v_p`. For every
`1<=j<=floor((p-1)/2)`, one must have

$$
v_j+v_{p-j}\ge t. \tag{9.3}
$$

Otherwise the lowest j vertices have all their cycle neighbours in the
highest j vertices. The former require 2j incidences; these use the entire
degree-two capacity of the latter, separating their union from the nonempty
middle set. This contradicts the connected proper cycle.

Put `y_j=2*v_j-t`. The y's are distinct integers of the same parity, separated
by at least two, and `E=sum(y_j)`. If p=2m+1, the m inequalities (9.3) pair
all y's except y_p into nonnegative sums. The middle pair has nonnegative
sum and unequal entries, so `y_(m+1)>=1`. Consequently
`E>=y_p>=1+2m=p`. If p=2m, m>=2, (9.3) instead leaves y_m and y_p unpaired.
Its last inequality and `y_(m-1)<=y_m-2` imply `y_(m+1)>=2-y_m`, so
`E>=y_m+y_p>=2+2(m-1)=p`. Finally `E=2*sum(v_j)-p*t` gives the parity
refinement for odd p. QED.

For sharpness choose t large enough, and set the centred cycle offsets
`z_i=2*u_i-t`. For odd p and odd t use
`(1,-1,3,-3,...,p-2,-(p-2),p)`; its total defect is p. For odd p and even t
use `(-(p-1),p-1,-(p-3),p-3,...,-2,2,p+1)`, with total p+1. For even p and
odd t use `(-(p-1),p-1,-(p-3),p-3,...,-1,p+1)`, with total p; for even t
subtract one from its negative entries and add one to its positive entries.
At each vertex set `H(u_i)=t-u_(i+1)` and use H(u)=u elsewhere. These give
nonnegative capped profiles and proper cycles of the stated cost. They are
abstract constructions, not instances of C.

The verifier checks these sharp constructions for p=3,...,12 and both offset
parities, and corroborates (9.2) on 13,505 selected C cycles through n=28996.
C itself attains E=p at n=68: t=13, cycle offsets `(9,6,8,5)` and defects
`(2,1,0,1)`. The defect-cost theorem constrains primitive cycle types and their
centroids; it does not bound E across Fibonacci orders or prove full ratio
convergence.

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

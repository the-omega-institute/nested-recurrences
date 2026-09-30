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
first period-five orbit appears outside the certified collar. For every
admissible `t`, define

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

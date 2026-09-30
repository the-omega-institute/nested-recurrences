# Fibonacci collars: bounded periods and exact nearby dynamics

This note derives new consequences of the [global golden-structure proof](golden-proof.md).
It uses its proved G lower bound, exact equality set and upper cap; it does not
introduce an additional finite premise. Thus its universal conclusions inherit
that proof's computer-assisted foundations. No Lean formalization is claimed.
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

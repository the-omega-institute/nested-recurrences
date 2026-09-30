# Global golden structure: lower bound, exact equality set and Fibonacci landing

The variable-depth recurrence proposed by Benoît Cloitre satisfies the following
global statements, with F_0=0,F_1=1 and alpha=1/phi=(sqrt(5)-1)/2:

1. C(n)>=G(n)=floor(alpha(n+1)) for every n>=1.
2. Its equality set is exactly

   $$
   Z=\{F_j,F_j+1:j\ge2\}
     \cup\{F_j-1:j\ge3\text{ odd}\}\cup\{11,24,25,59\}.
   $$

3. If F_j<=n<F_(j+1), j>=3, then

   $$
   C(n)\le U(n):=\min(n-F_{j-2},F_j).
   $$

   Set U(1)=1. This formula also gives U(2)=1.
4. C(F_j)=F_(j-1) for j>=2; C(F_j-1)=F_(j-1) for j>=5; and
   C(F_j+1)=F_(j-1)+1 for j>=3.
5. At n=F_k, k>=6, **every** orbit of T_n(x)=n-C(x) on [1,n-1]
   eventually reaches the fixed point F_(k-1). In particular, the prescribed
   variable depth selects that fixed point.
6. liminf C(n)/n=alpha.

The proof combines general induction with explicit finite premises:
the seed bound on [16384,131071] and the induction base on [1,65535].
It is a **computer-assisted proof**. Both finite premises are checked from
the recurrence with two independent evaluators; they are not conjectural
inputs. This is not a Lean formalization. A full limit, a decay exponent and
the universal shifted-family assertions are not established by this proof.

[Research overview](../README.md) · [Earlier results](proof.md) ·
[Landing development](landing.md) · [Finite certificate](golden-check.json)

## 1. Established inputs and the finite premises

Use the exact recurrence and indexing of [the original proof](proof.md):
C(1)=C(2)=1, x_0=n-1, x_(i+1)=n-C(x_i), d=C(n-1), g=x_d,
and C(n)=C(g)+C(n-g) for n>=3.

The earlier proof establishes totality, 3n/5<=C(n)<=3n/4 for n>=3,
and that the prescribed depth reaches a cycle. Its finite-window propagation
lemma, with the exact seed certificate on [16384,131071], gives

$$
C(m)\le\frac{15225}{22877}m<\frac23m\qquad(m\ge16384),
$$

where 3*15225=45675<45754=2*22877.

Write E(n)=C(n)-G(n). Direct computation supplies

$$
E(n)\ge0,\qquad E(n)=0\Longrightarrow n\in Z
\qquad(1\le n<65536).
$$

There are 57 zero-defect indices in this base. Their exact list, the seed
extrema and the evaluator hashes are recorded in [golden-check.json](golden-check.json).
The [checker](golden_check.py) generates C independently by full-orbit and
Brent evaluation through 131071, and also checks literal nesting through 4096.

No golden-ratio, zero-set or Fibonacci conjecture is used in these computations.

For completeness, the floor expression is Hofstadter's G-sequence globally,
not just a finite comparison. Set G(0)=0 and, for n>=1, write
k=floor(alpha n), rho={alpha n}. Then

$$
\alpha(k+1)=n-k+\alpha-(1+\alpha)\rho.
$$

The final term has floor zero when rho<alpha^2=1-alpha and floor -1 when
rho>alpha^2, while floor(rho+alpha) is respectively zero or one.
Equality rho=alpha^2 is impossible because it would make alpha(n+1) an
integer. Therefore G(G(n-1))=n-G(n), proving the defining recurrence
G(n)=n-G(G(n-1)). Its earlier-index evaluation determines it uniquely.

## 2. A universal restriction on the selected split

**Lemma.** For n>=65536, the prescribed split a=g,b=n-g satisfies

$$
\frac59n<a<\frac23n,\qquad\frac54<\frac ab<2.
$$

**Proof.** Every cycle point x has a cycle predecessor y<n, and
x=n-C(y)>n/4 by the global three-quarter bound. Thus all cycle indices
are at least 16384, and the strict two-thirds upper bound applies there.
If u and v are the smallest and largest cycle points, respectively, then

$$
u>n-\tfrac23v,\qquad v\le n-\tfrac35u.
$$

Combining them gives u>n/3+(2/5)u, hence u>5n/9 and then v<2n/3.
The selected point is on the cycle by the established cycle-entry theorem,
so the same bounds hold for a. The ratio bounds follow by b=n-a. QED.

In particular, both split arguments exceed 21845. The four exceptional
members 11,24,25,59 of Z and the small Fibonacci coincidences cannot occur
as zero-defect split arguments in this induction range.

## 3. An exact Fibonacci rotation lemma

The identity alpha F_j-F_(j-1)=(-1)^(j-1)alpha^j and Cassini's identity
give the following elementary best-approximation statement.

**Lemma.** For j>=3, 0<t<F_j, and any integer s,

$$
|\alpha t-s|\ge\alpha^{j-1}.
$$

Equality is possible only at (t,s)=(F_(j-1),F_(j-2)).

**Proof.** The two vectors (F_j,F_(j-1)) and (F_(j-1),F_(j-2))
have determinant +1 or -1. Write the integer vector (t,s) uniquely as
u(F_j,F_(j-1))+v(F_(j-1),F_(j-2)). Then

$$
\alpha t-s=(-1)^{j-1}\alpha^{j-1}(u\alpha-v).
$$

If u>=1, the condition t<F_j forces v<=-1, so |u alpha-v|>1.
If u<=-1, positivity of t forces v>=1, giving the same strict inequality.
If u=0, then v>=1 and the absolute value is v. Equality requires v=1. QED.

**One-sided consequence.** If j>=5 is odd, then among the integers
0<t<F_(j+2),

$$
\{\alpha t\}\ge1-\alpha^j
\quad\Longleftrightarrow\quad t=F_{j+1}.
$$

**Proof.** For 0<t<F_(j+1), apply the lemma at order j+1. A fractional
part at least 1-alpha^j would have distance at most alpha^j from the next
integer. The equality case of the lemma is t=F_j with integer F_(j-1),
but alpha F_j=F_(j-1)+alpha^j approaches that integer from above, not below.
Thus there is no such t in this range.

At t=F_(j+1) the fractional part is 1-alpha^(j+1), which qualifies.
For F_(j+1)<t<F_(j+2), write t=F_(j+1)+w with 0<w<F_j. The lemma gives
alpha^(j-1)<= {alpha w} <=1-alpha^(j-1). Subtracting alpha^(j+1)
does not wrap around zero and leaves a fractional part at most
1-alpha^(j-1)-alpha^(j+1)<1-alpha^j. QED.

## 4. Simultaneous induction: G lower bound and zero-set containment

Recall [the exact carry formula](landing.md#1-the-carry-has-three-possible-values):

$$
E(n)=E(a)+E(b)+\delta(a,b),\qquad
\delta=-\lfloor r(a)+r(b)-\alpha\rfloor\in\{-1,0,1\},
\qquad r(m)=\{\alpha(m+1)\}.
$$

The [infinite candidate-set arithmetic lemma](landing.md#2-an-infinite-arithmetic-lemma-for-the-candidate-equality-set)
already proves delta(a,b)>=0 for a,b in Z except (2,2).

We prove simultaneously that E(n)>=0 and E(n)=0 implies n in Z.
The finite base covers n<65536. At a later index, both smaller defects are
nonnegative and every smaller zero-defect index belongs to Z.

**Both defects positive.** Then E(n)>=1, so both assertions follow.

**Exactly one defect zero.** The other is an integer e>=1, hence E(n)>=0.
Equality requires e=1 and delta=-1, or r(a)+r(b)>=1+alpha.

Since the other fractional part is less than one, this negative carry forces
the zero argument z to satisfy r(z)>alpha. For a large z in Z, the only
such possibility is z=F_j with
j odd. Indeed even Fibonacci indices have r=alpha-alpha^j; Fibonacci-plus-one
indices have r<=4alpha-2<alpha; and the allowed minus-one indices have
r=alpha^j<alpha. The four exceptions have r<alpha and are already excluded
by the split bounds. Thus the zero argument must be F_j with j odd and
r(F_j)=alpha+alpha^j. The other argument w must satisfy

$$
\{\alpha(w+1)\}\ge1-\alpha^j.
$$

If the zero argument is a, then w=b<a=F_j, so w+1<=F_j and the
one-sided rotation lemma makes this impossible. If the zero argument is b,
then a<2b=2F_j, whence a+1<=2F_j<F_(j+2). The same lemma forces
a+1=F_(j+1). Consequently n=F_(j+2)-1, an allowed odd minus-one index in Z.

**Both defects zero.** Then a,b belong to Z. The ratio restriction
5/4<a/b<2 forces their nearest Fibonacci anchors to be consecutive.
To justify this, if they had the same anchor Q, their ratio would be at most
(Q+1)/(Q-1)<5/4. If their anchors differed by two or more, their ratio would
be at least (F_(j+2)-1)/(F_j+1)>2, since F_(j-1)>3 here.
Thus write

$$
a=F_{j+1}+s,\qquad b=F_j+t,
$$

with offsets s,t in {-1,0,1}, where -1 is allowed only at an odd anchor.
Both offsets cannot be -1, since consecutive orders have opposite parity.
The sum is n=F_(j+2)+s+t. The carry is nonnegative by the arithmetic lemma,
so E(n)>=0. To analyze equality, consider the possible offsets:

- s+t=0 or 1 gives n in Z.
- s+t=2 means s=t=1. The fractional-part sum is
  4alpha-2+(-1)^(j-1)alpha^(j+2)<alpha, so delta=1 and there is no equality.
  Here 4alpha-2=alpha-alpha^4 and j is large.
- s+t=-1 is in Z when j is odd. If j is even, only s=-1,t=0 is allowed;
  the fractional-part sum is alpha^(j+1)+alpha-alpha^j
  =alpha-alpha^(j+2)<alpha, again giving delta=1.

Thus equality again implies n in Z. This completes the simultaneous strong
induction: **C>=G globally, and every equality index belongs to Z.**

## 5. Cycle capture from a Fibonacci anchor

We next prove the upper cap U by strong induction. Its elementary definition
makes U nondecreasing and 1-Lipschitz on the positive integers:

$$
0\le U(x+1)-U(x)\le1.
$$

Within each Fibonacci block the slope is one and then zero; the boundary to
the next block is continuous, with the small initial values U(1),...,U(7)
equal to 1,1,2,3,3,4,5.

Fix a Fibonacci anchor A=F_j>=5 and B=F_(j-1)=U(A)=G(A).
The preceding lower-bound and containment theorem implies, whenever x<A,

$$
C(x)\ge B-(A-x)+1.
$$

For d=A-x>=2 this follows directly from
G(A-d)>=B-d+1: subtracting the integer B-d+1 from alpha(A-d+1)
gives alpha^2(d-1)+(-1)^(j-1)alpha^j>0.
For d=1, an odd j gives G(A-1)=B. An even j>=6 gives G(A-1)=B-1,
but A-1 is outside Z, so its defect is at least one and C(A-1)>=B.
The exceptional j=4 anchor A=3 is not used.

Assume C(x)<=U(x) for all x<n. For any x in the domain [1,n-1], the
monotonicity and Lipschitz property of U, together with the lower bound, yield

| Position | Bounds on C(x) |
|---|---|
| x<A | B+x-A+1 <= C(x) <= B |
| x>=A | B <= C(x) <= B+x-A |

**Cycle-capture lemma.** Every cycle of T_n lies between A and n-B,
including the endpoints. The anchor A itself need not lie in the domain;
the inequalities are required only for the actual arguments x<n.

**Proof.** Put D=n-B-A. If D>=0, the interval I=[A,A+D] is invariant.
A point x=A-d below I maps into [A+D,A+D+d-1], so its distance from I
decreases by at least one. A point x=A+D+d above I maps into [A-d,A+D],
so its distance does not increase, and any image still outside I is below it.
Therefore the distance decreases within every two steps outside I.

If D<=0, use I=[A+D,A]. A point x=A+D-d below I maps into
[A+D,A+d-1], reducing the distance by at least one. A point x=A+d above I
maps into [A+D-d,A+D], never increasing the distance and moving to the lower
side if it remains outside. The same strict decrease within two steps follows.
For points inside either interval, the table shows that their images stay
inside. A cycle therefore cannot have any point outside I. QED.

## 6. The upper cap, Fibonacci identities and the full equality set

The initial cases n<=7 satisfy C(n)<=U(n). Suppose n>=8 and write
q=F_j<=n<F_(j+1)=q+p, with p=F_(j-1) and r=F_(j-2).
Both anchors q>=8 and p>=5 are eligible for the capture lemma. Applying it
at (A,B)=(q,p) and (p,r), respectively, places every cycle point in

$$
[n-p,q]\cap[p,n-r].
$$

The selected split a is on a cycle, so

$$
p\le a\le q,\qquad r\le b=n-a\le p.
$$

The inductive upper bounds in the two consecutive blocks give

$$
C(a)\le\min(a-F_{j-3},p),\qquad
C(b)\le\min(b-F_{j-4},r).
$$

These formulas hold at both block endpoints as well. Adding, and using
F_(j-3)+F_(j-4)=r and p+r=q, proves

$$
C(n)\le\min(n-r,q)=U(n).
$$

This completes the upper-cap induction. Its dependencies are only the
already proved lower bound and zero-set containment, the earlier cycle-entry
theorem, and smaller upper-cap values.

At a Fibonacci index F_j, G(F_j)=U(F_j)=F_(j-1), proving the Fibonacci identity.
For j>=5, the predecessor has U(F_j-1)=F_(j-1) and the strict lower cone above
gives the matching lower bound. At F_j+1, j>=3, the floor formula and the cap
both give F_(j-1)+1; the small j=3 case can also be read directly.

Thus all Fibonacci and plus-one indices in Z are equal to G, as are all
odd minus-one indices. The small overlaps at 1 and 2 are checked directly,
and the finite base verifies equality at 11,24,25,59. Combined with Section 4's
containment, this proves **the exact equality set Z**.

For n=F_k, k>=6, take A=F_(k-1)>=5 and B=F_(k-2). Now n-B=A,
so the capture interval is a single point. Every orbit therefore reaches
that fixed point; its being fixed also follows from C(A)=B.

The earlier neighborhood conditions are now consequences of the proved bounds.
For any Fibonacci q=F_j>=5, p=F_(j-1), and positive t,

$$
0\le C(q+t)-p\le t.
$$

For 1<=t<q,

$$
-t+1\le C(q-t)-p\le0.
$$

Thus the negative side is strictly contracted, ruling out all saturated
symmetric two-cycles. These inequalities hold throughout the indicated domains,
not just in the smaller neighborhoods originally sampled.

Finally, C>=G gives liminf C(n)/n>=alpha, while the established Fibonacci
subsequence has C(F_j)/F_j=F_(j-1)/F_j tending to alpha. Hence

$$
\liminf_{n\to\infty}\frac{C(n)}n=\frac1\phi.
$$

Convergence of the entire ratio would additionally require limsup<=alpha.
The existing certified limsup upper bound and the slow-decay observations do
not yet establish that step.

## 7. Reproduction and proof dependency order

From the repository's main folder:

```sh
python3 cloitre-conway/golden_check.py
python3 scripts/verify.py
```

The first command verifies the finite premises and additional diagnostic
checks of all cycle points through 131071. The second replays the committed
basic evidence, including this certificate. The optional `--extended` flag
also replays the earlier F_36 exploration.

The logical order is: established totality/bounds/cycle entry; exact seed and
induction base; split restriction and rotation lemma; simultaneous lower-bound
and zero-containment induction; upper-cap induction; identities, reverse
zero-set inclusion, global Fibonacci landing and the liminf corollary.
The larger F_36 experiment is useful corroboration, but is not a premise of
the universal proof.

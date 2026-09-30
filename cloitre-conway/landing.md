# Fibonacci landing: corrected induction and two conditional reductions

**Completed continuation:** [Global golden structure](golden-proof.md) now
discharges the hypotheses of the reductions below. It proves C>=G, the exact
equality set, Fibonacci identities and landing, the neighborhood bounds, and
liminf C(n)/n=1/phi. This note records the intermediate stage and its independent
numerical audit. Its remaining-conjecture labels for those completed claims are
historical; full convergence and decay rates remain open.

This note develops Benoît Cloitre's proposed Fibonacci-orbit and zero-defect
approach. The identities and reductions proved below are unconditional
mathematical statements, but their application to all terms of C still has
explicit hypotheses to establish. They do **not** prove the universal
Fibonacci identity, C>=G, or a limiting ratio.

[Research overview](../README.md) · [Earlier proofs](proof.md) · [Status](../STATUS.md)

## 1. The carry has three possible values

Put alpha=1/phi=(sqrt(5)-1)/2 and G(n)=floor(alpha(n+1)). Write

$$
E(n)=C(n)-G(n),\qquad r(n)=\{\alpha(n+1)\}.
$$

For any positive a,b, with n=a+b,

$$
\delta(a,b)=G(a)+G(b)-G(n)
          =-\lfloor r(a)+r(b)-\alpha\rfloor\in\{-1,0,1\}.
$$

Indeed alpha(a+b+1)=alpha(a+1)+alpha(b+1)-alpha; separating the
integer and fractional parts gives the formula. More precisely,

| Condition on r(a)+r(b) | delta |
|---|---:|
| Less than alpha | +1 |
| At least alpha and less than 1+alpha | 0 |
| At least 1+alpha | -1 |

The positive carry occurs in the actual recurrence: at n=7 the selected split
is 4+3, and G(4)+G(3)-G(7)=3+2-4=1. Both summands have zero defect, while
E(7)=1. Thus a landing statement demanding delta=0 whenever an argument has
zero defect and n is outside the candidate equality set would be false.

For the **actual selected split** a=g,b=n-g the exact defect identity is

$$
E(n)=E(a)+E(b)+\delta(a,b).
$$

Assume the smaller defects are nonnegative integers. This gives a complete
local classification:

- If both are positive, then E(n)>=1.
- If exactly one is zero and the other is e>=1, then E(n)>=0. Equality holds
  precisely when e=1 and delta=-1.
- If both are zero, then E(n)=delta: a negative value is possible only for
  delta=-1, and equality requires delta=0.

In particular, merely showing "delta=-1 implies n belongs to Z" would not
complete the proposed invariant. One also needs the nonzero defect to equal
one in the one-zero case, and must establish equality at every intended index.

## 2. An infinite arithmetic lemma for the candidate equality set

Use F_0=0,F_1=1 and define the set proposed from the finite data by

$$
Z=\{F_j,F_j+1:j\ge2\}
 \cup\{F_j-1:j\ge3\text{ odd}\}\cup\{11,24,25,59\}.
$$

**Proposition.** For every a,b in Z,

$$
G(a)+G(b)\ge G(a+b),
$$

except a=b=2, where 1+1<3. This is an infinite-set statement, independent of
any conjecture about the values of C.

**Proof.** The Fibonacci identity

$$
\alpha F_j=F_{j-1}+(-1)^{j-1}\alpha^j
$$

follows by induction from alpha^2=1-alpha. Set beta=alpha+alpha^5=6alpha-3.
We show

$$
r(2)=3\alpha-1,\qquad 0<r(z)\le\beta\quad(z\in Z\setminus\{2\}).
$$

For z=F_j with j>=4, the displayed identity gives
r(z)=alpha+(-1)^(j-1)alpha^j. The largest positive correction occurs at j=5,
so r(z)<=beta. The remaining z=F_2=1 has r(1)=2alpha-1<=beta;
F_3=2 is the distinguished exception.

For z=F_j+1 with j>=3,
r(z)=2alpha-1+(-1)^(j-1)alpha^j, which lies strictly between zero and one.
It is at most 2alpha-1+alpha^3=4alpha-2<beta. The case j=2 again gives z=2.
For z=F_j-1 with odd j>=3, r(z)=alpha^j<=alpha^3<beta.

The four remaining indices have fractional parts

| z | r(z) |
|---:|---|
| 11 | 12alpha-7 |
| 24 | 25alpha-15 |
| 25 | 26alpha-16 |
| 59 | 60alpha-37 |

Each is positive and at most beta. These are direct exact comparisons in
Q(sqrt(5)); for the upper comparisons it suffices to use 3/5<alpha<5/8.

If neither argument is 2, then r(a)+r(b)<=2beta<1+alpha, since
11alpha<7. If exactly one is 2, then the sum is at most
beta+3alpha-1=9alpha-4<1+alpha, since 8alpha<5.
The carry formula therefore gives delta>=0 in both cases. For a=b=2,
the sum 6alpha-2 exceeds 1+alpha, since 5alpha>3, giving delta=-1. QED.

**Conditional lower-bound theorem.** If every zero-defect index of C belongs
to Z, then C(n)>=G(n) for every positive n.

**Proof.** Suppose n is the first counterexample. The initial terms n=1,2
are equal to G, and C(4)=3=G(4). Both smaller split defects are nonnegative.
If either is positive, Section 1 gives E(n)>=0. Otherwise both split indices
belong to Z by hypothesis, so the proposition again gives E(n)>=0 unless
both are 2. That would force n=4, already excluded. QED.

This reduction needs only **containment** of the zero set in Z, not equality
at every member of Z. The containment remains an open dynamical problem.
The result replaces the earlier finite check of all zero-index pairs with an
infinite arithmetic proof for the candidate set.

## 3. A precise sufficient condition for the Fibonacci basin

Fix k>=6. Write q=F_(k-1), p=F_(k-2), R=F_(k-4), and define

$$
h(t)=C(q+t)-p\qquad(-R\le t\le R).
$$

At n=F_k=q+p, the orbit's signed distance t=x-q transforms as

$$
t\longmapsto-h(t).
$$

**Conditional basin theorem.** Suppose

1. C(F_k-1)=q, C(F_(k-2))=F_(k-3), and C(q)=p;
2. for each 1<=t<=R, 0<=h(t)<=t and -t<=h(-t)<=0;
3. there is no t in [1,R] for which h(t)=t and h(-t)=-t both hold.

Then the starting orbit at F_k reaches q, and C(F_k)=F_(k-1).

**Proof.** The first three distances are p-1, -F_(k-3), R, by hypothesis 1.
After the third point, hypothesis 2 keeps the distances in [-R,R], reverses
their weak sign and never increases their absolute value. If a nonzero
absolute value stays unchanged for two consecutive steps, the corresponding
positive and negative distances form exactly the two-cycle forbidden by
hypothesis 3. Thus absolute value decreases by at least one within every two
steps, until it reaches zero. Hypothesis 1 makes zero a fixed point.

The earlier cycle-entry theorem says the prescribed depth C(F_k-1) reaches
the eventual cycle, so the **selected** split is q, not merely some earlier
transient point. Consequently C(F_k)=C(q)+C(p)=p+F_(k-3)=q. QED.

This proves a finite termination criterion, not a logarithmic bound on the
number of orbit steps. Its elementary estimate is at most 2R steps after
the third point.

The predecessor identity C(F_k-1)=q is a separate hypothesis. For even k,
F_k-1 is not in Z and the proposed zero-set invariant alone only gives a lower
bound there; it does not supply this exact value.

There is a useful simplification of hypothesis 3. Put j=k-1>=5. For t>=2,

$$
G(F_j-t)\ge F_{j-1}-t+1.
$$

To see this, subtract the right integer from alpha(F_j-t+1). The result is
(1-alpha)(t-1)+(-1)^(j-1)alpha^j>0, since alpha^2>alpha^j.
Taking the floor proves the inequality. If the earlier G lower bound is
available, it gives h(-t)>=-t+1 for t>=2. The separate neighbor identity
C(q-1)=p gives h(-1)=0. Together these exclude all the symmetric two-cycles.
The remaining substantive task is to prove the neighborhood inequalities
and predecessor identities simultaneously without assuming the desired result.

## 4. Reproducible finite audit

The [audit program](landing_audit.py) computes C using a compact integer array,
checks its first 2^20 terms against a separate Brent implementation and the
previously recorded sequence hash, and examines every Fibonacci neighborhood
specified in Section 3 within the requested range. The detailed output is
[landing-audit.json](landing-audit.json).

The recorded full run gives:

- C>=G and the candidate equality set agree at every index through
  F_36=14,930,352, with exactly 86 equality indices. This remains finite evidence.
- For every 6<=k<=36, the first three distances have the claimed values, the
  nonzero distances alternate in sign, their absolute values do not increase,
  and the orbit ends at the Fibonacci fixed point. The k=20 trajectory is
  2583,-1597,987,-862,368,-350,92,-89,14,-14,1,-1,0. At k=36 it takes 18 steps
  to reach the fixed point.
- Every integer in all 31 neighborhoods in Section 3 satisfies its two
  inequalities and no forbidden symmetric two-cycle occurs. This checks the
  whole neighborhoods, not just the observed orbit points.
- Among selected splits for 3<=n<=2^20, delta=-1,0,+1 occur 75,779,
  772,058 and 200,737 times respectively. The one-zero, negative-carry cases
  occur exactly at F_j-1 for odd 7<=j<=29; there are 12. In each case the other
  defect is exactly one and the resulting defect is zero. There is no
  two-zero, negative-carry case in the checked range.

It also tests the three shifted variants with (L,D)=(2,2),(2,1),(1,2), explicitly
using a(1)=a(2)=1 and starting the recurrence at n=3. Each has an independent
literal 4096-term check. Other shifts require an initial-value convention;
the general assertion about nearly every D is not covered by this audit.
All three named variants satisfy their proposed side of G and Fibonacci
anchors through 2^20. No asymptotic conclusion follows from that finite check.

For the arch samples, [OEIS A022388](https://oeis.org/A022388) uses offset zero,
initial values 6,13, and the Fibonacci recurrence. The program rounds A(m)/5
exactly as floor((A(m)+2)/5); there are no half-integer ties. Its scaled
logarithmic quantities are floating-point observations, not proof certificates.

For 21<=m<=33, the computed quantity
(C(n)/n-alpha)(log_2 n)^(1/4) ranges from **0.0859630664 to 0.0892896999**.
Seven of the 13 samples fall outside 0.087 times [0.995,1.005]. In particular,
m=23 gives A(m)=478807, n=95761, C(n)=63423, and the scaled value
0.0892896999, about **2.632%** above 0.087. This sample is inside the prefix
checked against the independent Brent evaluator. Thus the claimed 0.5%
stability is not reproduced under the stated indexing and rounding.

The half-power scaled values do rise overall, from 0.1696200967 to
0.1916332692, but not monotonically: m=26 gives 0.1848345581 and m=27 gives
0.1827695559. These corrections do not disprove a quarter-power asymptotic;
they remove the stated numerical precision as evidence for it. Checking a
single point in each arch also supplies no bound on all the intervening terms.

There is also an indexing/rounding distinction. With k=m+2, the exact formula is

$$
\frac{A(m)}5
=F_k+\frac{F_{k-1}}{\sqrt5}
 +\frac25\left(-\frac1\phi\right)^{k-1}.
$$

This follows from A(m)=6F_(m+2)+F_m=5F_k+L_(k-1), where L denotes the
Lucas numbers. The unrounded expression differs from the proposed arch
location exponentially little. Rounding adds a bounded error, at most 2/5,
which need not decay. Neither version implies that the sampled point is the
maximum of its arch.

To reproduce the full audit from the repository's main folder:

```sh
python3 cloitre-conway/landing_audit.py --output replay-landing.json
```

The defaults reach F_36=14,930,352 for C and 2^20 for the selected-split audit
and each shifted variant. The smaller command below is useful while developing;
its output is a different, shorter experiment and will not match the full report.

```sh
python3 cloitre-conway/landing_audit.py --limit 1048576 --output small-landing.json
```

Run without Python optimization flags. All limit, decay-rate, universal
Fibonacci and family-side assertions remain conjectural unless a separate
proof is supplied.

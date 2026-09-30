# Cloitre's variable-depth Conway recurrence: foundations

Research date: 2026-09-30, Asia/Singapore. This is a research note, not a
manuscript, priority claim, or Lean formalization. The candidate and original
G/Fibonacci observations are due to Benoît Cloitre, proposed during joint
research discussions in September 2026. The results below concern that exact
candidate, separately from Campbell's already evaluated b-sequence.

**Latest theorem:** [Global golden structure](golden-proof.md) proves C>=G,
the exact equality set, Fibonacci identities and global landing at Fibonacci
indices, a Fibonacci-block upper cap, and liminf C(n)/n=1/phi. The finite premises
are separately certified; the universal argument is an induction and cycle
capture. This note supplies the foundational arguments used there.
The [supporting arithmetic and audit](landing.md) supplies the carry lemma
and the larger F36 audit, including the decay precision correction.

## Definition and result status

Set C(1)=C(2)=1. For n>=3, define

$$
x_0=n-1,\qquad x_{j+1}=T_n(x_j)=n-C(x_j),\qquad
d=C(n-1),\qquad g=x_d,\qquad C(n)=C(g)+C(n-g).
$$

The starting value is x_0, not the first iterate. The two arguments are g and
n-g, and there are exactly d applications of T_n.

Results established here:

1. This defines a unique sequence at every positive integer. For n>=2,
   ceil(n/2)<=C(n)<=n-1; for n>=3, C(n)>=2.
2. For every n>=3, 3n/5<=C(n)<=3n/4. Both constants are attained, at n=5 and
   n=4 respectively. This is an elementary induction with a displayed finite
   initial table.
3. For n>=4 the selected arguments satisfy
   g>=ceil((n+3)/4) and n-g>=ceil((n+3)/8).
4. A finite seed window [M,8M-1] propagates both ratio bounds to every n>=M.
   Exact computation of that window therefore proves, for all n>=131072,
   121393/196418 <= C(n)/n <= 103088/155677 < 2/3.
   This is a computer-assisted theorem: the propagation proof is general,
   while the initial inequalities are verified by finite integer computation.
5. At every n>=3 the chosen depth d is at least the preperiod of the starting
   orbit. The proof uses the elementary bounds and a small initial check.

The assertions C(n)>=G(n), C(F_k)=F_(k-1), and the exact equality set below
are proved in the [global golden-structure note](golden-proof.md).
The statement that every equality C(n)=G(n) is a Fibonacci number or an
immediate neighbor is false: n=11,24,25,59 are counterexamples.

## 1. Global well-definedness and the half bound

Assume the already defined prefix satisfies 1<=C(m)<=m, with the stronger
C(m)<=m-1 for m>=2. Then for 1<=x<n,

$$
1\le n-C(x)\le n-1.
$$

Consequently every finite iterate uses only earlier values. The depth C(n-1)
is a positive integer, g is in [1,n-1], and both summands are defined. If a=g
and b=n-g, at least one of a,b is >=2. Using C(1)=1 and the stronger bound on
that summand gives C(a)+C(b)<=a+b-1=n-1. Both summands are positive, so C(n)>=2.
The initial cases C(1)=C(2)=1 complete strong induction and uniqueness.

For the lower bound, C(1)>=1/2 and C(2)=2/2. Inductively,
C(n)=C(a)+C(b)>=a/2+b/2=n/2. Integrality gives ceil(n/2).

The endpoint C(1)=1 must be treated separately: the inequality C(m)<=m-1 is
false there. Complementary arguments alone do not establish totality without
first proving that the inner orbit stays in the previously defined prefix.

For n>=3, T_n actually maps [1,n-1] into [2,n-1]. Indeed T_n(1)=n-1>=2;
for x>=2, T_n(x)>=n-x+1>=2. All orbit points used below are therefore >=2.

## 2. The uniform upper bound and split separation

**Proposition.** C(n)<=3n/4 for n>=2.

The values C(2),...,C(5)=1,2,3,3 give the initial cases. Suppose n>=6 and the
bound holds at every earlier index >=2. For every point of the starting orbit,

$$
x_{j+1}=n-C(x_j)\ge n-\tfrac34(n-1)=\tfrac{n+3}{4}.
$$

Thus x_j>=3 for j>=1. The depth is d=C(n-1)>=2. Hence g=x_d>=3 and
n-g=C(x_(d-1))>=2. Both summands now have indices >=2, so

$$
C(n)=C(g)+C(n-g)\le \tfrac34g+\tfrac34(n-g)=\tfrac34n.
$$

This proves the proposition without assuming any Fibonacci identity.

**Split lemma.** For all n>=4,

$$
g\ge\left\lceil\frac{n+3}{4}\right\rceil,\qquad
n-g\ge\left\lceil\frac{n+3}{8}\right\rceil.
$$

The first inequality is the orbit estimate just proved, now using the global
upper bound. Since d>=2, it also applies to x_(d-1). The half bound gives
n-g=C(x_(d-1))>=x_(d-1)/2>=(n+3)/8. Integrality finishes the proof. In
particular, both selected arguments are at least ceil((n+3)/8).

## 3. Finite-window propagation and explicit infinite bounds

**Propagation lemma.** Let M>=1 be an integer. If real constants L,U satisfy

$$
Lm\le C(m)\le Um\qquad(M\le m\le8M-1),
$$

then the same bounds hold at every m>=M.

**Proof.** The given window supplies the initial cases. At n>=8M, the split
lemma places both g and n-g in [M,n-1]. Strong induction gives

$$
Ln=L g+L(n-g)\le C(g)+C(n-g)\le U g+U(n-g)=Un.
$$

The split lemma applies because n>=8. QED.

For M=3 the exact values C(3),...,C(23) are

```
2,3,3,4,5,5,6,7,7,8,8,9,10,11,12,12,13,13,13,14,15.
```

They satisfy C(m)>=3m/5, and therefore this lower bound holds for every m>=3.
Together with Section 2 this proves the sharp elementary bounds stated above.

The larger seed windows were generated from the recurrence, without a guessed
formula, and checked by integer cross multiplication. Selected certificates:

| M | Last seed index | Minimum C(m)/m | Maximum C(m)/m |
|---:|---:|---:|---:|
| 32 | 255 | 21/34 | 16/23 |
| 128 | 1023 | 144/233 | 127/185 |
| 2048 | 16383 | 2584/4181 | 466/693 |
| 16384 | 131071 | 17711/28657 | 15225/22877 |
| 32768 | 262143 | 46368/75025 | 39071/58812 |
| 131072 | 1048575 | 121393/196418 | 103088/155677 |

Each row supplies bounds for **all** n>=M, not just its finite seed interval.
For the last row the extremizing indices are respectively 196418 and 155677,
with C-values 121393 and 103088. Numerically the resulting bounds are

$$
0.6180339887383030\ldots\le C(n)/n\le0.6621915889951631\ldots
\quad(n\ge131072).
$$

In particular, liminf C(n)/n is at least the left rational and limsup C(n)/n
is at most the right rational. The lower rational is approximately
1.1592e-11 below 1/phi. This gap is nonzero; it does not prove the golden-ratio
conjecture. The upper rational is strictly less than 2/3 because
3*103088=309264 < 311354=2*155677.

## 4. The actual depth always reaches the cycle

Let mu_n be the preperiod and lambda_n the period of the orbit starting at
x_0=n-1, with x_(mu+lambda)=x_mu and all earlier listed points distinct.

The half and three-quarter bounds imply, for n>=4,

$$
x_j\ge n/4\ (j\ge1),\qquad
x_j\le7n/8\ (j\ge2),\qquad
x_j\ge11n/32\ (j\ge3).
$$

Thus every point from x_3 onward lies in the integer interval
[ceil(11n/32),floor(7n/8)], of cardinality at most 17n/32+1. Since the first
mu_n+lambda_n orbit points are distinct,

$$
\mu_n+\lambda_n\le17n/32+4,\qquad
\mu_n\le17n/32+3.
$$

For n>=53, Section 3 gives

$$
d=C(n-1)\ge3(n-1)/5\ge17n/32+3\ge\mu_n.
$$

The remaining indices 3<=n<=52 are checked directly. Their exact depths and
preperiods are recorded in `conway-results.json`, field `small_orbit_checks`.
For 3<=n<=8, (d,mu) is (1,0),(2,0),(3,0),(3,1),(4,3),(5,4).
For 9<=n<=13 it is (5,2),(6,2),(7,3),(7,5),(8,6).
For 14<=n<=20, the minimum depth is 8 and the maximum preperiod is 6.
For 21<=n<=52, the minimum depth is 13 and the maximum preperiod is 9.
These exact small checks complete the proof for every n>=3.

Consequently the actual selected split is always

$$
g=x_{\mu_n+((C(n-1)-\mu_n)\bmod\lambda_n)}.
$$

This proves that the depth selects a cycle phase. It does not prove unbounded
cycle lengths, a growth exponent, or a small universal preperiod bound.

## 5. Independent reproduction and corrections

The code uses three evaluators:

- A dictionary of first visits computes each full orbit and reduces the depth
  by its exact preperiod and period.
- A separately implemented Brent cycle detector generates its own sequence
  from C(1)=C(2)=1; it agrees term by term through 1,048,576.
- A literal evaluator performs all 5,467,850 requested nested steps through
  n=4096, without cycle reduction; it agrees term by term.

The supplied 30-term prefix is reproduced exactly. G is independently
generated by G(0)=0, G(n)=n-G(G(n-1)), and checked against
floor((n+1)/phi) using integer square roots, not floating point.

For precisely the intervals 2^(k-1)<n<=2^k:

| Interval | Max period | Mean period | Max preperiod | Share with period >2 |
|---|---:|---:|---:|---:|
| (32,64] | 2 | 1.656250000 | 9 | 0% |
| (512,1024] | 10 | 2.152343750 | 25 | 19.3359375% |
| (8192,16384] | 26 | 3.984619141 | 69 | 52.8686523% |
| (131072,262144] | 71 | 7.750679016 | 142 | 73.3139038% |
| (524288,1048576] | 106 | 10.712249756 | 211 | 79.6014786% |

Benoît's reported maximum periods and preperiods agree. The originally reported first mean
was 1.64; for the stated half-open interval it is exactly 53/32=1.65625.
The last of his displayed ratio maxima is exactly 103088/155677, approximately
0.662192, rather than approximately 0.663. These are reporting corrections,
not a different recurrence.

At n=220663, the orbit has mu=39, lambda=71, depth=143466, selected split
134063, and C(n)=143408. At n=964361, mu=37, lambda=106, depth=630491,
selected split 584152, and C(n)=630561. Full trajectories are in the JSON.

The first differences through 2^17 have minimum -195 and maximum +188, as
reported. The supplied Grytczuk recurrence agrees through n=18 and first
differs at n=19: this C gives 13 and that recurrence gives 12.

There are exactly 62 indices with C(n)=G(n) through 2^17, also as reported.
However, four of them are not a Fibonacci number or an immediate neighbor:

| n | C(n)=G(n) | Selected split | Summands |
|---:|---:|---:|---:|
| 11 | 7 | 6+5 | 4+3 |
| 24 | 15 | 13+11 | 8+7 |
| 25 | 16 | 13+12 | 8+8 |
| 59 | 37 | 34+25 | 21+16 |

All four are within the independently checked literal prefix. Through 2^20
there are 72 equality indices, and their set is exactly the truncation of

$$
\{F_k,F_k+1:k\ge2\}\ \cup\
\{F_k-1:k\ge3\text{ odd}\}\ \cup\ \{11,24,25,59\},
$$

with F_0=0,F_1=1. The [global proof](golden-proof.md) establishes this exact
infinite description.
C(n)>=G(n) has no failure through 2^20, and C(F_k)=F_(k-1) holds for
2<=k<=30 (F_30=832040). The k=1 identity would be false under F_0=0.

## 6. Supporting pair inequality and subsequent proofs

For all a,b in [1,2^20], the finite data satisfy

$$
C(a)+C(b)\ge G(a+b),
$$

apart from a=b=2, where the values are 2 and 3. This covers sums up to 2^21
without generating C at those sums. To verify it efficiently, set
E(a)=C(a)-G(a). The floor formula implies
G(a)+G(b)>=G(a+b)-1. Since the finite prefix has E>=0, a failure requires
E(a)=E(b)=0. It suffices to check the 2628 unordered pairs among the 72 zero
indices; only (2,2) fails. The floor formula at a+b is evaluated exactly.

The infinite arithmetic lemma in [the supporting note](landing.md#2-an-infinite-arithmetic-lemma-for-the-candidate-equality-set)
replaces this finite pair check in the global argument. The simultaneous
induction and cycle-capture theorem in [the global proof](golden-proof.md)
establish the exact zero set and Fibonacci landing. Existence of a Fibonacci
fixed point alone would not establish landing; cycle capture supplies that step.

Full ratio convergence, decay rates and growth of periods remain open.
The [collar theorem](fibonacci-collars.md) gives local control near Fibonacci
indices but does not settle the behavior in the centers of the arches.

The bibliographic identity of the cited Grytczuk paper was checked via
Crossref: *Another variation on Conway's recursive sequence*, DOI
10.1016/j.disc.2003.10.022. Its full text and the novelty of the present
propagation argument have not been audited; no priority claim is made.

## Reproduction

From this directory, run with Python 3 and its standard library:

```
python3 verification/conway_explore.py --output replay.json
```

The default limit is 2^20 and the literal limit is 4096. The script records its
own SHA-256 and the SHA-256 of the comma-separated C(1),...,C(2^20). The latter
is `a2fcf614a04054ea43f76155940b933d0613a077012ae74c6b8d9a8a3aa5ed8b`.
The exact ratio extrema use integer cross multiplication. Floating-point
values in the descriptive orbit table are never used to certify a bound.

AI assistance was used for exploration, proof development, implementation and
writing. The verification described here consists of written arguments and
exact computations; no Lean formalization is claimed.

Run without Python's `-O` option or `PYTHONOPTIMIZE`, since assertions perform
the mathematical checks. The repository-wide `scripts/verify.py` also checks
that fresh results match the committed evidence.

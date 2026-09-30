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

3. **Selected-value closure:** the actual depth `d=C(n-1)` and transient
   length `mu`, with the certificate `d >= mu`. The phase is then derived as
   `d-mu (mod 5)`, so it is not a third independent payload entry. If the full
   depth is not stored, the equivalent compressed certificate is `d >= mu`
   together with the one residue `d-mu (mod 5)`. Either encoding identifies
   which point of a closed five-cycle is selected by the defining recurrence.

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
while remaining only one local type.

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

The next bounded C result should enumerate all period-five words in one arch
window using this payload and prove a reverse completeness map. No global finite
alphabet is claimed yet.

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

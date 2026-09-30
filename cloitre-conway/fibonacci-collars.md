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

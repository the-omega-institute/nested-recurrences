# Inverse reconstruction and cycle qualification

[Project home](../README.md) · [Research map](README.md#technical-research-map)

This note reconstructs candidate cycles from the
[reflection-window interface](five-window-closure.md). It separates the
branch-label budget from profile qualification, then gives a bounded-gap
graph and reverse-completeness proof. A geometric certificate does not by
itself certify the actual prescribed-start basin.

## Contents

- [Seed reconstruction and the remaining branch information](#seed-reconstruction-and-the-remaining-branch-information)
- [Golden-defect words give a uniform cyclic decoder](#golden-defect-words-give-a-uniform-cyclic-decoder)
- [A universal seed label from the parent defect budget](#a-universal-seed-label-from-the-parent-defect-budget)
- [Local cycle admissibility and what it does not prove](#local-cycle-admissibility-and-what-it-does-not-prove)
- [Minimal periodicity checks for inverse reconstruction](#minimal-periodicity-checks-for-inverse-reconstruction)
- [A bounded gap automaton with reverse completeness](#a-bounded-gap-automaton-with-reverse-completeness)
- [Minimum defect cost of a proper cycle](#minimum-defect-cost-of-a-proper-cycle)

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

### Golden-defect words give a uniform cyclic decoder

There is a different supplied-data interface that avoids searching a whole
lower profile. Write a scalar value as G(z)+d, where d is its golden defect.
If the ordered defect at each row is supplied, the unknown index occurs
only inside the monotone golden floor. For a five-window this makes the
cyclic inverse unique, regardless of the size of the defects. The defect
integers themselves and their actual-C qualification remain resources.

**Cyclic decoder theorem.** Set eta=1/phi and extend only the diagnostic
floor to integers by

$$
\widehat G(z)=\lfloor\eta(z+1)\rfloor\quad(z\in\mathbb Z).
$$

It agrees with G at positive indices; this extension does not define C at
nonpositive indices. Given an ordered integer word c_0,...,c_(ell-1),
consider closed integer words

$$
z_{i+1}=c_i-\widehat G(z_i),\qquad z_\ell=z_0. \tag{G.1}
$$

In any declared finite interval for z_0:

- If ell is odd, there is at most one closed word: zero residual seed bits.
- If ell is even, there are at most three closed words. Their initial
  indices lie in three consecutive integers, so at most two residual
  seed bits suffice before further qualification.
- All raw candidates can be found with O(ell log(W+2)) golden-floor
  evaluations, where W is the width of the initial interval. Candidate
  membership, actual values, proper period, basin and phase are then checked.

Arbitrary candidate sets at later rows can only remove words. These are
conditional numeric inverse bounds, not a minimum total payload theorem.

**Proof.** Every map z->c_i-Ghat(z) is nonincreasing and 1-Lipschitz on
integers. For a separation delta>=3,

$$
|\widehat G(z+\delta)-\widehat G(z)|
\le\lceil\eta\delta\rceil\le\delta-1, \tag{G.2}
$$

because eta<2/3. Thus a cyclic pair of solutions cannot start at distance
at least3: its distance shrinks at the first step and cannot increase
afterward. At odd ell the composite map F is nonincreasing, and two
distinct fixed points would reverse their own strict order, which is
impossible. At even ell, F is nondecreasing and 1-Lipschitz; hence F(z)-z
is nonincreasing. Its zero set is an integer interval, and (G.2) limits
that interval to at most three integers. The same difference is strictly
decreasing at odd ell. Binary search for its first nonpositive value,
test equality, and test at most the next two seeds. Each composite
evaluation uses ell floor operations. Signed provisional indices are
allowed during this search; the declared positive row domains are checked
on the resulting words, not assumed during a bisection trial. QED.

**Application to the actual child inverse.** Use the existing profile
definition P(r)=C(L+r)-B, not the natural defect P(r)-r. More generally
allow supplied row anchors L_i,B_i and parameters

$$
\alpha_i=r_{i+1}+C(L_i+r_i)-B_i.
$$

Supply the ordered golden-defect word
d_i=C(L_i+r_i)-G(L_i+r_i). With z_i=L_i+r_i, its physical inverse is

$$
z_{i+1}=L_{i+1}+\alpha_i+B_i-d_i-G(z_i). \tag{G.3}
$$

This is (G.1). In particular every five-row child inverse has at most one
numeric solution given alpha, the anchor words and d. No branch ordinal,
profile-cover itinerary or large defect-dependent seed residue is needed
in this supplied-data model. The higher-order alpha collision above has
different ordered golden-defect words for its two solutions; each decodes
uniquely once its own word is supplied.
Explicitly, its common physical anchor is L=2584 and baseline B=1597;
the two ordered words are (79,106,108,79,88) and (80,112,107,86,89).
Their separation concerns the row-local inverses: the earlier periodicity
check still excludes both as actual selected child words.

After reconstruction, verify row candidate membership, the actual equation
C(z_i)=G(z_i)+d_i, complementary scalar sums, repeated physical-index
consistency and selected validity. A wrong supplied defect word can produce
a perfectly closed geometric candidate. This decoder does not certify
that the candidate is the actual prescribed split.

**Application to an inner orbit and its phase readout.** For a fixed root N
and a proposed ordered orbit-defect word d_i=C(x_i)-G(x_i), put c_i=N-d_i.
Equation (G.1) reconstructs its orbit positions. An odd orbit-defect word
therefore fixes the numeric starting phase whenever it is feasible. On
every proper odd cycle, the golden-defect trace has the full cycle period:
a nontrivial rotation preserving that trace would give a second starting
point solving the same ordered inverse, contradicting uniqueness.

For a proper five-cycle at least two defect values occur. The existing
[cyclic-readout refinement bound](five-window-closure.md#the-exact-minimum-phase-interface-depends-on-the-readout)
then distinguishes its five phases after at most three additional defect
observations, that is, a block of at most four consecutive observations.
The observations require actual scalar values. This conditional phase
diagnostic does not identify the prescribed entrance or provide those
observations from five digit labels alone.

The four-observation bound is attained by an actual cycle at N=513:
its canonical positions are (306,309,307,308,311), and its golden-defect
trace is (15,15,15,12,15). Two starting phases have the same first three
observations (15,15,15); all five blocks of four observations are distinct.
Thus three observations cannot always replace four in this readout model.

**Even sharpness and Campbell.** At N=5 both actual C and Campbell's b have
the common earlier values (1,1,2,3)=G(1),...,G(4). The length-two defect
word (0,0) admits exactly the closed words (2,4),(3,3),(4,2) in1..4.
Thus the even three-candidate bound and two-bit worst-case label are sharp
in the stated raw cyclic model. If proper period2 is supplied, only the
first and last remain, requiring one phase bit. Campbell's actual start4
and depth b(4)=3 select2. Its complete ternary templates supply that
selection; the golden word alone does not. See the
[cross-family comparison](../campbell/scale-memory.md#golden-defect-words-and-the-period-two-interface).

**Information and validation contract.** The decoder uses only the golden
floor to reconstruct coordinates, replacing full lower-profile lookup by
the supplied point-defect word. It does not construct or prove that word.
For a five-row problem with input magnitudes bounded by O(N), ordinary
integer registers and the supplied integer words use O(log N) bits; this
is distinct from the smaller working-bit modular selector that assumes
read-only tables. The defects can grow, and autonomous recognition,
table construction, actual basin/phase certification and the total minimum
recursive interface remain separate questions.

The [checker](verification/selector_payload_check.py) independently compares
bisection with exhaustive signed-index search, decodes all69064 public
row-local child combinations, verifies the higher-order collision with its
two different defect words, and reconstructs actual selected cycles from
an independently evaluated prefix. All-start small-block cycles additionally
check the odd phase-period conclusion and proper five-cycle observation
bound. The infinite bounds follow from monotonicity and (G.2), not from
extrapolating the finite census.

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
entry alignment in the total selected residue as in the [closure interface](five-window-closure.md#8-five-window-closure-interface).
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

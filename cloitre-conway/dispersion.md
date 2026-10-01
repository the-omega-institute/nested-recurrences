# Martingales, dispersion, and the open limit question

[Project home](../README.md) · [Research map](README.md#technical-research-map)

This note proves the martingale identities and the conditional route from
four-generation dispersion to an upper decay rate. It then develops basin
lower envelopes and scalar-valid policies. Uniform dispersion remains open.
Explicit nonconvergent extensions show why golden bounds, finite prefixes,
and exact collars alone cannot prove the actual limit.
Prerequisites: [global golden structure](golden-proof.md) and the
[profile identity](five-window-closure.md#7-fibonacci-profile-renormalization-and-defect-dynamics).

## Contents

- [Size-biased martingales and the four-generation dispersion criterion](#size-biased-martingales-and-the-four-generation-dispersion-criterion)
- [A phase-free lower bound from the prescribed basin](#a-phase-free-lower-bound-from-the-prescribed-basin)
- [Quadratic basin dispersion in the unit-defect family](#quadratic-basin-dispersion-in-the-unit-defect-family)
- [Cap-adaptive quadratic dispersion](#cap-adaptive-quadratic-dispersion)
- [A logarithmic horizon from one retained child](#a-logarithmic-horizon-from-one-retained-child)
- [Diophantine dispersion in cube-root Fibonacci neighborhoods](#diophantine-dispersion-in-cube-root-fibonacci-neighborhoods)
- [Additive dispersion policies without orbit qualification](#additive-dispersion-policies-without-orbit-qualification)
- [Two-split moment policies and cycle-average dispersion](#two-split-moment-policies-and-cycle-average-dispersion)
- [Finite prefixes and exact collars do not force convergence](#finite-prefixes-and-exact-collars-do-not-force-convergence)
- [Exact small-cap closure still does not force convergence](#exact-small-cap-closure-still-does-not-force-convergence)

### Size-biased martingales and the four-generation dispersion criterion

A dispersion route suggested by Benoît Cloitre can be expressed entirely
in the same selected child interface. The martingale identities and the
conditional decay implication below are exact. The required uniform
dispersion inequality for actual C remains open.

Start at a closed natural-block state (j,N), F_j<=N<=F_(j+1), and stop
at profile orders4 or5. At every internal node use its actual selected
children a and b=N-a, carrying labels j-1,j-2. The closed-block capture
theorem puts them in those two natural blocks. Choose the first child
with probability a/N and the second with probability b/N. Preserve these
inherited labels: recomputing a canonical order at a Fibonacci endpoint
would change the next variable and invalidate its displayed identity.

With alpha=1/phi, define the two path variables

$$
Z=\frac{C(N)-\alpha N}{N},\qquad X=\frac{F_j}{N}.
$$

**Martingale and exact local variance.** Both Z and X are martingales.
For Z, the conditional expectation is
`[C(a)+C(b)-alpha*(a+b)]/N=Z`. For X it is
`[F_(j-1)+F_(j-2)]/N=X`. In the stopped tree X lies in[3/5,1], so
the sum of its expected conditional variances is bounded independently
of the root. In particular the bound1 suffices below.

Writing A=F_(j-1), B=F_(j-2), the one-step variance is exactly

$$
v(j,N)=\frac{(Ab-Ba)^2}{N^2ab}. \tag{9.22}
$$

Indeed the two child readouts are A/a and B/b, with probabilities a/N
and b/N; the two-point variance is their squared difference times ab/N^2.
For N=F_j+u and a=A+r, the numerator is the square of
`A*u-F_j*r`. It measures the selected split's deviation from a proportional
Fibonacci split, rather than the cycle's defect sum alone.

Define V_0=0 and, away from the terminal orders, define recursively

$$
V_m(j,N)=v(j,N)+\frac aN V_{m-1}(j-1,a)
                       +\frac bN V_{m-1}(j-2,b). \tag{9.23}
$$

This is the accumulated variance over m generations; by martingale
orthogonality it also equals E[(X_m-X_0)^2]. Stop terms at orders4/5.
Although v is positive at every nonanchor internal N, positivity alone
does not give a scale-independent dispersion bound. In fact v=0 would
give F_j dividing N, since consecutive Fibonacci numbers are coprime;
the natural-block interval then forces N=F_j.

**Conditional quartic decay theorem.** Suppose there exist kappa>0 and
J such that every sufficiently high actual selected context satisfies

$$
V_4(j,N)\ge\kappa\left(\frac{C(N)-G(N)}N\right)^4
\qquad(j\ge J). \tag{9.24}
$$

Then

$$
C(n)-\alpha n=O\left(\frac n{(\log n)^{1/4}}\right).
$$

**Proof.** At a root of order j take L=floor(j/16) successive four-generation
blocks, with j large enough that j/2>=J. Every encountered order remains
at least floor(j/2), because one generation lowers it by at most two.
Thus every index is at least F_floor(j/2). Write
epsilon_j=alpha/F_floor(j/2) and D(N)=C(N)-G(N)>=0. Since
`G(N)-alpha*N<alpha`, the martingale identity for Z gives at each block
start

$$
\mathbb E\frac{D(N)}N\ge Z_0-\epsilon_j.
$$

Jensen's inequality, (9.24), and the disjoint accumulated variance budget
therefore give

$$
L\kappa\,\max(Z_0-\epsilon_j,0)^4\le1.
$$

Consequently Z_0<=epsilon_j+(L*kappa)^(-1/4). The Fibonacci growth law
gives epsilon_j=O(n^(-1/2)) and L of order log n. QED. This proves the
implication; it supplies neither (9.24) nor a matching lower bound for
the maxima, so it does not establish the conjectured order or exponent.

**Why geometric closure is insufficient.** There is an explicit globally
shared counterfamily to deriving (9.24) from the Fibonacci child geometry,
the terminal values and these martingale identities alone. Use the upper-cap
value U(N)=F_(j-1)+Q_j(u), Q_j(u)=min(u,F_(j-2)), discussed above.
In the linear part, set r to the nearest integer to
`F_(j-1)*u/F_j`, if

$$
u\le F_{j-2},\qquad 0\le r\le F_{j-3},\qquad
0\le u-r\le F_{j-4}.
$$

Otherwise use its already proved split
`r=min(F_(j-2),max(0,u-F_(j-4)))`. Select a=F_(j-1)+r and b=N-a.
Use the canonical order to define this choice once per physical N;
Fibonacci endpoint aliases obey the same split. In the rounded case both
child profiles are linear and their offsets sum to u, so U(a)+U(b)=U(N).
The fallback has the same identity. Thus this is shared geometric descent
with the original terminal values, and both martingales hold with U.

Now take N_j=F_j+floor(F_j/10). For any fixed number of generations, all
visited indices have the form

$$
N'=\frac{11}{10}F_h+O(1),
$$

with h differing from j by a bounded amount. This follows by rounding
error induction; the ratios of the Fibonacci child weights are less than
one, so a bounded-depth accumulated rounding error stays bounded. For
large j the displayed split inequalities have a margin proportional to
F_h, so all these top splits use the rounded case. Each X then differs
from10/11 by O(1/F_j), proving V_4(j,N_j)=O(F_j^(-2)). But

$$
\frac{U(N_j)-G(N_j)}{N_j}\longrightarrow\frac{1-\alpha}{11}>0.
$$

Indeed U(N_j)=N_j-F_(j-2) in this linear part and F_(j-2)/F_j tends
to1-alpha. No positive uniform kappa can satisfy (9.24) for this family.
It is not the nested C sequence: at11 its value8 fails the actual depth
selection, as proved above. It also does not satisfy all global C envelopes.
This counterexample isolates a missing use of actual selected-orbit
constraints; it does not refute Cloitre's conjecture for actual C.

**An exact basin obstruction in that counterfamily.** The rounded family
also shows that correct numeric values and periodicity can admit the wrong
dispersion phase. For its upper-cap profile U, choose j>=12 and

$$
F_{j-5}+1\le u\le F_{j-4},\qquad N=F_j+u,
$$

and write A=F_(j-1), B=F_(j-2), D=F_(j-3). From the prescribed start,
the clocks0 through8 under T_(N,U)(x)=N-U(x) are exactly

$$
N-1,\ B+1,\ 2B+u-1,\ B+u,\ 2B,\ 2D+u,\ A+u,\ A,\ A+u.
$$

To check every arrow, the U-values at the first eight points are,
respectively,

$$
A+u-1,\ D+1,\ A,\ D+u,\ B+F_{j-4},\ B,\ B+u,\ B.
$$

These follow directly from U(F_h+w)=F_(h-1)+min(w,F_(h-2)).
The lower bound on u caps the value at2B+u-1; at2D+u the cap
follows from `2F_(j-5)+1>F_(j-4)`. The other points lie in the
displayed linear pieces. At u=F_(j-4),2D+u=A, so entry may already
occur at clock5; the claim is entry by clock6. The prescribed depth
U(N-1)=A+u-1 is at least6, and selects A+u at even clocks and A
at odd clocks.

Yet every point A+r,0<=r<=u, is periodic, since
`T_(N,U)(A+r)=A+u-r`; and every such split gives the same numeric
root value U(A+r)+U(B+u-r)=A+u. The rounded proportional r at
u=floor(F_j/10),j>=12, lies strictly between0 andu, in a different
cycle from the prescribed outer pair. Its value certificate and
periodicity therefore do not certify the prescribed-start basin.
This tenth offset satisfies the required interval: F_j-10F_(j-5)
has the Fibonacci recurrence with values14,23 at orders12,13, hence
is at least14 thereafter; and F_j=5F_(j-4)+3F_(j-5)<10F_(j-4).
Since u>=14 and 1/2<A/F_j<2/3, its rounded r is strictly interior.
For example, j=12,u=14,N=158 gives

```text
157 -> 56 -> 123 -> 69 -> 110 -> 82 -> 103 -> 89 -> 103.
```

The depth102 selects103; the rounded split98 is in the separate
cycle(94,98). Both give U(158)=103. Along the tenth-offset family,
the outer pair's local variances stay bounded away from zero, while
the rounded geometric four-generation variance tends to zero.
This strengthens the basin obstruction within U; it remains a
counterfamily to weaker premises, not a counterexample for actual C.

**Finite actual check.** Exact rational arithmetic verifies (9.24) with
kappa1 for every positive-defect root144<=N<=131071. The smallest ratio
V_4/(D/N)^4 occurs at N=469 and equals
18868124506192831/112729162291200, approximately167.376. The checker
also verifies the rounded counterfamily at orders20,30,40,60,90 without
generating huge recurrence prefixes; at order90 its quartic ratio is
less than10^(-29). Finite actual support is encouraging, but cannot replace
the uniform inequality. Proving that inequality would connect the
selected-value interface to a quantitative occupation estimate.

### A phase-free lower bound from the prescribed basin

For proving a lower bound, exact selected phase can be avoided by taking
the worst phase in a certified basin. This is a different contract from
recovering the actual split or all future variance readouts.

Let Gamma_N be the eventual cycle reached from the prescribed start N-1
under the actual T_N(x)=N-C(x). Supply this cycle and the actual C values
on the relevant contexts. For a closed-block state (j,N), define

$$
\mathcal B_0(j,N)=0,
$$

$$
\mathcal B_m(j,N)=\min_{a\in\Gamma_N}
\left[v(j,N;a)+\frac aN\mathcal B_{m-1}(j-1,a)
                  +\frac{N-a}{N}\mathcal B_{m-1}(j-2,N-a)\right],
$$

where v(j,N;a) is (9.22) evaluated at a and N-a; stop at orders4/5.
Let Gamma_N^C be the subset satisfying C(a)+C(N-a)=C(N), and define
Q by the same recurrence with Gamma_N^C in place of Gamma_N.
The actual selected endpoint belongs to Gamma_N^C. The closed-block
capture theorem puts all these candidates in the two inherited child
blocks, including endpoint aliases. Therefore both recurrences are defined.

**Bellman lower-envelope theorem.** For every m and supplied actual context,

$$
\mathcal B_m(j,N)\le\mathcal Q_m(j,N)\le V_m(j,N).
$$

**Proof.** At depth0 all three quantities are zero. Inductively, restricting
Gamma_N to Gamma_N^C and replacing child B by their larger Q values
can only increase the minimum. Evaluating the Q minimum at the actual
selected endpoint, then replacing child Q by their larger actual V,
gives exactly (9.23). This proves both inequalities. All weights are
nonnegative. QED.

Each envelope is the exact minimum over its permitted occurrence trees:
after choosing a root phase, its two subtree minima are attained
independently. Different occurrences of the same physical integer may
choose different phases, even at different remaining depths. Thus this
is a relaxation of globally shared actual descent; it is not an exact
minimum over globally shared selectors. Sharing constraints can only
raise the minimum. Q preserves the scalar C identity at every chosen
split; the larger B domain does not require that identity.

A uniform lower bound

$$
\mathcal B_4(j,N)\ge\kappa\left(\frac{C(N)-G(N)}N\right)^4
$$

would be a stronger sufficient condition for (9.24), and the same is
true with Q in its place. Neither condition is proved uniformly.
They require no exact predecessor-depth residue for selecting a phase
once the basin tables are supplied. Building and certifying those tables,
their scalar profiles and their recursive context is still part of the
full interface problem. The conditional local-variance phase minimum
above does not prevent this lower-bound strategy.

The maintained checker verifies B_4<=Q_4<=V_4 and the stronger finite
bound B_4>=(D/N)^4 for all130891 positive-defect roots144..131071.
The finite minima over this entire range are:

| Four-generation quantity | Minimum ratio to (D/N)^4 | Root N |
|---|---:|---:|
| All phases of the prescribed-start basin, B_4 | 101.197 | 4590 |
| Basin phases preserving the actual scalar value, Q_4 | 140.919 | 302 |
| Actual depth-selected descent, V_4 | 167.376 | 469 |

These rounded decimals summarize exact rational evidence. The first
minimum is62668211167781606281392909/619272222475981140335360;
the second is3659008386849973/25965324000000.
The checker also computes the weaker all-periodic
relaxation through4096, replacing Gamma_N by every periodic point of T_N.
In144..4096, the minimum basin ratio B_4/(D/N)^4 is
9279338934951/86736329680, approximately106.983, at191. The minimum
all-periodic ratio is2179271359290201381/104713624505000000,
approximately20.812, at2778. These are minima over the stated finite
range, not estimates of a uniform constant. They show quantitatively
why basin qualification strengthens the available lower envelope.

### Quadratic basin dispersion in the unit-defect family

The [exact unit-sublevel theorem](exact-collars.md#the-unit-defect-sublevel-set-and-its-arithmetic-spine)
gives an infinite actual-C domain on which the required basin lower bound
can be proved without choosing a cycle phase. Let k>=20,
N=F_k-v, 0<=v<=R_k, and retain its natural-block label j=k-1.
Write D=C(N)-G(N). Then

$$
\boxed{\mathcal B_1(j,N)\ge\frac{v^2}{25N^2}
                    \ge\frac1{25}\left(\frac DN\right)^2.} \tag{U.4}
$$

In particular the four-generation quartic sufficient condition holds
on this growing domain with kappa=1/25. This is a scoped theorem;
the inequality for all sufficiently high natural-block contexts remains open.

**Proof.** Put A=F_(k-1), B=F_(k-2), H=F_(k-3).
For every phase in the unique prescribed basin, the split and its
complementary argument have the form

$$
a=A-v+\delta,\qquad b=B-\delta.
$$

The unit-family classification gives delta in{0,1,2}. A phase with
delta=1 requires v>=L_(k-1)+1>=10. A phase with delta=2 requires
v=R_(k-1)+2>=21. This applies to both phases at both two-cycle
frontiers, including a phase that does not preserve the actual parent
scalar value. All these splits are in the captured child blocks.

With inherited label j=k-1, the numerator of (9.22) is

$$
M=Bb-Ha=B^2-HA+Hv-A\delta
       =(-1)^{k-1}+Hv-A\delta.
$$

We have A<=3H and H>=2. If v>=1 and delta=0, then
M>=Hv-1>=Hv/2. For delta=1,
M>=H(v-3)-1>=Hv/2 since v>=10; for delta=2,
M>=H(v-6)-1>=Hv/2 since v>=21. Thus the bound holds for
every basin phase, without any depth residue or entrance flag.
Since N<=F_k=A+B<=5H and ab<=N^2/4,

$$
v(j,N;a)=\frac{M^2}{N^2ab}
\ge\frac{H^2v^2}{N^4}
\ge\frac{v^2}{25N^2}.
$$

Taking the minimum over phases proves the first inequality in (U.4).
The global cap gives C(N)<=A=G(F_k), and G is1-Lipschitz, hence
0<=D<=v. At v=0 this gives D=0 and the displayed lower bound is
trivial. Nonnegative child variances imply B_4>=B_1; also D/N<=1,
so (U.4) implies B_4>=(1/25)(D/N)^4 on the stated domain. QED.

The [collar checker](verification/collar_check.py) verifies the exact
Cassini numerator and both inequalities using integer cross-products
for every phase of every qualified basin at orders20..30. Its finite
minimum ratio to (D/N)^2 is recorded exactly as a rational number in
[the evidence](verification/collar-check.json); it is corroboration,
not an estimate of a global constant.

**Extension through cap defect3.** The
[higher-cap theorem](exact-collars.md#two-higher-cap-levels-and-their-phase-selected-closure)
extends (U.4), with the same constant1/25, to every k>=22 and
0<=v<=Z_k=3k+floor((k-1)/3)-24. All phases of the unique basin
have delta in{0,1,2,3,4}. A nonzero shift1 requires v>=12;
shift2 requires v>=23; shift3 requires v>=41; and shift4
requires v>=49. These follow from the four frontier cycles at
the first eligible order22 and the fixed bands between them.
In particular v>=6delta+2 whenever delta>=1. Thus

$$
M\ge H(v-3\delta)-1\ge Hv/2,
$$

using H>=2, and the previous argument applies to every phase.
The checker verifies all basin phases through order30, including
excluded boundary phases with a different parent scalar readout.
This gives a larger infinite domain, still of width O(k) at F_k;
it is not a uniform inequality over the interiors of whole blocks.

This proof connects arithmetic recursive closure to Benoît Cloitre's
dispersion route. In the extended family every complementary gap is at most4,
so the
proportional-split cancellation of M cannot occur. In wider blocks,
large complementary gaps can approach that cancellation ratio; controlling
their accumulated variance still requires new actual-profile restrictions.

**A scalar-valid alternative on canonical interaction windows.** The
[additive-window theorem](exact-collars.md#additive-canonical-windows-and-a-direct-descendant-decoder)
supplies an explicit stronger policy certificate on its infinite family.
Let t=F_m, k=ceil(3(t-3)/2), m>=8, and put
S=F_k,A=F_(k-1),B=F_(k-2),N=F_(k+1)-t. Retain the natural-block
label j=k. The geometric split a=S-t,b=A preserves C(N) exactly,
although the actual prescribed split is a+1. Its one-step variance obeys

$$
\boxed{v(k,N;a)\ge\frac12\left(\frac{C(N)-G(N)}N\right)^2.} \tag{U.5}
$$

**Proof.** The additive table gives C(a)+C(b)=C(N)=S-1.
Cassini gives the variance numerator
AN-Sa=Bt+sigma, where sigma=A^2-SB is1 or-1.
For k>=5, A/B lies in[3/2,5/3], as follows by induction under
r->1+1/r. Therefore B^2/(SA)>=9/40, and

$$
v(k,N;a)=\frac{(Bt+\sigma)^2}{N^2(S-t)A}
\ge\frac9{40}\frac{(t-1)^2}{N^2}.
$$

Writing alpha=1/phi, Fibonacci's exact error
|S-alpha F_(k+1)|=alpha^(k+1)<alpha and
G(N)>alpha(N+1)-1 give D=C(N)-G(N)<alpha t.
Since alpha^2<2/5 and t>=21, for D>0 the last bound is greater than
(9/16)(20/21)^2*(D/N)^2=(25/49)(D/N)^2, which exceeds half.
At D=0 the result is immediate. QED.

At m8, D=12 and the exact ratio v/(D/N)^2 is
155142242161/214570989189. The collar checker verifies this selected
alternative and the symbolic inequality on the larger arithmetic contexts;
only the first context is regenerated as an actual C prefix.
This removes phase qualification for a concrete scalar-valid policy and
connects the five-pattern interaction to dispersion. It still covers a
Fibonacci neighborhood rather than the interiors of all blocks.

### Cap-adaptive quadratic dispersion

Integer cap conservation extends quadratic dispersion beyond the exact
cap-defect0..3 profiles. The number of generations now depends on the
parent cap defect. A stopped lower envelope needs no high-cap basin or
depth-selection information: it allows every scalar-valid geometric split
until reaching a zero-child split or the arithmetic low-cap family.

**Theorem.** Let N=F_k-v, 0<=v<=F_(k-2), and put
e=Q_k(v)=F_(k-1)-C(N). Set

$$
t(e)=\max(1,e-2),\qquad K(e)=22+2\max(0,e-3).
$$

For k>=K(e), actual selected descent with inherited natural label k-1
satisfies

$$
\boxed{V_{t(e)}(k-1,N)\ge\frac1{100}\left(\frac vN\right)^2
                 \ge\frac1{100}\left(\frac{C(N)-G(N)}N\right)^2.}
\tag{A.1}
$$

Thus for every fixed cap bound m>=0, horizon max(1,m-2) suffices
at k>=22+2max(0,m-3), on the entire cap sublevel, including holes.
In particular,

$$
k\ge28,\quad Q_k(v)\le6
\quad\Longrightarrow\quad
V_4(k-1,N)\ge\frac1{100}\left(\frac{C(N)-G(N)}N\right)^2.
\tag{A.2}
$$

This also gives the quartic sufficient inequality on that sublevel.
It does not establish a fixed-horizon bound at unbounded cap defects,
or a global convergence or decay rate.

**A local bound when a child cap is zero.** At any order h>=22 put
A=F_(h-1), B=F_(h-2), H=F_(h-3), and write a=A-r, b=B-q,
where r+q=u and N'=F_h-u. A geometrically valid split has both
children in their inherited closed blocks. Suppose it preserves the
actual scalar sum and at least one child cap defect is zero.

If u<=Z_h=3h+floor((h-1)/3)-24 and the split is in the prescribed
basin, the earlier cap-defect0..3 theorem already gives
v(h-1,N';a)>=u^2/(25N'^2). For u>Z_h no basin assumption is needed.
The exact zero-support law places a zero-cap first-child gap at
r<=L_(h-1), or a zero-cap second-child gap at q<=L_(h-2), where
L_s=floor(2s/3)-3. Direct integer arithmetic gives

$$
Z_h+1\ge4L_{h-1}+4\qquad(h\ge22).
\tag{A.3}
$$

Indeed, writing h=3s,3s+1,3s+2, the difference between the two
sides is respectively 2s-12,2s-12,2s-9, all nonnegative in this range.
Thus the zero child's gap is at most(u-4)/4. The variance numerator is

$$
M=Bb-Ha=(-1)^{h-1}+Hu-Aq
             =(-1)^{h-1}-Bu+Ar.
$$

Use H<=B<=2H, A<=3H and N'<=5H. If q is the zero-cap gap,
M>=Hu-3Hq-1>=Hu/4. If r is the zero-cap gap,
M<=1-Hu+3Hr<=-Hu/4. Since ab<=N'^2/4,

$$
v(h-1,N';a)=\frac{M^2}{N'^2ab}
\ge\frac{u^2}{100N'^2}.
\tag{A.4}
$$

For a parent cap e>3, the exact sublevel theorem forces u>Z_h;
therefore every scalar-valid zero-child split obeys (A.4). At e<=3,
use any phase of the arithmetic prescribed basin and the earlier
stronger bound. These are the two stopping cases.

**Integer branching gives a finite stopping frontier.** Actual child
cap defects e_1,e_2 are nonnegative integers with e_1+e_2=e.
Stop at a node of cap at most3, or at a split with a zero-cap child,
and include its one-step variance. Before stopping, both child caps
are positive, so each is at most e-1. Starting at cap e>3, every path
therefore stops at depth at most e-3 and makes at most e-2 splits.
For e<=3 it makes one split. The order drops by at most two per
generation, so k>=K(e) keeps every stopping node at order at least22.

The upper-anchor gap ratio Y=u/N' is itself an exact martingale:

$$
\frac a{N'}\frac ra+\frac b{N'}\frac qb=\frac u{N'}.
\tag{A.5}
$$

Let w_l be the size-biased probability of a stopping node and
Y_l its gap ratio before its final split. This bounded-depth frontier
has sum_l w_l=1 and sum_l w_lY_l=v/N. By (A.4) and the low-cap
bound, its total expected final-step variance is at least

$$
\frac1{100}\sum_l w_lY_l^2
\ge\frac1{100}\left(\frac vN\right)^2.
$$

Earlier conditional variances are nonnegative. The stopped sum is
therefore bounded above by V_t(e), proving the first inequality in
(A.1). The global cap and the 1-Lipschitz G give
0<=C(N)-G(N)<=G(F_k)-G(F_k-v)<=v, proving the second. QED.
The gap martingale uses the upper anchors, while V uses the previously
defined natural-anchor martingale X. Their inherited labels must both
be preserved; no endpoint recanonicalization is made.

**A sufficient interface without high-cap orbit qualification.** The
same proof applies to a larger stopped class. At cap e>3 allow every
geometric split satisfying C(a)+C(b)=C(N'), regardless of whether it
is periodic or in the prescribed basin. Stop if a child cap is zero;
otherwise recurse into both children. At cap e<=3 use any phase of
the arithmetic prescribed basin, take one variance step and stop.
Its scalar readout need not equal C(N') at this final step: cap
conservation is only used before this stopping case, and (A.5) remains
true for the final geometric split.

The exact minimum A(h,N') over this class obeys the same lower bound.
This can also be proved by induction on e: a zero-child option uses
(A.4); a two-positive-child option uses the two inductive bounds and
the weighted-square inequality in (A.5). The low-cap arithmetic kernel
starts the induction. Evaluating every minimum at the actual selected
split shows

$$
\frac1{100}(u/N')^2\le\mathcal A(h,N')
\le V_{t(e)}(h-1,N').
\tag{A.6}
$$

The minimum permits independent choices at repeated occurrences; a
globally shared actual selector is included in this larger class. No
high-cap predecessor, exterior entrance, cycle or phase certificate is
needed for this dispersion contract. Actual scalar values, geometric
child blocks, cap conservation and the proved low-cap basin kernel
remain required. This relaxation does not reconstruct the original
selected children or settle their full minimum interface. Campbell's
nonadditive recurrence does not have this integer two-child cap flow;
its modular endpoint interface remains the relevant comparison.

The [checker](verification/collar_check.py) computes the stopped minimum
over all scalar-valid geometric high-cap options at qualifying roots,
checks the arithmetic low-cap kernel against full inner orbits, and
compares the envelope with exact actual accumulated variance. Literal
prescribed-depth witnesses independently check the selected splits.
The infinite argument adds no new finite sequence premise; it inherits
the established cap conservation, zero-support and cap0..3 theorems.

The exact finite audit covers821 qualifying roots at orders22..30,
with22397 geometric candidate tests,5949 zero-child stopping options
and5416 two-positive-child options. Its567 low-cap contexts are checked
against full inner graphs. The minimum envelope ratio to(v/N)^2 is
49874948929/740731548887, at k26,v73,N121320; this finite minimum
is above1/100 but is not claimed as a uniform best constant.
Among the minimizing high-cap choices,247 are nonperiodic points of
the inner map. At N46312 the relaxed minimizing split is28625,
while the actual split is28604. This verifies that the envelope does
not quietly retain high-cap periodicity or basin qualification.
The finite qualifying roots have cap defects0,1,2,3,4,7; there are
no qualifying cap5/6 witnesses in this range. The theorem for those
levels follows from the general integer induction, not numerical
examples. Two selected high-cap witnesses are checked by542875 literal
updates; full-orbit and Brent prefixes agree through832074.

### A logarithmic horizon from one retained child

The linear stopping horizon above retains both positive-cap children.
One child suffices if the parent's own variance is used to control its
gap ratio. Integer conservation then halves the permitted cap at each
retained step, giving a logarithmic horizon with a smaller constant.

**Theorem.** For any integer t>=1, let N=F_k-v lie in the full closed
upper-anchor block, with e=Q_k(v). If

$$
k\ge22+2(t-1),\qquad e\le3\cdot2^{t-1},
$$

then actual selected descent satisfies

$$
\boxed{V_t(k-1,N)\ge\kappa_t\left(\frac vN\right)^2
                  \ge\kappa_t\left(\frac{C(N)-G(N)}N\right)^2,
\qquad \kappa_t=\frac1{25\cdot4^{t-1}}.}
\tag{L.1}
$$

Choose the least t>=1 for which e<=3*2^(t-1); its order is
O(log(e+1)). For e>3 its capacity lies in[e,2e), so
kappa_t>9/(100e^2); the constant has inverse-quadratic cap order.
It depends on t. In particular

$$
k\ge28,\quad Q_k(v)\le24
\quad\Longrightarrow\quad
V_4(k-1,N)\ge\frac1{1600}
                 \left(\frac{C(N)-G(N)}N\right)^2.
\tag{L.2}
$$

The previous constant1/100 remains available at its stated linear
horizon. Neither result proves a uniform fixed-horizon bound
at unbounded caps or the global decay rate.

**One-child transfer lemma.** Put N'=F_h-u, h>=22, u>=1,
A=F_(h-1), B=F_(h-2), H=F_(h-3). For any geometric split
a=A-r, b=B-q with r+q=u, let nu be its one-step natural-anchor
variance. For either child, write w for its size divided by N' and
y for its upper-anchor gap divided by its size. Then for
0<theta<=1/25,

$$
\boxed{\nu+\theta w y^2\ge\frac\theta4(u/N')^2.}
\tag{L.3}
$$

This lemma does not assume periodicity, cap conservation or scalar
preservation. It uses the geometric child blocks, Cassini's identity
and the order/gap domain.

**Proof.** Write s=(-1)^(h-1) and

$$
M=Bb-Ha=s+Hu-Aq=s-Bu+Ar,
\qquad \nu=\frac{M^2}{N'^2ab}.
$$

Since H>=32 and u>=1, the additive Cassini error1 is at most
Hu/32, and also Bu/32. Consequently

$$
\frac u{N'}\le\frac{32}{31}\left(
     \frac AB\frac a{N'}\frac ra+
     \frac{\sqrt{ab}}B\sqrt\nu\right),
$$

$$
\frac u{N'}\le\frac{32}{31}\left(
     \frac AH\frac b{N'}\frac qb+
     \frac{\sqrt{ab}}H\sqrt\nu\right).
$$

The geometric blocks give B<=a<=A, H<=b<=B, so
a/N'<=3/4 and b/N'<=1/2. Consecutive Fibonacci ratios satisfy
3/2<=B/H<=5/3 in this range; the recurrence maps that interval
into itself. Thus A/B<=5/3, A/H<=8/3 and AB/H^2<=40/9.
Weighted Cauchy--Schwarz in the first
display therefore gives

$$
(u/N')^2\le\left(\frac{32}{31}\right)^2
                  \left(\frac{25}{12\theta}+\frac53\right)
                \left(\nu+\theta\frac a{N'}(r/a)^2\right).
$$

The second display gives

$$
(u/N')^2\le\left(\frac{32}{31}\right)^2
                  \left(\frac{32}{9\theta}+\frac{40}9\right)
                \left(\nu+\theta\frac b{N'}(q/b)^2\right).
$$

Both coefficients are at most4/theta when theta<=1/25: after
multiplication by theta the larger is at most
(32/31)^2*(56/15)<4,
proving (L.3). QED. This transfers a bound from one child;
the gap martingale alone would require both children for Jensen.

**Cap-halving induction.** At t=1 the cap0..3 arithmetic basin
theorem proves (L.1). At a larger t, if the parent already has
cap<=3, that stronger one-step bound suffices. Otherwise consider
its actual split. A zero-cap child gives the earlier1/100 local
bound, at least kappa_t since t>=2. If both caps are positive,
one has

$$
e_c\le\lfloor e/2\rfloor\le3\cdot2^{t-2}.
$$

Its inherited order is at least k-2>=22+2(t-2). The inductive
bound gives V_(t-1) at that child at least kappa_(t-1)y^2.
Discard the other child's nonnegative descendant variance and apply
(L.3) with theta=kappa_(t-1). The remaining quantity is at least
kappa_t(v/N)^2. As before 0<=C(N)-G(N)<=v gives the last
inequality in (L.1). QED.

**An exact minimum over retained spines.** A larger certificate class
preserves this lower bound. At high cap allow every scalar-valid
geometric split. Stop at a zero-child option; otherwise retain only
one child whose cap is at most3*2^(t-2), assigning zero future
variance to the other child. At least one child is eligible. At
cap<=3 finish with one phase of the arithmetic prescribed basin.
Its final scalar sum may differ, because no further cap induction
uses that final step. The retained horizon decreases at every edge.

The minimum L_t over all these choices satisfies

$$
\kappa_t(v/N)^2\le\mathcal L_t(k,N)\le V_t(k-1,N).
\tag{L.4}
$$

The proof repeats the cap-halving induction for every candidate option;
the actual split and an eligible actual child give the upper comparison.
Each candidate certificate retains a single path of length at most t,
including its weighted local variances, instead of both descendant trees.
For five row-aligned roots this gives five such paths, with inherited
labels throughout; the five roots need not form an inner five-cycle.
Their scalar profiles and high-cap splits still
require geometric and scalar-sum checks; no high-cap cycle, entrance
or exact phase certificate is needed for the bound. The low-cap basin
kernel remains required. This is sufficient information for dispersion,
not a minimum certificate theorem or a reconstruction of actual children.

Campbell's nonadditive family does not supply this two-child integer cap
flow. Its ternary arithmetic supplies the endpoint/parity interface,
while the additive Cloitre interface admits this retained-spine bound.
The distinction matters when comparing what information each proof uses.

The [checker](verification/collar_check.py) evaluates L_t over all
scalar-valid geometric high-cap splits and every eligible retained child,
checks (L.3) independently on geometric splits, and compares the minimum
with exact actual accumulated variance. The infinite theorem adds no new
finite sequence premise; it uses the previously proved cap0..3 and
zero-support results with the displayed transfer lemma.

Exact finite evidence covers1418 qualifying roots at orders22..30,
with145487 geometric candidate tests and39135 eligible-child transfer
checks. There are17569 zero-child options and1071 arithmetic low-cap
context checks. The one-child inequality is also checked independently
on36720 geometric cases without scalar or cap qualification. Every
retained-spine minimum is compared with actual V_t;809 high-cap
minimizers are nonperiodic, so no high-cap orbit qualification is hidden
in this computation. Three actual selected endpoints have300083 literal
updates, and full-orbit/Brent prefixes agree through832074.

The four-generation finite minimum L_4/(v/N)^2 is
8314368923835887179/627400837029851962000 at k28,v280,N317531,
cap24. Its minimizing first gap is169 and it retains the second child;
the actual first gap is257. This finite ratio is above1/1600;
it is not a claimed uniform optimal constant. The qualifying finite
cap counts are recorded separately: cap5 has no example in this range,
while the general induction covers it. Table construction, minimum
certificate size and global dispersion remain separate questions.

### Diophantine dispersion in cube-root Fibonacci neighborhoods

Small complementary gaps are not necessary for a uniform quartic bound.
Integer separation from the golden ratio controls every captured phase
through a much wider sublinear neighborhood.

**Cube-root dispersion theorem.** Let k>=21, N=F_k-v with
0<=v<=F_(k-2), and suppose v^3<=N. With D=C(N)-G(N),

$$
\boxed{\mathcal B_1(k-1,N)\ge\frac1{25}\left(\frac DN\right)^4.} \tag{D.1}
$$

For v>=1 we also have B_1>=1/(25v^2N^2). Consequently B_4
satisfies the same quartic criterion on this entire cube-root collar.
The theorem requires no exact profile, predecessor residue or phase choice.

**Proof.** Put A=F_(k-1), B=F_(k-2), H=F_(k-3) and
lambda=phi^2=(3+sqrt(5))/2. Every captured phase has
a=A-v+delta, b=B-delta with integral0<=delta<=v. Its variance
numerator is M=(-1)^(k-1)+Hv-A*delta.

For v>0, the nonzero integer norm

$$
(v-\lambda\delta)(v-\lambda^{-1}\delta)
 =v^2-3v\delta+\delta^2
$$

has absolute value at least1. Its conjugate factor is positive and
at mostv, since0<=delta<=v. Hence |v-lambda*delta|>=1/v.
Also |A-lambda H|=alpha^(k-3)<1. If H>=4v^2, then

$$
|M|\ge H/v-v-1\ge H/(2v).
$$

Since N<=A+B<=5H and ab<=N^2/4,

$$
\frac{M^2}{N^2ab}\ge\frac1{25v^2N^2}
\ge\frac1{25}\left(\frac vN\right)^4
\ge\frac1{25}\left(\frac DN\right)^4. \tag{D.2}
$$

The middle inequality uses v^3<=N; the last uses0<=D<=v from
the global cap and the1-Lipschitz G function. The auxiliary condition
H>=4v^2 is automatic: for v>=20 use H>=N/5>=v^3/5>=4v^2;
for1<=v<=19 use H>=F_18=2584>4*19^2. At v0, D=0.
Taking the minimum over all basin phases proves (D.1). QED.

**Every fixed cap level eventually qualifies.** The
[cap-budget theorem](recursive-descent.md#a-quadratic-enclosure-for-every-bounded-cap-level)
gives v<=mP_k throughout Q_k<=m, for m>=1. Define T(m) as the
first k>=30 with F_(k-3)>=4(mP_k)^2 and
F_k-mP_k>=(mP_k)^3. Both inequalities persist: P_(k+1)<=11P_k/10
for k>=30, while Fibonacci numbers grow by at least3/2 and
F_(k+1)-mP_(k+1)>=3(F_k-mP_k)/2. The budget ratio follows from
P_k>=10L_(k-1), starting at k30 and propagating because L>=10.
Exponential growth ensures T(m) exists. Thus the whole cap sublevel,
including its holes, satisfies (D.1) for every k>=T(m).
For m1,2,3,4 these sufficient thresholds are39,45,49,51.

The checker exhausts geometric integer shifts in the cube-root collars
at orders21..40, verifies actual basin phases at orders21..30, and
checks the explicit bounded-cap thresholds arithmetically. Large-order
arithmetic checks do not evaluate new C prefixes. This is an infinite
Diophantine proof with finite corroboration, not extrapolated dispersion.
The interiors outside these sublinear collars, where v is proportional
to F_k, still require a uniform multi-generation argument; the global
convergence and decay theorem remains open.

### Additive dispersion policies without orbit qualification

The asymptotic problem permits more freedom than reconstructing the
original nested recurrence. Once actual C values are established, a
different value-preserving decomposition tree can prove facts about
those same values. Its split need not be a periodic point, belong to
the prescribed basin, or agree with the prescribed depth phase.

At a closed state (j,N), put A=F_(j-1), B=F_(j-2), S=A+B and define

$$
\mathcal R_j(N)=\{a:\ A\le a\le S,\quad B\le N-a\le A,
                         \quad C(a)+C(N-a)=C(N)\}.
$$

This set is nonempty because it contains the actual selected endpoint.
Every child is strictly smaller than N. Preserve inherited order labels,
including Fibonacci endpoint aliases, and stop at orders4/5 as before.
An admissible policy chooses any member of R at each occurrence; it may
depend on the previous choices and on the remaining horizon.

**Policy martingales.** Under every such policy, choose its two children
with probabilities a/N,(N-a)/N. Then Z=(C(N)-alpha*N)/N and X=F_j/N
remain exact martingales, with the same bounded variance budget for X.
The proof uses only the scalar sum and the Fibonacci anchor sum, not the
inner dynamics. Even if repeated physical indices use different choices,
their scalar C value is unchanged, so both conditional identities hold.

Define the standard finite-horizon Bellman maximum

$$
\mathcal M_0(j,N)=0,
$$

$$
\mathcal M_m(j,N)=\max_{a\in\mathcal R_j(N)}
\left[v(j,N;a)+\frac aN\mathcal M_{m-1}(j-1,a)
                  +\frac{N-a}{N}\mathcal M_{m-1}(j-2,N-a)\right].
$$

It is attained and equals the greatest accumulated X variance over
m-generation admissible occurrence trees. Indeed, after the root
choice, the two finite subtree optima can be attained independently;
induction gives the displayed formula. In particular M_m>=actual V_m.
This upper envelope of possible variance serves a lower-bound criterion
by selecting a policy that attains it.

**Adaptive dispersion criterion.** Suppose fixed m>=1,q>=1,kappa>0
and J exist such that every closed actual-value context of order j>=J
satisfies

$$
\mathcal M_m(j,N)\ge\kappa
                   \left(\frac{C(N)-G(N)}N\right)^q.
$$

Then

$$
C(n)-\alpha n=O\left(\frac n{(\log n)^{1/q}}\right).
$$

**Proof.** For a root of order j, use L=floor(j/(4m)) consecutive
m-generation blocks. At each block start choose an M_m maximizing
policy, decreasing the remaining horizon along that block. All visited
orders stay at least floor(j/2), so the inequality applies for large j.
The X variance budget is at most1. The Z martingale and
`-alpha^2<G(N)-alpha*N<alpha` imply at every block start

$$
\mathbb E\frac{C(N)-G(N)}N
\ge Z_0-\frac\alpha{F_{\lfloor j/2\rfloor}}.
$$

Conditional accumulated variance in that block is its attained M_m.
Sum over blocks and apply Jensen for q>=1 to obtain

$$
L\kappa\max\left(Z_0-\frac\alpha{F_{\lfloor j/2\rfloor}},0\right)^q
\le1.
$$

Fibonacci growth gives the conclusion. The block policies may be
time-dependent; conditional martingale identities and orthogonality
still apply. QED.

For q=4 this is a sufficient route to Cloitre's proposed upper rate
without proving his actual-selected dispersion inequality. For q=2 it
would give a stronger square-root logarithmic upper rate, but no uniform
q=2 or q=4 policy inequality is proved here. A finite greedy experiment
cannot settle either exponent or the matching maxima lower bound.

**Only extreme value-valid candidates are needed for a local maximum.**
Let ell=min R_j(N), h=max R_j(N). Then

$$
\mathcal M_1(j,N)=\max(v(j,N;\ell),v(j,N;h)).
$$

To prove this, put z=a/N,p=A/S. The variance is
`(S/N)^2*(z-p)^2/(z*(1-z))`. The derivative of its final factor is

$$
\frac{(z-p)(p(1-z)+(1-p)z)}{z^2(1-z)^2}.
$$

The second factor in the numerator is positive for0<z<1. Thus variance
decreases to its unique minimum at z=p and then increases. Every
candidate between ell and h has variance at most their maximum, even
when R is non-contiguous. Choose the larger endpoint variance, breaking
ties by the larger index, to define a greedy policy. This maximizes
one-step variance; it need not maximize M_m for m>1.

For certifying a lower bound, even extremality is unnecessary. One
value-valid geometric split with

$$
2|AN-Sa|\ge(C(N)-G(N))^2
$$

already certifies v>=(D/N)^4, since a(N-a)<=N^2/4. More generally a
factor c on the right certifies kappa=c^2. Thus an existential scalar
sum, child-block membership and integer mismatch witness can replace
basin and phase certificates for this asymptotic contract. Proving such
witnesses uniformly, or providing certified multi-generation policies,
still requires the actual C profiles. This does not recover the original
selector or establish the full minimum recursive closure interface.

**Actual policies can leave every inner cycle.** At N=3054 the greedy
split is1971 instead of the actual1839. Both preserve C(3054)=2016;
the child values are C(1971)=1313 and C(1083)=703. This alternative is
not a periodic point of T_3054, as the all-start graph check verifies.
Its admissibility for this proof rests on the scalar sum and the
two child blocks. The actual recurrence and its selected endpoint have
not been redefined.

This freedom is specific to an additive scalar recursion. Campbell's
sequence has b(5)=2, whereas the four complementary sums b(a)+b(5-a)
are4,3,3,4. It admits no additive policy at that index. Its ternary
endpoint/phase templates remain the appropriate cross-family interface;
the common reflection description alone does not transfer this argument.

**Why maximal dispersion is still an additional premise.** The upper-cap
family U supplies a stronger obstruction than its rounded tenth-offset
example. Take the knee N_j=F_j+F_(j-2). Then U(N_j)=F_j and
write A=F_(j-1), B=F_(j-2), D=F_(j-3), E=F_(j-4), so D+E=B.
For a geometrically valid split a=A+r, scalar preservation requires

$$
\min(r,D)+\min(B-r,E)=B=D+E.
$$

Both terms must attain their caps, forcing r=D. Thus there is exactly
one admissible split, to N_(j-1)=A+D and N_(j-2)=B+E. Every subsequent
node is another knee. Its split determinant is

$$
Ab-Ba=AB-(A+B)D=(-1)^{j-1},
$$

by the Fibonacci Cassini identity. Every one-step variance is therefore
1/(N_j^2*N_(j-1)*N_(j-2)). For any fixed m,

$$
\mathcal M_m^U(j,N_j)=O(F_j^{-4}),\qquad
\frac{U(N_j)-G(N_j)}{N_j}
\longrightarrow\frac1{1+\alpha^2}-\alpha>0.
$$

No admissible policy can repair this family: its choices at every knee
are forced. It has the known geometric descent and terminal values,
but violates actual nesting and actual global upper envelopes. Thus
maximization removes orbit qualification from the *sufficient proof
contract*, while geometric/terminal data alone still cannot supply the
required inequality. Further properties of actual C must be used.

**Exact finite policy evidence.** On every one of the130891 positive-defect
roots144..131071, the greedy policy's four-generation variance satisfies

$$
V_4^{\mathrm{greedy}}(j,N)\ge\left(\frac{C(N)-G(N)}N\right)^2.
$$

The finite minimum ratio is1261233567928603/1069661546553600,
approximately1.17910, at N=1384. Its minimum quartic ratio is
8021464423967/23247511560, approximately345.046, at191. These are
exact rational finite statements. The stronger quadratic observation
motivates checking a q=2 policy criterion alongside q=4; neither is
a uniform theorem or a proved global rate.
The three-generation greedy quadratic ratio is below1 at11631
(approximately0.487651); thus the four-generation kappa1 finite
observation is not justified by simply shortening the horizon. A
different constant or policy remains a separate question.

For the one-step greedy maximum, kappa1 already fails at125952:
R_26(125952)={77846}, D=1662, and the quartic ratio is
4645051457352564736/49606335160931882511, approximately0.0936383.
Thus allowing every scalar-valid geometric split does not make a
one-step kappa1 proof automatic. Further generations materially change
the finite bound.

Through4096, all44425 scalar-valid geometric splits are enumerated
independently, checking that the extremal candidates maximize local
variance. Full four-generation Bellman maxima are computed and dominate
the greedy variance on all3936 positive-defect roots144..4096.
The checker also verifies the unique upper-cap knee split through
order16 and its maximal-variance counterexamples at orders20,30,40,60,90.
No prescribed-orbit or global-closure theorem is inferred from these
policy experiments.

### Two-split moment policies and cycle-average dispersion

There is a larger sufficient interface for the asymptotic problem.
A random split need only preserve or increase the scalar value **in
expectation**. Individual choices may have a different complementary
sum from C(N). The golden-defect orbit equations then give a quadratic
cycle-average certificate, and a local linear program reduces any
successful mixture to at most two splits.

This is a proof policy for the already defined C. It does not replace
its prescribed endpoint, determine C(N) from unknown children, or close
the full recursive evaluation interface. Five digit labels do not
supply the scalar profiles and context used below.

**Moment-admissible policies.** At a closed state (j,N), let K_j(N)
be all geometrically captured splits:

$$
K_j(N)=\{a:A\le a\le S,\ B\le N-a\le A\},
\quad A=F_{j-1},\ B=F_{j-2},\ S=A+B.
$$

Put H(a)=C(a)+C(N-a). Choose weights w_a>=0 with

$$
\sum_a w_a=1,\qquad \sum_a w_a H(a)\ge C(N). \tag{M.1}
$$

After choosing a, descend to a or N-a with the usual size-biased
probabilities. Preserve inherited labels and stop at orders4/5.
The selected actual split makes (M.1) feasible at every internal state.

Then X=F_j/N is still a martingale, and
Z=(C(N)-alpha*N)/N is a submartingale. Indeed, every fixed split has
conditional mean X equal to S/N, whereas the mean Z is
`[sum(w_a*H(a))-alpha*N]/N`. If equality holds in (M.1), Z is a
martingale. The conditional X variance is exactly

$$
\sum_a w_a\,v(j,N;a), \tag{M.2}
$$

since all splits have the same conditional X mean. There is no additional
variance from randomizing between those means.

Define E_0=0, with the same stopping convention as V, and

$$
E_m(j,N)=\max_{w\text{ satisfying (M.1)}}\sum_{a\in K_j(N)}w_a
\left[v(j,N;a)+\frac aN E_{m-1}(j-1,a)
                  +\frac{N-a}N E_{m-1}(j-2,N-a)\right]. \tag{M.3}
$$

Finite backward induction gives an attaining policy. In particular
E_m>=M_m>=V_m, where M is the preceding scalar-valid Bellman maximum.
If fixed m>=1,q>=1,kappa>0,J exist with

$$
E_m(j,N)\ge\kappa\left(\frac{C(N)-G(N)}N\right)^q
\quad\text{for every closed actual-value state with }j\ge J, \tag{M.4}
$$

then C(n)-alpha*n=O(n/(log n)^(1/q)). The previous block proof applies:
X has the same bounded total variance; the submartingale now gives
E[Z at a block start]>=Z_0, which is the direction that proof needs.
The upper rounding inequality G(N)-alpha*N<alpha gives the same
lower bound on E[(C(N)-G(N))/N], and Jensen and L disjoint blocks
finish the argument. This is a conditional theorem, not a verification
of (M.4) or of a global rate.

**At most two splits suffice, sharply.** More generally, supply any finite
table of geometric splits, scalar readouts H_a and rational rewards R_a,
with some H_a>=C(N). The maximum of sum(w_a R_a) under (M.1) is
attained by either one split with H_a>=C(N), or two splits with

$$
H_-<C(N)<H_+,\qquad
w_- =\frac{H_+-C(N)}{H_+-H_-},\qquad w_+=1-w_-. \tag{M.5}
$$

**Proof.** This is a compact finite linear program. An extreme optimum
with a slack moment constraint has one positive coordinate. With a
binding moment constraint it has at most two: three positive coordinates
admit a nonzero perturbation preserving both normalization and the moment,
so cannot form a vertex. A two-coordinate vertex must strictly bracket
the target; an endpoint equality reduces to one coordinate. QED.

Apply this to the bracketed reward in (M.3), at every occurrence and
remaining horizon. Thus two splits suffice even for an optimal
multi-generation policy. For a supplied five-phase table there are only
five singleton and ten pair options. The readouts, rewards and target
determine an optimizer by exact comparison, with a fixed tie rule;
no additional phase or option label is needed in this supplied-table
model. The weights are derived from the integer readouts. This is not
a minimum total recursive payload or a random-bit sampling bound.
The readout tables, parent value, scales, domains and actual qualifications
remain resources. Each derived weight has O(log N)-bit integer numerator
and denominator. Comparing multi-generation rewards also needs their
exact rational representations; the support bound is not a full optimizer
memory bound. One need not supply basin or depth-phase certificates for
geometrically qualified alternatives.

An actual five-cycle makes the two-support bound necessary. At N=313,
the canonical prescribed cycle and its scalar readout are

$$
(182,190,185,186,191),\qquad H=(210,211,213,204,214),\qquad C(313)=211.
$$

Only phase190 individually preserves211. Among all single phases with
H>=211, phase185 has the greatest local variance. Mixing phase182
with weight2/3 and phase185 with weight1/3 preserves211 exactly and
has still larger variance:

$$
\frac{71476778683}{27655598472320}
>\frac{3869089}{2319905920}
>\frac{321602}{1144767765}.
$$

Direct enumeration of the five singleton and ten pair options verifies
that this mixture is optimal on that table. This is a conditional
two-support minimum on the supplied cycle, not a claim about all
geometric alternatives at N313.

A hand-checkable optimality certificate uses S=233,A=144 in (9.22).
Write v_182,v_185 for the two supporting variances and set
L(H)=v_182+(H-210)(v_185-v_182)/3. The slope is negative, and
direct substitution of the five indices shows v(x)<=L(H(x)) at every
phase, with equality at182 and185. Every admissible mixture therefore
has mean variance at most L(mean H)<=L(211), and the displayed mixture
attains it. This proves optimality without assuming a numerical solver.
Uniform sampling of this cycle has mean readout1052/5<211 and fails
(M.1); the two-point mixture therefore also repairs a failed uniform
mean condition.

**An adjacent-phase quadratic identity.** For every captured pair
x,y=N-C(x) in a closed block j>=6, set

$$
M(x)=AN-Sx,\quad p=A/S,\quad \sigma=A^2-SB\in\{-1,1\},
\quad d(x)=C(x)-G(x).
$$

Then

$$
A M(x)+S M(y)=S^2 C(x)-ASx+\sigma N. \tag{M.6}
$$

Moreover their geometric split variances satisfy

$$
v(j,N;x)+v(j,N;y)\ge\frac1{10}\left(\frac{d(x)}N\right)^2. \tag{M.7}
$$

Neither scalar readout has to equal C(N) for (M.7).

**Proof.** Equation (M.6) is substitution of y=N-C(x). Put
h=C(x)-p*x+sigma*N/S^2, so p M(x)+M(y)=S h. Since
v(j,N;x)>=4M(x)^2/N^4, Cauchy-Schwarz gives

$$
v(j,N;x)+v(j,N;y)
\ge\frac{4S^2 h^2}{N^4(1+p^2)}\ge\frac{h^2}{N^2}. \tag{M.8}
$$

Here p<=5/8, N/S<=1+p, and (1+p)^2(1+p^2)<4. Correct
golden rounding has -alpha^2<G(x)-alpha*x<alpha.
Also |alpha-p|=alpha^j/S, x<=S, alpha^j<1/16,
alpha^2<2/5 and N/S^2<=13/64, for j>=6. Consequently

$$
h>d(x)-\frac25-\frac1{16}-\frac{13}{64}
=d(x)-\frac{213}{320}.
$$

For integral d(x)>=1, this is at least (107/320)d(x), whose
squared coefficient exceeds1/10. For d(x)=0, (M.7) is simply
nonnegativity. This proves the bound. QED.

**Cycle-average certificate.** For any actual captured cycle
x_0,...,x_(ell-1), sum (M.7) around it to obtain

$$
\frac1\ell\sum_i v(j,N;x_i)
\ge\frac1{20\ell}\sum_i\left(\frac{d(x_i)}N\right)^2. \tag{M.9}
$$

If its supplied scalar table and first-child defects satisfy

$$
\frac1\ell\sum_i H(x_i)\ge C(N),\qquad
\frac1\ell\sum_i d(x_i)\ge\theta\,[C(N)-G(N)] \tag{M.10}
$$

for theta>=0, uniform phase sampling is moment-admissible and Jensen gives

$$
E_1(j,N)\ge\frac{\theta^2}{20}
             \left(\frac{C(N)-G(N)}N\right)^2. \tag{M.11}
$$

The two-split optimizer on that cycle attains at least this variance.
For theta=1/2 the constant is1/80, independent of period and cap size.
One can reconstruct an odd cycle using its
[ordered golden-defect word](inverse-reconstruction.md#golden-defect-words-give-a-uniform-cyclic-decoder),
then qualify its actual points, complementary values and (M.10).
Those qualifications are additional information; uniqueness alone does
not supply the mean conditions.

The obstruction is visible even on a proper two-cycle. At N11213,
the prescribed cycle is (6930,6868), its scalar readouts are (7030,7024),
and C(11213)=7030. Condition (M.1) forces probability1 on6930 when
restricted to this cycle. Its first-child defects are62,38 and the
parent defect is100, but the high-variance second phase has a lower
scalar readout. The cycle-policy quadratic ratio is only
11/119924000. This finite small ratio is not an infinite counterexample
to (M.4); it identifies why a cycle-average inequality alone is insufficient.

There is an actual obstruction even in the full geometric domain at
N125952. All4560 geometric readouts lie in[79210,79505], the actual
value is79505, and only split77846 attains it. Thus (M.1) forces that
split under every mixture. Its one-step quartic ratio is
4645051457352564736/49606335160931882511<1, as in the earlier
scalar-valid witness. The larger moment domain still does not give a
one-step kappa1 criterion automatically; further generations or a
different constant remain necessary.

The upper-cap U counterfamily above is also an infinite obstruction to
the enlarged moment criterion. At every knee N_j, every geometric scalar
sum is at most U(N_j), and only the unique knee split attains it.
Thus (M.1) forces all probability onto that split. Consequently
E_m^U=M_m^U=O(F_j^(-4)) for each fixed m, while its relative golden
defect has a positive limit. Random mixtures do not replace the missing
actual-profile restrictions. This concerns U, not the actual C sequence.

Campbell's endpoint recurrence does not have this scalar moment interface.
At N5, b(5)=2 but all four complementary sums are4,3,3,4; even
randomization cannot have mean b(5) in an additive martingale.
Its exact endpoint/parity interface is separate.
An inequality-only additive submartingale would be feasible there, but
the Cloitre criterion relies on its proved nonnegative golden defects,
which Campbell does not have; no Campbell rate follows from this comparison.

The [checker](verification/selector_payload_check.py) compares the
two-support optimizer with an independent full-simplex grid in small
integer tables, checks the actual witnesses by literal endpoint iteration,
and audits (M.6)--(M.11) over independently evaluated selected cycles.
These computations corroborate the written theorems. The mean conditions
fail at some actual roots; no uniform occupation, (M.4), global limit
or decay exponent is asserted.

The finite census through131071 checks677836 adjacent-phase pairs at
131064 roots. Conditions (M.10) with theta=1/2 certify73864 positive-
defect roots, including3661 proper five-cycles and block interiors;
this is not a universal density theorem. Exact four-generation cycle
policies through4096 improve on the scalar-valid cycle maximum at1881
of3936 positive-defect roots. Their minimum quadratic ratio is
1677629509156595629/2454936662461732020, at1886, below1.
The broader geometric policy domain is separate and contains the
previous scalar-valid policies; neither finite comparison proves (M.4).

### Finite prefixes and exact collars do not force convergence

The missing global condition can be isolated more sharply than with U.
There are explicit extensions of arbitrarily late actual C prefixes that
retain G, the upper cap, the exact golden equality set, saturated profiles
and all the proved fixed collars, but whose ratios do not converge.
Thus even these stronger static premises do not supply a uniform actual
or maximal-policy dispersion theorem. The construction is a counterfamily
to those premises; it is not the prescribed nested C recurrence.

**A nonnegative-carry split always exists nearby.** For every N and two
consecutive admissible indices a,a+1, at least one satisfies

$$
G(a)+G(N-a)\ge G(N).
$$

Indeed put alpha=1/phi and theta={alpha(N+2)}. The sum of the two
floors at a,N-a is G(N+1), or G(N+1)-1 when
`{alpha(a+1)}>theta`. A negative G carry therefore requires
G(N+1)=G(N), theta>=alpha, and {alpha(a+1)}>theta. At the next
index the fractional part becomes `{alpha(a+2)}={alpha(a+1)}+alpha-1`
and is less than alpha<=theta. Its carry is zero. QED.

Fix J>=25 and let K=F_J. Define W_J(N)=C(N) for1<=N<=K.
For N>K use its natural block S=F_j<=N<=F_(j+1), with
A=F_(j-1),B=F_(j-2), and the geometric interval

$$
l=\max(A,N-A),\qquad h=\min(S,N-B).
$$

Take floor(AN/S) and ceil(AN/S), clipped to[l,h], discard candidates
with negative G carry, and choose the remaining index closest to AN/S;
break ties by the larger index. Denote it s_J(N), and put

$$
W_J(N)=W_J(s_J(N))+W_J(N-s_J(N)).
$$

The choice depends only on N, its order and the known G arithmetic.
It is shared at every occurrence of the same physical N. At Fibonacci
endpoint aliases the geometric domain is a singleton, so the definition
is independent of that alias.

For interior S<N<S+A both neighboring integers are in[l,h]. To see this,
write N=S+u,1<=u<=A-1. The ideal split is A+A*u/S. Cassini gives
`A^2-S*B=+/-1`, so A*(A-1)<=S*B and
`(A-B)*S-B*(A-1)>=B-1`. Together with0<A/S<1, these establish all
four geometric bounds. The carry lemma leaves a candidate. At either
endpoint the unique Fibonacci split has zero carry. Thus W is total,
and its chosen split satisfies

$$
|AN-Ss_J(N)|\le S. \tag{9.25}
$$

**Bounds, saturation and finite collars.** For every N,

$$
G(N)\le W_J(N)\le U(N).
$$

The lower bound propagates because the chosen carry is nonnegative.
For the upper bound write N=S+u,s_J(N)=A+r,N-s_J(N)=B+q,
so r,q>=0,r+q=u. The two child caps satisfy

$$
\min(r,F_{j-3})+\min(q,F_{j-4})\le\min(u,F_{j-2}),
$$

giving the parent cap by induction. Both statements hold in the actual
prefix. The same profile sum propagates the actual saturated lower
barrier: for all closed blocks of order j>=23,

$$
W_J(F_j+u)-F_{j-1}\ge\min(u,32).
$$

Consequently W_J(F_j+u)=F_(j-1)+u for0<=u<=32,j>=23.
It also retains W_J(F_k-v)=F_(k-1) for0<=v<=12,k>=23.
For the latter assertion, the two distances from the children's upper
anchors are nonnegative and sum to v. Hence they are at most12,
and the flat actual seed collars propagate. Orders at the cutoff are
at least J-2, so all needed seed collars have order at least23.

**The exact equality set is unchanged.** Let E_W=W_J-G. At a new node,

$$
E_W(N)=E_W(a)+E_W(N-a)+G(a)+G(N-a)-G(N),
$$

with all terms nonnegative. Equality thus requires two zero children
and zero carry. By induction the possible first zero child in[A,S]
is A,A+1,S, or S-1 when j is odd; the possible second in[B,A]
is B,B+1,A, or A-1 when j-1 is odd. Exceptional seed zeros are below
these high-order blocks.

Mixed lower/upper pairs cannot obey (9.25). For pairs near A,A, their
determinant has magnitude at least A*(A-B)-S>S; for pairs near S,B,
it has magnitude at least B^2-S>S. These inequalities hold for j>=8.
Two lower pairs give N=S,S+1,S+2; the last has carry one since
G(S+2)=A+1 whereas the child sum is A+2. Two upper pairs give
N=F_(j+1),F_(j+1)-1,F_(j+1)-2. The last would require j and j-1
both odd for both children to be zero, which is impossible.
The already proved collars determine the remaining minus-one case:
W(F_k-1)=F_(k-1), equaling G exactly when k is odd. This proves

$$
\{N:W_J(N)=G(N)\}
=\{F_k,F_k+1:k\ge2\}\cup\{F_k-1:k\ge3\text{ odd}\}
 \cup\{11,24,25,59\}.
$$

**Every fixed width eventually becomes exact.** The property is stronger
than retaining the finite band. For a positive offset u, (9.25) gives
child offsets at most `(2/3)*u+1`. After d steps they are at most
`(2/3)^d*u+3`. Put

$$
d_+(u)=\min\{d\ge0:(2/3)^d u\le29\}.
$$

If j>=J+2d_+(u), every path to the actual-prefix boundary has at least
d_+(u) steps; its leaf offset is at most32, where the actual prefix
is linear. Recombining the two Fibonacci baselines and offsets gives

$$
W_J(F_j+u)=F_{j-1}+u.
$$

The bound also ensures u<=F_(j-1), since
`F_(J+2d-1)>=2^d F_(J-1)>=29*(3/2)^d`.
For an upper-anchor gap v, the Cassini error at the proportional center
and rounding give child gaps at most `(2/3)*v+2`. Define

$$
d_-(v)=\min\{d\ge0:(2/3)^d v\le6\}.
$$

At k>=J+1+2d_-(v), all boundary gaps are at most12, proving
W_J(F_k-v)=F_(k-1). These infinite collar statements concern W;
the actual moving-plateau theorem independently proves all fixed negative widths.
In particular its lowest five legal digit-window responses are exactly
the same as C at every anchor of order at least23: their interaction
coefficient is zero. This static agreement does not identify the
prescribed inner selection.

**The exact moving top plateau excludes this counterfamily.** The
[moving-plateau theorem](exact-collars.md#exact-moving-negative-plateau-and-arithmetic-closure)
now proves the full-block zero-support law L_k=floor(2k/3)-3 for actual C.
It is stronger than eventual flatness at each fixed negative gap.
Every extension W_J with J>=26 violates that law already at

$$
N=F_{J+1}-v,\qquad v=L_{J+1}+1=\lfloor2(J+1)/3\rfloor-2.
$$

Indeed its two chosen child gaps r,q below the upper anchors F_J,F_(J-1)
are nonnegative, sum to v, and satisfy max(r,q)<=(2/3)v+2 by the
rounding estimate above. For J>=26,

$$
\max(r,q)\le\frac{4J+10}{9}
\le\frac{6J-42}{9}\le L_{J-1}\le L_J.
$$

Both children belong to the unchanged actual prefix. Their actual plateau
values are F_(J-1) and F_(J-2), so W_J(N)=F_J. But N lies one gap
outside the actual top plateau, giving C(N)<F_J. Thus no member of this
arbitrarily late-prefix family satisfies the new moving-profile constraint.
The checker verifies the concrete J25/J26 violations and exact arithmetic
child-gap bounds at J=26,...,90; the infinite exclusion is proved by the
displayed estimates. A uniform dispersion inequality for profiles satisfying
this constraint still requires a proof; excluding this counterfamily alone
does not supply it.

**Certified ratio envelopes are inherited.** Suppose actual C has
ell<=C(N)/N<=beta for N>=M, and choose J with F_(J-2)>=M.
Every terminal index of a W descent from N>K lies in[F_(J-2),F_J].
The parent ratio is a size-weighted average of those actual terminal
ratios, so W has the same envelope for every N>=M. Thus J>=31
preserves even the current upper bound8900/13459 for N>=349525.
Increasing J also preserves any desired finite actual prefix. None of
these choices prevents the obstruction below.

**A persistent positive defect at Fibonacci knees.** Put
N_j=F_j+F_(j-2). Its nearest proportional split is N_(j-1), since
its determinant has absolute value one. Moreover

$$
G(N_j)=N_{j-1},\qquad G(N_{j-1})+G(N_{j-2})=G(N_j).
$$

The first identity follows by lowering the two nonadjacent Fibonacci
weights, or directly by Binet's formula. Therefore the nearest candidate
has zero G carry and is chosen. For j>=J,

$$
W_J(N_j)=W_J(N_{j-1})+W_J(N_{j-2}).
$$

The two actual seed defects at orders J-2,J-1 are strictly positive,
by the exact equality set. Let D_h=C(N_h)-G(N_h) at those seeds.
The continued defect has the Fibonacci recurrence, and hence

$$
\frac{W_J(N_j)}{N_j}\longrightarrow\alpha+\Delta_J,
\qquad
\Delta_J=\frac{D_{J-1}+\alpha D_{J-2}}
                  {N_{J-1}+\alpha N_{J-2}}>0.
$$

On the other hand W_J(F_j)=F_(j-1) and W_J>=G, so its liminf
ratio is alpha. Its ratio therefore does not converge.
The fixed-horizon maximal-policy criterion applies to any scalar function
with these bounds and nonempty geometric additive domains. If it held
uniformly for W at any fixed m,q>=1,kappa>0, it would force convergence
to alpha, a contradiction. Thus even the maximal dispersion inequality
fails uniformly somewhere at arbitrarily high orders in this family.
This last conclusion does not locate those optimizing states, and does
not assert failure for actual C.

**A concrete failure of prescribed selection.** For J=25, W agrees with
actual C through75066. Its first difference is N=75067:

```text
chosen geometric split: 46394,
W(46394)+W(28673)=28683+17727=46410,
prescribed nested split: 46368,
W(46368)+W(28699)=28657+17750=46407.
```

The alternative split lies in the inner two-cycle(46384,46394), while
the prescribed start reaches a different cycle. Both child-value sums
use the identical actual prefix. This is exactly where the geometric
extension ceases to be the original recurrence, rather than an error
in its scalar descent or its golden bounds.

The knee seeds at orders23,24 are26111 and42202, with golden defects
1635 and2599. Its knee ratio tends to

$$
\frac{42202+\alpha\,26111}{64079+\alpha\,39603}
=0.658793805466\ldots>\alpha.
$$

The checker builds the J25 and J26 extensions through2^20, verifies
their bounds, exact zero set, saturation and available collar thresholds,
and replays each first prescribed failure literally. Consecutive-carry
contexts through4096 are exhausted, and huge knee values and selected
splits through order90 are checked by exact arithmetic. The nonconvergence
and arbitrary-prefix conclusions have independent written proofs; they
are not extrapolations from those finite tests.

### Exact small-cap closure still does not force convergence

The moving top plateau excludes W_J above. The stronger obstruction here
preserves that plateau, all four exact cap sublevels, their actual local
selection rules, and the cap-budget and cap-dependent dispersion bounds.
Those premises still do not imply convergence. This is an assigned additive
extension, not another solution of Cloitre's prescribed recurrence.

**Theorem.** For every J>=26 there is an integer-valued H_J agreeing with C
through F_J, with a shared geometric additive split at every later index,
such that:

1. G<=H_J<=U, the exact G-equality set is unchanged, and H_J(F_k)=F_(k-1).
   Every certified actual ratio envelope is inherited when its threshold
   is at most F_(J-2).
2. On every full closed upper-anchor block k>=21, the cap sublevels0..3
   and their values are exactly those of C. The four subsequent positions
   also agree with C and have cap4. On newly extended blocks, the actual
   prescribed iteration under H_J selects the same arithmetic endpoints
   as C throughout the cap0..3 domain.
3. The quadratic cap budget, bounded-cap ratio convergence, and the linear
   and logarithmic cap-dependent dispersion theorems apply to its assigned
   geometric descent, with their existing domains and constants. All fixed
   positive and negative collars eventually have their exact C values.
4. Nevertheless liminf H_J(N)/N=alpha and its Fibonacci-knee ratios tend
   to alpha+Delta_J with Delta_J>0. At those knees every fixed-horizon
   assigned variance tends to zero while the relative golden defect stays
   positive. Thus no uniform fixed-horizon dispersion bound follows from
   these combined premises.

The asserted sublevels include both Fibonacci endpoint aliases. Only
statement2 claims agreement with prescribed nesting outside the original
prefix; high-cap splits remain assigned choices.

**Construction.** Use the widths L_k,R_k,S_k,Z_k and exact shift delta_k(v)
from [the cap0..3 theorem](exact-collars.md#two-higher-cap-levels-and-their-phase-selected-closure).
Put H_J(N)=C(N) for N<=F_J. At a later index use the unique upper order
F_(k-1)<N<=F_k and write

$$
A=F_{k-1},\quad B=F_{k-2},\quad H=F_{k-3},\quad
v=F_k-N,\quad d_k=Z_k-Z_{k-1}\in\{3,4\}.
$$

Choose a first child a by the following ordered rule, and set
H_J(N)=H_J(a)+H_J(N-a):

- If v<=Z_k, take a=A-v+delta_k(v).
- If Z_k<v<=Z_k+4, take a=A-v+d_k.
- Otherwise consider floor(BN/A) and ceil(BN/A). Admit a candidate a
  only if its G carry is nonnegative and
  `[B-H_J(a)]+[H-H_J(N-a)]>=4`. Among admitted candidates choose
  the closest to BN/A, breaking a tie by the larger a.
- If none is admitted and v<=H+d_k, take a=A-v+d_k.
- In the remaining case take a=B if its G carry is nonnegative, and
  a=B+1 otherwise.

All children are earlier physical indices. No branch depends on a future
value, and repeated occurrences of an index use the same split.
For k>=27, the size bounds Z_k+4<H, L_(k-2)>=4 and F_(k-4)-1>=4
hold at the first order and persist; these keep the displayed strip and
transport children inside their closed blocks.

**Totality and profile preservation.** The first two branches have
child gaps r=v-delta,q=delta with delta<=4. In the small-cap branch,
the exact arithmetic selector has first cap e and second cap0. For the
four-point strip write v=Z_k+w,1<=w<=4. Its first gap is
Z_(k-1)+w and its second gap is d_k<=4. The first child has cap4 and
the second cap0; this agrees with actual C by the level3 shelf theorem.
The seed contains the required full profiles at orders J-1 and J.

For an interior index both neighboring proportional integers are geometric,
by the consecutive-Fibonacci inequalities proved for W_J. They satisfy
B<=a<=A and H<=N-a<=B. At v=0 the first branch supplies the unique
Fibonacci split. If no proportional candidate is admitted, the transport
branch has a>=B and first gap
`v-d_k>Z_(k-1)+4`, so its first cap is at least4; its second cap is0.
The final branch is geometric: v>H+d_k gives N<2B-d_k, while N>A
gives N-B>=H+1. The consecutive-carry lemma supplies B or B+1.
Their first caps are F_(k-4) or F_(k-4)-1, both at least4.
Here H_J(B)=H and H_J(B+1)=H+1 are inductive endpoint identities;
their propagation is checked below. Every branch is therefore defined,
and every outside-band value has cap at least4.

The geometric upper-cap inequality used for W_J gives H_J<=U in every
branch. For G, the first two branches equal C; the proportional and final
branches use nonnegative carry. In a transport branch, its second child
B-d_k has value H and golden defect at least1. Every G carry is at least
-1, so G<=H_J also follows there. Additivity gives exact nonnegative
integer child-cap conservation. These steps prove the full profile
classification and the bounds simultaneously by induction on N.

**Equality set and endpoint identities.** In a nonnegative-carry branch,
equality with G requires two golden-zero children and zero carry. For a
proportional split the determinant bound |BN-Aa|<=A excludes mixed
lower/upper anchor pairs by the argument for W_J. The lower pairs give
N=A,A+1,A+2, with positive carry at A+2; upper pairs give only the
already copied upper-anchor zeros. In particular at N=A+1 the closest
candidate is a=B+1,b=H, has inherited cap H-1>=4 and carry0, and gives
H_J(A+1)=B+1. The identity H_J(F_k)=F_(k-1) follows from v=0.

For a transport split its first child lies in
`[B,A-Z_(k-1)-5]`; its only possible golden zeros are B,B+1.
If it is not zero, its golden defect and the second child's defect are
both at least1, so even a carry -1 leaves a positive parent defect.
If it is B+epsilon,epsilon in{0,1}, then N=2B-d_k+epsilon and
the assigned value is 2H+epsilon. Binet's identity
`alpha B=H+(-1)^(k-1)*alpha^(k-2)` gives
G(N)<=2H-1 for d_k>=3,k>=27, so equality is again impossible.
In the final branch the second child is below B-4; its only possible
golden zeros are H,H+1. Thus only the same lower pairs can occur.
The copied bands agree with C. This proves the complete equality set
and the endpoint identities required in the preceding induction.

**Actual low-cap selection and inherited closure.** At v<=Z_k, capture
uses only G, U and Fibonacci values. Its local gap domain is0..v;
the lower profile there agrees with C because
`Z_k<=Z_(k-1)+4`. Every fixed point and frontier two-cycle is therefore
the same. For a frontier, full sublevel classification gives exactly
the exterior side inequalities used in the original phase proof. The
predecessor H_J(N-1)=C(N-1) is copied through the four-point strip,
so the depth parity is the same as well. The capture budget is at most
4k+v+1<8k, whereas the depth is at least B>8k for k>=27.
Thus the prescribed iteration actually reaches and selects the stated
endpoint under H_J; this is not an assumption about its high-cap choices.
The same arithmetic five-row closure and phase-free small-cap variance
kernel apply without alteration.
In particular the entire
[persistent canonical interaction family](exact-collars.md#a-persistent-interaction-on-canonical-index-words)
has the same five readouts, interaction coefficient1, root endpoints and
inherited first-child signal under H_J: those roots and their descendants
have cap0 or1. Matching this feature interaction therefore does not supply
the missing global condition either.

The [cap-budget proof](recursive-descent.md#a-quadratic-enclosure-for-every-bounded-cap-level)
uses just exact zero support and geometric integer cap conservation;
its finite small blocks are unchanged. The linear and logarithmic
dispersion inductions additionally use the same arithmetic cap0..3 kernel.
They therefore apply to the assigned descent of H_J. Their cap-dependent
horizon, constants and order thresholds remain part of each conclusion.

For positive natural offsets, the saturation proof for W_J uses only
geometry and addition, and gives
`H_J(F_j+u)-F_(j-1)>=min(u,32)` for j>=23. Hence offsets0..32
are exactly linear. For any fixed u choose K>=J+2 with F_(K-2)>=u+4.
At natural orders h>=K and offsets at most u, every geometric candidate
has inherited cap sum at least F_(h-2)-u>=4. A nonnegative-carry nearest
candidate is therefore admitted. For a positive offset, the upper gap
is beyond Z_(h+1)+4: it is at least F_(h-3)+4, with
F_(h-3)>Z_(h+1) at these orders. Thus no copied-band branch preempts
the nearest rule. Its child offsets are at most
`(2/3)*u+1`. After d steps they are at most `(2/3)^d*u+3`.
Choosing d with `(2/3)^d*u<=29` and starting at j>=K+2d puts every
descendant into the copied linear band before an order falls below K.
Recombination proves the eventual exact positive collar. Every fixed
negative gap lies eventually in the moving zero plateau. Ratio envelopes
are size-weighted averages of unchanged prefix leaves, as for W_J.

**Knee obstruction.** Put N_j=F_j+F_(j-2). Its upper gap is
F_(j-3)>Z_(j+1)+4 for j>=J. The nearest proportional split is N_(j-1),
with determinant of absolute value1 and zero G carry. Both actual seed
knees at orders J-2,J-1 lie beyond their cap3 bands; their inherited caps
are at least4. Hence the nearest knee split is admitted, and induction gives

$$
H_J(N_j)=H_J(N_{j-1})+H_J(N_{j-2})\quad(j\ge J).
$$

The inherited cap sum also obeys this Fibonacci recurrence, so it never
drops below the admission threshold. The positive seed golden defects
D_h=C(N_h)-G(N_h) give

$$
\frac{H_J(N_j)}{N_j}\longrightarrow\alpha+
\frac{D_{J-1}+\alpha D_{J-2}}{N_{J-1}+\alpha N_{J-2}}
=\alpha+\Delta_J>\alpha.
$$

The anchors and G lower bound give liminf alpha. On a knee descent of any
fixed length t, all nodes are knees at orders j,j-1,...,j-2(t-1).
Each local variance has numerator1 and denominator N^2ab, so it is
O_t(N_j^(-4)). Size-biased probabilities sum to1 at each level; therefore
the accumulated assigned V_t is O_t(N_j^(-4)). This explicitly refutes a
fixed-horizon bound by any positive power of the relative golden defect
for this family. It does not refute such a bound for actual C. QED.

**Independent audit and a recurrence failure.** The
[selector checker](verification/selector_payload_check.py) tests J26 through
2^20 against actual C, verifies both fallback constructions independently
of whether the main rule chooses them, checks actual low-cap selected
endpoints under H_J, and replays the first discrepancy by literal nesting.
At N=121460 the assigned split75067 gives H_J(N)=75089, whereas
depth75091 selects75025 and gives75092. The prefix through121459 agrees
with C. This is a concrete failure of high-cap prescribed nesting.
The knee seed values42202,68155 give the limit

$$
\frac{68155+\alpha\,42202}{103682+\alpha\,64079}
=0.657691108044\ldots>\alpha.
$$

Finite arithmetic checks through order90 corroborate the knee admission
and variance identities; all infinite assertions above have written proofs.
The obstruction identifies a necessary use of actual orbit restrictions
outside the small-cap domain, not a sufficient full recursive interface.
Campbell's completed power-of-three formula supplies endpoints and parity
at every index; its nonadditive recurrence does not have this integer
two-child cap flow. That family remains a comparison for a complete
selector interface, rather than a recipient of this counterconstruction.

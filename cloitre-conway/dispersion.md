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
- [Additive dispersion policies without orbit qualification](#additive-dispersion-policies-without-orbit-qualification)
- [Finite prefixes and exact collars do not force convergence](#finite-prefixes-and-exact-collars-do-not-force-convergence)

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
For every phase in the unique prescribed basin, its two points have
the form

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

This proof connects arithmetic recursive closure to Benoît Cloitre's
dispersion route. Here every complementary gap is at most2, so the
proportional-split cancellation of M cannot occur. In wider blocks,
large complementary gaps can approach that cancellation ratio; controlling
their accumulated variance still requires new actual-profile restrictions.

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
`0<=G(N)-alpha*N<alpha` imply at every block start

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

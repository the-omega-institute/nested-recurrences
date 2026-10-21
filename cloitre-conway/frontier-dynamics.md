# Contact frontiers, first capture, and the prescribed clock

[Conway guide](README.md) · [Contact-loss budget](dispersion.md#an-exact-budget-for-the-outermost-cap-contacts)

The outermost cap contacts have a limiting relative width b. This note proves
that b vanishes exactly when the prescribed orbits at those contacts take
increasingly many steps to enter their captured intervals. It also proves
that an isolated contact satisfying a one-sided barrier forces a precisely
measured adjacent downward jump within five inputs at the next level.
Neither result establishes b=0 or full convergence.

We use Cloitre's recurrence with its prescribed start and depth:

$$
C(1)=C(2)=1,\quad T_n(x)=n-C(x),\quad
g(n)=T_n^{C(n-1)}(n-1),\quad C(n)=C(g(n))+C(n-g(n)).
$$

Write alpha=(sqrt(5)-1)/2 and phi=1/alpha. The inputs are the
[golden bounds and child capture](golden-proof.md), the
[invariant anchor intervals](fibonacci-collars.md#1-all-cycles-near-a-fibonacci-index),
and the [exact left plateau](exact-collars.md#exact-moving-negative-plateau-and-arithmetic-closure).
For inherited block labels put

$$
E_j(u)=F_{j-1}+u-C(F_j+u),\quad 0\le u\le F_{j-1},\qquad
t_j=\max\{u:E_j(u)=0\}.
$$

The global cap gives 0<=E_j(u)<=u and E_j(u)>0 for u>F_(j-2).
At an actual selected split the two native child profiles add exactly.
The [contact-loss budget](dispersion.md#an-exact-budget-for-the-outermost-cap-contacts)
proves t_j/F_(j-1)->b, with 0<=b<=alpha.

## A lower barrier from two finite profiles

Fix K>=8 and define

$$
c=\max\left\{\frac{t_K}{F_{K-1}},\frac{t_{K+1}}{F_K}\right\},
\qquad \gamma=\frac1{F_K(1-c)}.
$$

Then c<1, 0<gamma<=1, and throughout every native profile at j>=K,

$$
E_j(u)\ge\gamma(u-cF_{j-1})_+. \tag{1}
$$

Here x_+=max(x,0). At either base level, a positive right-hand side
means u>t_j, so the integer E_j(u) is at least one; the right-hand side
is at most gamma*(1-c)*F_K=1. At subsequent levels, child capture gives
legal native arguments s,u-s, and

$$
\begin{aligned}
E_j(u)&=E_{j-1}(s)+E_{j-2}(u-s)\\
&\ge\gamma(s-cF_{j-2})_++\gamma(u-s-cF_{j-3})_+\\
&\ge\gamma(u-cF_{j-1})_+.
\end{aligned}
$$

The first induction parents are at least F_(K+2)>=55. The integer
gap between each base frontier and its native right endpoint also gives
F_K*(1-c)>=1. This proves all the stated constants.

## Uniform entrance above the barrier

For n=F_k+t, 0<=t<=F_(k-2), write A=F_(k-1), B=F_(k-2),
y_r=T_n^r(n-1), and define the **first-capture rank**

$$
\rho(n)=\min\{r:y_r\in[A,A+t]\}.
$$

This is first entrance into the invariant interval; the orbit may have
a further transient inside it before reaching a cycle.

**Theorem.** Choose epsilon>0 with c+epsilon<1, put
eta=min(gamma*epsilon,1/3), and choose an integer m with alpha^m<=eta/2.
If

$$
k\ge\max(K+1,10),\quad
(c+\varepsilon)B\le t\le B,\quad
B\ge\frac{2}{(1-\alpha)\eta},
$$

then rho(n)<=2m+1. Every orbit point from rank rho(n)+2 onward satisfies

$$
\eta B\le y_r-A<t-\alpha\eta B+1. \tag{2}
$$

Every cycle of T_n lies in this smaller interval, regardless of its period.

**Proof.** For a permitted high argument A+u<n set
widehat_E(u)=B+u-C(A+u). On t<=u<=B, (1) gives
widehat_E(u)>=gamma*epsilon*B>=eta*B. If u>=B, the next-block cap
C(A+u)<=A+u-B gives widehat_E(u)>=2B-A=F_(k-4)>=B/3.
Thus the same bound holds at every exterior high point.

The comparison envelopes give C(y)<=B for y<A, and C(y)>=B+1 for
y>A. Until capture, even ranks are therefore above A+t and odd ranks
below A, starting from y_0=A+t+B-1. Write exterior successive points as
A+t+v_i and A-z_i. Their exact relation is

$$
z_i=v_i-\widehat E(t+v_i)\le v_i.
$$

If the following point remains exterior, its overshoot is
v_(i+1)=B-C(A-z_i)<alpha*z_i+1<=alpha*v_i+1. This uses the global
lower comparison C(x)>alpha*x-alpha^2 and
B-alpha*A=(-1)^(k-1)*alpha^(k-1). Starting at v_0=B-1, an orbit still
outside at rank 2m has

$$
v_m<\alpha^m B+\frac1{1-\alpha}\le\eta B.
$$

Its next offset is widehat_E(t+v_m)-v_m>0 and, by the lower comparison
at points above A, at most t-1. It has entered [A,A+t].

On that interval the offset map is H(u)=t-u+E_(k-1)(u). Since gamma<=1,
t-u+gamma*(u-cB)_+ is nonincreasing in u. Its value at t proves
H(u)>=eta*B; also H(u)<=t. The global lower comparison gives
H(u)<t-alpha*u+1. Applying these inequalities twice proves (2), and
they preserve the smaller interval. Every cycle is captured and has
predecessors on its cycle, proving the last assertion. QED.

## The first-capture dichotomy

**Theorem.** At n_k=F_k+t_k,

$$
\boxed{b=0\quad\Longleftrightarrow\quad\rho(n_k)\longrightarrow\infty.} \tag{3}
$$

If b>0, the ranks are eventually uniformly bounded, and the reached
cycles stay a fixed positive fraction of F_(k-2) away from both capture
endpoints.

**Positive width.** The constants c=c_K from (1) tend to b, whereas
t_k/F_(k-2)->b/alpha>b. Choose fixed K and epsilon with
c_K+epsilon<min(b/alpha,1). The preceding theorem applies for every
sufficiently large k with the same m and eta. The strict upper endpoint
in (2) stays a positive fraction away from t_k for large k.

**Inverse localization.** We first prove

$$
C(z_k)=F_{k-2}+o(F_{k-2})
\quad\Longrightarrow\quad
z_k=F_{k-1}+o(F_{k-2}). \tag{4}
$$

Let L_j(u)=F_(j-1)-C(F_j-u), 0<=u<=F_(j-2). The exact plateau theorem
says its zeros are precisely 0<=u<=w_j, where w_j=floor(2j/3)-3.
For J>=9 define

$$
a=\max\left\{\frac{w_J}{F_{J-2}},\frac{w_{J+1}}{F_{J-1}}\right\},
\qquad \lambda=\frac1{F_{J-1}(1-a)}.
$$

Then

$$
L_j(u)\ge\lambda(u-aF_{j-2})_+\qquad(j\ge J). \tag{5}
$$

The base is the same integer argument as for (1). For an actual parent
F_j-u, the captured children are F_(j-1)-v and F_(j-2)-w, with v+w=u,
0<=v<=F_(j-3), 0<=w<=F_(j-4), and
L_j(u)=L_(j-1)(v)+L_(j-2)(w). This proves (5) by induction.
Because w_j/F_(j-2)->0, for any fixed sigma>0 choose J with a<sigma/2.
Then u>=sigma*F_(j-2) implies L_j(u)>=lambda*sigma*F_(j-2)/2.

The lower comparison in (4) first gives z_k<=F_(k-1)+o(F_(k-2)).
The cap excludes z_k<=F_(k-2), where C(z_k)<=F_(k-3). In the remaining
left block, a distance at least epsilon*F_(k-2) below F_(k-1) would
give a proportional deficit by (5), contradicting the premise of (4).
This proves (4).

**Zero width.** If b=0, then t_k=o(F_(k-2)). Suppose first-capture ranks
were bounded along an infinite subsequence. Restrict to one fixed rank r.
At capture y_r=A+o(B), so C(y_(r-1))=n_k-y_r=B+o(B). By (4),
y_(r-1)=A+o(B). Repeating backward r times gives y_0=A+o(B), contrary
to the prescribed start y_0=A+B+t_k-1. Hence the ranks tend to infinity.
Together with the positive-width conclusion this proves (3). QED.

## An isolated gated frontier forces an adjacent drop

Put R_j(u)=C(F_j+u)-F_(j-1)=u-E_j(u). A frontier r=t_j is **gated** if

$$
R_j(u)\ge r\qquad(r\le u\le F_{j-1}). \tag{6}
$$

**Theorem.** Suppose j>=10,
r>max(4,t_(j-1)), r+4<=F_(j-1), both E_j and E_(j-1) vanish on 0..4,
and (6) holds. Put delta=E_(j-1)(r)>0 and n_d=F_(j+1)+r+d, 0<=d<=4.
Then the actual depth h=C(n_d-1) selects

$$
g(n_d)=\begin{cases}F_j+r,&h\text{ even},\\F_j+d,&h\text{ odd},\end{cases}
\qquad
E_{j+1}(r+d)=\delta\,\mathbf1_{\{h\text{ odd}\}}. \tag{7}
$$

For at least one d in 0..3,

$$
\boxed{C(n_d)-C(n_d+1)=\delta-1.} \tag{8}
$$

**Proof.** In offsets from F_j the map is H_d(u)=r+d-R_j(u), extending
R_j to every permitted argument. The gate extends to u above its native
block: the lower comparison there gives R_j(u)>=F_(j-2)>=r. For u<=d,
the cap at negative offsets and the exact collar at 0..d give R_j(u)<=d.
Thus the disjoint high region u>=r and low region u<=d map into one
another. The prescribed rank-zero offset F_(j-1)+r+d-1 is high; even
ranks stay high and odd ranks low throughout the transient.

Capture puts every cycle in [0,r+d]. Its low points are in [0,d], where
H_d(u)=r+d-u and H_d^2(u)=u+E_j(r+d-u). For u<d the latter exceeds u
because r is the last zero; the gate also bounds it by d. At u=d it is d.
Consequently the only cycle reachable from the low band is {d,r}.
Cyclic selection of the prescribed depth and its absolute rank parity give
the selected points in (7). Additivity, including the lower collar 0..4,
gives the output defects in (7).

Write E_(j+1)(r+d)=delta*z_d with z_d in {0,1}, and a=F_j+r. For d>=1
the preceding output is a+d-1-delta*z_(d-1), so the exact clock gives

$$
z_d\equiv a+d-1-\delta z_{d-1}\pmod2. \tag{9}
$$

If delta is even, z_1,z_2,z_3 alternate and include a 0-to-1 transition.
If delta is odd, z_(d+2)=1-z_d; the possible five-letter words are
00110, 01100, 10011, 11001. Each contains a 0-to-1 transition. The output
falls by delta-1 at that transition, proving (8). QED.

## Consequence and the remaining obstruction

If b>0, choose K in (1) with c<b/alpha. For all sufficiently large j,

$$
E_{j-1}(t_j)\ge\kappa F_{j-2},\qquad
\kappa=\tfrac12\gamma(b/\alpha-c)>0.
$$

All hypotheses of (7) except gating eventually hold: t_j>t_(j-1),
t_j>4, t_j+4<=F_(j-1), and both fixed collars are exact.
Thus every sufficiently large gated level forces an adjacent drop at
N_j=F_(j+1)+t_j+d_j, d_j in 0..3, with

$$
\liminf_{\substack{j\to\infty\\j\ {\rm gated}}}
\frac{C(N_j)-C(N_j+1)}{N_j}
\ge\frac{\kappa}{\varphi^3+b/\alpha}>0
$$

if there are infinitely many gated levels. In particular, if the forward
drawdown Q_C(N)=max({0} union {C(u)-C(v):1<=u<v<N}) is sublinear, then
a positive-width frontier must eventually be ungated.

Gating does not follow from being the last contact. Already t_9=8,
C(42)=29 and C(43)=28, so R_9(9)=7<8. The proof does not cover such
frontiers. Bounded first capture also leaves the interior transient and
the residue of the prescribed clock on the reached cycle uncontrolled.
These are actual remaining gaps in proving cumulative contact erosion.

## Independent checks

The [checker](verification/frontier_dynamics_check.py) uses full visited-state
orbits through 131072 and literal values through 2584. Its
[compact output](verification/frontier-dynamics.json) checks the two
minorants at 364120 right-profile and 225013 left-profile positions,
the quantitative entrance bound at 408 inputs, and the interior bounds
at 2075 cycle positions. Seven gated frontiers satisfy the five-input
theorem in this prefix; levels 19..25 satisfy its other hypotheses but
are ungated.

For j=16 the frontier is 40 and delta=E_15(40)=3:

| n | Prescribed depth | Selected offset from F_16 | E_17(n-F_17) | C(n) |
|---|---|---|---|---|
| 1637 | 1025 | 0 | 3 | 1024 |
| 1638 | 1024 | 40 | 0 | 1028 |
| 1639 | 1028 | 40 | 0 | 1029 |
| 1640 | 1029 | 3 | 3 | 1027 |
| 1641 | 1027 | 4 | 3 | 1028 |

The adjacent drop is 1029-1027=delta-1. These finite checks corroborate
the stated theorems; the infinite conclusions follow from the arguments.

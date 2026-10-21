# Contact frontiers, first capture, and the prescribed clock

[Conway guide](README.md) · [Contact-loss budget](dispersion.md#an-exact-budget-for-the-outermost-cap-contacts)

The outermost cap contacts have a limiting relative width b. This note proves
that b vanishes exactly when the prescribed orbits at those contacts take
increasingly many steps to enter their captured intervals. It also proves
that an isolated contact satisfying a one-sided barrier forces a precisely
measured adjacent difference within five inputs at the next level.
Neither result establishes b=0 or full convergence.

A further conditional theorem describes the whole reached frontier cycle:
under sublinear drawdowns on that cycle, its scaled limits consist of at
most two reflected intervals. Its proof uses finite cycle transitivity
before taking limits.

An exact earlier-row feedback theorem also gives terminal-interval
exclusion certificates with the seed and depth kept correlated. The checked
level-20 certificate is uniform over all preceding defects permitted by the
cap. A cross-level estimate on these excluded intervals remains open.

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

This is a strict downward jump when delta>=2; delta=1 forces equal
adjacent outputs.

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
frontiers. Moreover, removing the gate falsifies the five-input conclusion
even when all its other hypotheses hold. At j=21 the frontier is r=203,
delta=E_20(203)=3, and the five inputs 17914..17918 have defects
7,1,3,0,1. Their four adjacent differences are -7,1,-4,0; none reaches
delta-1=2. The source gate fails by only three:
R_21(203)=203, while R_21(207)=200. An error-dependent inequality or a
longer input interval remains possible.

Bounded first capture also leaves the interior transient and
the residue of the prescribed clock on the reached cycle uncontrolled.
These are actual remaining gaps in proving cumulative contact erosion.

## Cycle geometry under small drawdowns

For any contact n=F_k+t>=47 with 0<=t<=F_(k-2), let Gamma be its reached
cycle in offsets from A=F_(k-1). Capture puts Gamma in [0,t]. Put E=E_(k-1) and
H(x)=t-x+E(x). The actual selected offset s is cyclic and satisfies
E(s)=0; its successor is v=t-s. Define D(n)=n-C(n), and let q_C and q_D
be the maximum forward drawdowns of C and D restricted to the integer
arguments A+Gamma. Set q=q_C+q_D, ell=min Gamma and u=max Gamma.

**Finite cycle lemma.** For every primitive period p,

$$
0\le\ell+u-t\le q,\qquad
E(u)\le q_D+2q_C,\qquad
\max_{x\in\Gamma}E(x)\le2q,\qquad
|H^2(x)-x|\le2q. \tag{10}
$$

Every orbit S of H^2 on Gamma has consecutive spatial gaps at most 2q.
Its Hausdorff distance from the real interval [min S,max S] is at most q.
For odd p there is one such orbit and

$$
u-\ell\le(p-1)q.
$$

For even p there are two such orbits, each of diameter at most
2*floor(p/4)*q.

**Proof.** Compare a preimage of u with ell, and a preimage of ell with u.
Since H reverses C-values, the restricted C-drawdown gives

$$
0\le u-H(\ell)\le q_C,\qquad 0\le H(u)-\ell\le q_C.
$$

Also E(x)=D(A+x)-F_(k-3). Since ell<=s and E(s)=0,
0<=E(ell)<=q_D. Therefore ell+u-t=E(ell)+u-H(ell) lies in [0,q],
and E(u)=ell+u-t+H(u)-ell<=q_D+2q_C. For any x in Gamma, x<=u
implies E(x)-E(u)<=q_D, proving the uniform bound. The exact identity
H^2(x)-x=E(H(x))-E(x) proves the two-step bound.

If a spatial gap in an H^2-orbit exceeded 2q, no two-step edge could
cross it. Its two sides would then belong to different orbits, a
contradiction. Half the maximum gap bounds the distance to the filled
interval. For odd p the undirected cycle graph of H^2 has diameter
(p-1)/2; for even p each of its two cycles has diameter floor(p/4).
Each edge has length at most 2q, proving the period bounds. QED.

**Conditional geometry theorem.** Assume b>0 and, on the actual frontier
cycles Gamma_k at n_k=F_k+t_k, assume

$$
q_{C,k}+q_{D,k}=o(N_k),\qquad N_k=F_{k-2}. \tag{11}
$$

Global sublinear drawdowns of C and D would suffice for (11); neither
global hypothesis has been proved. Then

$$
\frac{\min\Gamma_k}{N_k}\to\alpha b,\qquad
\frac{\max\Gamma_k}{N_k}\to b,\qquad
\max_{x\in\Gamma_k}\frac{E_{k-1}(x)}{N_k}\to0. \tag{12}
$$

Along every odd-period subsequence, Gamma_k/N_k converges in Hausdorff
distance to [alpha*b,b]. For an even-period subsequence, let Gamma_(k,0)
be the H_k^2-orbit of the actual selected point and
Gamma_(k,1)=H_k(Gamma_(k,0)). After taking a further subsequence there
is a number a in [alpha*b,b] such that

$$
\frac{\Gamma_{k,0}}{N_k}\longrightarrow[a,b],\qquad
\frac{\Gamma_{k,1}}{N_k}\longrightarrow[\alpha b,b/\alpha-a]. \tag{13}
$$

Thus every possible whole-cycle limit has at most two reflected end
intervals. They overlap or touch if a<=b/(2alpha); otherwise there is
one central gap. At a=b the limit is the two points {alpha*b,b}.
These hypotheses exclude multiple macroscopic gaps in a frontier-cycle
limit. They make no assertion about smaller-scale structure.

**Proof.** At the actual selected split, both child defects vanish. Hence
0<=t_(k-1)-s_k, 0<=t_(k-2)-v_k, and their sum is Delta_k=o(N_k).
The limit defining b consequently gives

$$
\frac{t_k}{N_k}\to b/\alpha,\qquad
\frac{s_k}{N_k}\to b,\qquad \frac{v_k}{N_k}\to\alpha b.
$$

Fix K in (1). Applying the minorant and (10) at u_k=max Gamma_k gives
u_k<=c_K*N_k+(q_(D,k)+2q_(C,k))/gamma_K. First let k tend to infinity
with K fixed, then let K tend to infinity, using c_K->b. Since u_k>=s_k,
this proves u_k/N_k->b. The first bound in (10) determines ell_k/N_k,
and its uniform defect bound proves (12).

For odd periods H_k^2 is transitive on Gamma_k, so its gap bound in
(10), together with (11) and the extrema, proves convergence to the full
interval. For even periods the class containing s_k has upper endpoint
tending to b. Extract a limit a of its lower endpoint. Its spatial gap
bound gives the first interval in (13). On the entire cycle the error
in H_k(x)=t_k-x+E_(k-1)(x) is o(N_k), uniformly by (12), so reflection
gives the second interval. This argument uses actual finite cycles;
it does not pass the diverging prescribed iteration count through a
limiting map. QED.

There is also a quantitative restriction on periods. Along an odd-period
frontier subsequence, s_k-v_k=(alpha^3+o(1))*t_k, so
(p_k-1)*(q_(C,k)+q_(D,k))>=(alpha^3-o(1))*t_k. Odd periods must therefore
diverge under (11). If all frontier periods remain bounded, they are
eventually even and both classes have sublinear diameter, giving the
two-point limit. This permits several finite cycle points to coalesce
at each limiting endpoint; it does not prove that the actual periods
equal two. Absolute rank parity is still determined by the prescribed
depth and entrance, not by naming one class the upper class.

## Earlier-row feedback preserves the prescribed clock

The dependence on the current row reduces to one preceding defect, with
its correlation to both the first orbit point and the remaining depth intact.
Write N=F_k, A=F_(k-1), B=F_(k-2), ell=F_(k-3). The small frontiers
t_9=8=F_6 and t_10=7<=F_7, together with the contact recursion, imply
t_j<=F_(j-3) for j>=9. Thus U_k=t_(k-1)+t_(k-2)<=ell for k>=11,
covering every possible positive contact offset at those levels.

**Exact feedback theorem.** Fix k>=11 and 1<=t<=ell. For 0<=e<=t-1 put

$$
h_t(e)=A+t-1-e,\qquad z(e)=B+1+e,\qquad
s_{k,t}(e)=T_{N+t}^{\,A+t-2-e}(B+1+e)-A.
$$

Then s_(k,t)(e) lies in [0,t], and

$$
\Phi_{k,t}(e)=E_{k-1}(s_{k,t}(e))+
E_{k-2}(t-s_{k,t}(e))\in\{0,\ldots,t\}
$$

uses only C(1),...,C(N-1). The actual row satisfies

$$
\boxed{E_k(t)=\Phi_{k,t}(E_k(t-1)).} \tag{14}
$$

**Proof.** The comparison envelopes give ell+1<=C(x)<=A for B+1<=x<N.
Hence J=[B+1,N-1] is invariant:

$$
T_{N+t}(J)\subseteq[B+t,N+t-\ell-1]\subseteq J.
$$

Every z(e) lies in J. Its A-1 points bound every transient by A-2.
The remaining iteration count A+t-2-e is at least A-1, so the selected
point is cyclic. All-cycle capture puts it in [A,A+t]. Both child offsets
are native because they are at most t<=ell; their caps give the range of Phi.
For the actual e=E_k(t-1), the preceding output is A+t-1-e. Its first
iterate from N+t-1 is B+1+e, with exactly A+t-2-e iterations remaining.
Child-defect additivity proves (14). Every lookup after the first stays
below N. QED.

Each diagnostic e retains its paired seed and remaining depth. This enclosure
neither chooses a free cycle phase nor asserts another consistent sequence.

**Finite erosion certificate.** Choose 1<=a<=U_k, initialize
S_(a-1)={0,...,a-1}, and set S_t=Phi_(k,t)(S_(t-1)) successively.
The actual defect belongs to S_t by the initial cap and (14). Each map's
output range is the next map's input range. Therefore

$$
\boxed{0\notin S_t\ (a\le t\le U_k)
\quad\Longrightarrow\quad\Delta_k\ge U_k-a+1.} \tag{15}
$$

Every set in this certificate uses earlier rows alone.

### A uniform basin exclusion at level 20

Here N=6765, A=4181, B=2584 and U_20=87+67=154. The
[checker](verification/earlier_row_check.py) evaluates Phi using only the
prefix through 6764. The [exact images](verification/earlier-row.json) are:

| t | Phi_(20,t)({0,...,t-1}) | Propagated S_t from S_148={0,...,148} |
|---|---|---|
| 149 | {4} | {4} |
| 150 | {4} | {4} |
| 151 | {1,4,8} | {4} |
| 152 | {1} | {1} |
| 153 | {1,3,6} | {1} |
| 154 | {4} | {4} |

The earlier prefix thus determines
(E_20(149),...,E_20(154))=(4,4,4,1,1,4) without supplying E_20(148).
Equation (15) gives Delta_20>=6; an independent actual contact at 148
makes this equality. Delta_20=6 was already enumerated. The stronger
certificate eliminates all uncertainty about the preceding current-row state.

At t=154, every allowed e=0,...,153 gives y_1=2585+e and h=4334-e>=4181.
Earlier-row interval propagation encloses every trajectory at absolute rank
10 in offsets [151,154] from A. The evidence records every intervening
interval with its exact minimum and maximum C-values. Direct iteration gives

$$
H_{154}^{25}(151)=H_{154}^{25}(152)=
H_{154}^{25}(153)=H_{154}^{25}(154)=45,\qquad
H_{154}(45)=112,\quad H_{154}(112)=45.
$$

All allowed first images synchronize at offset 45 at absolute rank 35.
Both reached phases have total defect four:

$$
E_{19}(45)+E_{18}(109)=3+1=4,\qquad
E_{19}(112)+E_{18}(42)=3+1=4.
$$

Every permitted depth is later than this synchronization. The exact clock
selects offset 112 for even e and 45 for odd e; neither is a contact.
In the same earlier row, {87,67} is a genuine two-cycle, with the marked
phase E_19(87)+E_18(67)=0. Its basin misses the entire first-image interval
[2585,2738], even after allowing every capped preceding defect with its
correlated clock. The actual e=1 gives depth 4333, selected offset 45 and
C(6919)=4331 rather than the cap 4335. Its first cycle-entry rank is 33;
rank 35 is the common synchronization rank.

The reproducer checks all 909 seed-and-clock cases by literal residual
iteration. A separate literal construction through 6919 takes 15533193
updates and agrees with the independently generated earlier prefix.
This finite certificate gives no uniform cross-level erosion estimate.
Excluded widths w_k with sum(w_k/U_k)=infinity would force b=0 by the
contact-loss budget; such widths remain unproved.

### An exact three-route decoder for amplitude-three windows

The [traveling-history obstruction](exact-collars.md#an-amplitude-three-traveling-history-limits-the-relaxed-routing-method)
leaves the first core entrance free. The following formula determines that
entrance from earlier values, keeping each diagnostic seed paired with its
own clock. It applies to an actual source window with defects in {0,3}.

Let j>=22 and 2<=W<=B<=min(2W,F_(j-3)). Assume the complete natural
profile P_(j-1)(u)=C(F_(j-1)+u)-F_(j-2) satisfies
P_(j-1)(u)>=min(u,W), the lower profile E_(j-2) vanishes through W,
and b(u)=E_(j-1)(u) belongs to {0,3} for 0<=u<=B. Write
A=F_(j-1), D=F_(j-2), H=F_(j-3), and fix
W<t<=floor(alpha B) with t+3<=B. Set a(u)=E_(j-2)(u) and define

$$
z(u)=0\quad(0\le u\le W),\qquad
z(u)=\begin{cases}a(u),&b(u)=0,\\z(u-3),&b(u)=3\end{cases}
\quad(W<u\le B).
$$

For each diagnostic preceding defect 0<=e<=t-1, start at k=H-1-e
and repeat the following exterior excursion while k>Z_(j-1):

$$
s=Q_{j-1}(k),\qquad
k\longleftarrow P_{j-1}(t+s)-t
=C(A+t+s)-D-t. \tag{16}
$$

Here Q_m(k)=F_(m-1)-C(F_m-k) and
Z_m=3m+floor((m-1)/3)-24. At termination put q(e)=Q_(j-1)(k) and

$$
d(e)=\begin{cases}
2,&q(e)=1\text{ and }b(t+1)=3,\\
1,&q(e)=2\text{ and }b(t+2)=3,\\
0,&\text{otherwise}.
\end{cases}
$$

**Exact decoder theorem.** Algorithm (16) uses only C below F_j and
terminates after O(log F_j) excursions. With h(e)=A+t-1-e, the feedback
map in (14) is exactly

$$
\boxed{\Phi_{j,t}(e)=
\begin{cases}0,&h(e)\text{ even},\\z(t-d(e)),&h(e)\text{ odd}.
\end{cases}} \tag{17}
$$

Thus, after precomputing z, only three routed lower values can occur.
The choice between them is fixed by the earlier exterior trajectory.

**Proof.** The first diagnostic point is D+1+e=A-k, at absolute rank 1.
The invariant interval in the feedback theorem is [D+1,F_j-1]. Its A-1
points ensure the diagnostic endpoint is already cyclic at every allowed
depth h(e)>=A; all-cycle capture puts that endpoint in [A,A+t].

An exterior point A-k goes to A+t+s, then to A-k_new with k_new as in
(16). Invariance ensures t+s<=D-1, within the complete source domain.
The [negative shelves](exact-collars.md#two-higher-cap-levels-and-their-phase-selected-closure)
give s>=4 when k>Z_(j-1). If t+s<=B, then
k_new=s-b(t+s)>=1. If t+s>B, the
[golden localization](exact-collars.md#simultaneous-extinction-of-binary-cap-defects)
gives P_(j-1)(t+s)>=floor(alpha B)+1>t, again making k_new positive.
For completeness, the localization follows directly from the global golden
lower bound. If v>B, then

$$
P_m(v)\ge\lfloor\alpha(v+1)+\delta_m\rfloor
\ge\lfloor\alpha B\rfloor+1,\qquad
\delta_m=(-1)^{m-1}\alpha^m,
$$

because v>=B+1 and 2alpha-alpha^m>1 for m=j-1>=21.
Nonnegative native defects and the quantitative negative-anchor bound give

$$
1\le k_{\rm new}\le s\le\lfloor2k/3\rfloor.
$$

These excursions remain exterior and contract until k<=Z_(j-1).
The exact shelves then give q(e) in {0,1,2,3}. When q=0, the next
point is the high core endpoint A+t at an even absolute rank. For q>0,
if b(t+q)=3, the next two points reach low offset 3-q and high offset
t+q-3. If b(t+q)=0, the next lower distance is q<=3, in the negative
zero plateau; the following point reaches high offset t. Hence the
even-rank high start is t-d(e). Each exterior excursion takes two steps;
the terminal branch takes one step when q=0 and three when q>0. Starting
from the rank-one lower point, every resulting high start has even
absolute rank. The case q=3 also gives high start t.
All these queries lie in the controlled band because t+3<=B.

The high start is at least W. In particular, if d=2 the guard
b(t+1)=3 and saturation imply t+1-3>=W; if d=1 the other guard
implies t+2-3>=W. A high offset u with b(u)=3 next visits low offset
t-u+3 and high offset u-3. The low offset is at most t-W<=W and
therefore exact. High offsets descend by three until a source contact
R>=W is reached: whenever u>W and b(u)=3, saturation gives
u-3=P_m(u)>=W, so a routing step cannot cross below W. At u=W
saturation forces b(W)=0. The terminal pair is {R,t-R}, with high R at even
absolute rank. At even depth its two child defects vanish; at odd
depth their sum is a(R)=z(t-d(e)). This proves (17), and the selected
point is A+R at even depth, A+t-R at odd depth. Finally, the nondecreasing
golden lower envelope gives C(x)>=G(x)>=G(F_j)=A for x>=F_j.
Together with the native cap this gives 0<=E_j(t-1)<=t-1, so the actual
preceding defect is an allowed
diagnostic state, and (14) gives the claimed actual recurrence. QED.

This determines the first entrance, including the two guarded alternatives,
without an alphabet assumption on source queries outside B. Bounding how
often the terminal distance lands in the q=1 or q=2 strips remains open;
(17) alone gives no uniform extinction or convergence estimate.

### A protected distance interval and a necessary distant query

Retain the decoder hypotheses and put m=j-1, M=floor(alpha B), V=M-t.
Golden localization gives the following inverse restriction on (16):

$$
t+s>B\quad\Longrightarrow\quad
k_{\rm new}=P_m(t+s)-t\ge V+1. \tag{19}
$$

Consequently every transition into the lower-distance interval [1,V]
uses a controlled source query. Once k<=V, all subsequent exterior
queries remain controlled too: t+Q_m(k)<=t+2k/3<=M<=B, and contraction
keeps the next positive distance at most V. This conclusion permits
arbitrary actual source defects outside B.

Write L=L_m, R=R_m, S=S_m and Z=Z_m for the four exact shelf endpoints.
Suppose the diagnostic path starts at k_0>Z, and its decoded high start
is nondefault. It must first cross from some k_->Z to a positive
distance r<=Z. The final shelf classification forces L<r<=S.
If t+S<=M, (19) makes that incoming query controlled. With
s=Q_m(k_-), it therefore satisfies

$$
L+1\le s\le S+3,\qquad
r=s-b(t+s),\qquad b(t+s)\in\{0,3\}. \tag{20}
$$

The two entrance channels have the more precise necessary conditions:

| Decoded high start | Incoming s if b(t+s)=0 | Incoming s if b(t+s)=3 | Neighbor guard |
|---|---|---|---|
| t-2 | L+1..R | L+4..R+3 | b(t+1)=3 |
| t-1 | R+1..S | R+4..S+3 | b(t+2)=3 |

For the first channel alone, the weaker margin t+R<=M suffices.
Thus a nearby guard alone cannot determine a nondefault entrance:
the actual contracting path must also visit a distant source query with
the compatible value in this table. If the canonical preceding defect
lies in {0,3}, then k_0>=H-4>Z for j>=22, so this necessary condition
applies whenever its displayed margin holds.

With the stronger margin t+Z<=M, every first crossing into [1,Z] is
controlled and has 4<=s<=Z+3. Incoming labels

$$
s\in[4,L]\ \cup\ [S+4,Z+3]
$$

force the default high start: their returned distances lie respectively
in the q=0 and q=3 shelves. These are excluded *labels*, not a frequency
bound on actual crossings. Even a default entrance can copy a positive
lower defect. The margins can be empty, and none of these restrictions
yet bounds the delay to a zero output.

### A seeded branch exclusion at level 33

Take j=33, W=225, B=450 and t=260. The independently regenerated earlier
prefix verifies the source hypotheses, including the complete barrier:
its controlled part satisfies saturation, and the golden lower bound at
B+1 bounds the whole remaining profile. Here
A=2178309, D=1346269, H=832040 and Z_32=82. The entire diagnostic
seed interval is k in [H-t,H-1]=[831780,832039]. Exact interval
enclosures under (16) give:

| Exterior distance k | Range of Q_32(k) |
|---|---|
| 831780..832039 | 513970..514228 |
| 424025..424891 | 190842..191963 |
| 176000..177784 | 58636..59583 |
| 56804..57996 | 13776..14365 |
| 13498..14358 | 2351..2540 |
| 2310..2538 | 287..323 |
| 287..323 | 24..26 |
| 24..26 | 1..1 |

Each next distance interval encloses C(A+t+s)-D-t for every integer s
in the preceding right column. The last distance interval is inside the
exact q=1 strip (L_32,R_32]=(18,36]. Therefore every capped preceding
state has d(e)=2: b(261)=3 forces high start 258, b(258)=3 routes to
255, and b(255)=0 stops there. Since E_31(255)=0,

$$
\boxed{\Phi_{33,260}(\{0,\ldots,259\})=\{0\}.} \tag{21}
$$

This excludes a positive branch that the relaxed rule permits: its default
odd-depth route stops immediately at b(260)=0 and copies E_31(260)=2.
The actual seeded route always stops at 255 instead. The selected points
are A+255=2178564 at even depth and A+5=2178314 at odd depth.
No current-row value is used to obtain this exclusion.

The [same checker](verification/earlier_row_check.py), with `--ternary`,
regenerates the prefix through F_33-1=3524577 by full visited orbits and
independently by Brent cycle detection. It checks 8384 interval extrema
lookups and compares all 260 paired seeds and clocks with direct visited
orbits, including their selected points. The [compact evidence](verification/earlier-row.json)
contains both this certificate and the earlier level-20 certificate.
The level-33 exclusion is finite; a uniform cross-level reset estimate
still requires a new argument.

## Independent checks

The [checker](verification/frontier_dynamics_check.py) uses full visited-state
orbits through 131072 and literal values through 2584. Its
[compact output](verification/frontier-dynamics.json) checks the two
minorants at 364120 right-profile and 225013 left-profile positions,
the quantitative entrance bound at 408 inputs, and the interior bounds
at 2075 cycle positions. Seven gated frontiers satisfy the five-input
theorem in this prefix; levels 19..25 satisfy its other hypotheses but
are ungated.

The finite cycle lemma is checked at all 2315 non-anchor cap contacts
from n=47 through 131072, covering 4642 two-step cycle edges and three
cycles of period greater than two. This includes both spatial gap and
period inequalities. These checks do not establish the sublinear
drawdown assumption (11).

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

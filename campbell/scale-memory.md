# Campbell scale memory in canonical Fibonacci windows

[Project home](../README.md) · [Research map](../cloitre-conway/README.md#technical-research-map)

This note proves a finite-horizon lower bound for autonomous recognition
in canonical Fibonacci five-window encoding, using the
[proved Campbell formula](note.pdf). It counts control states and excludes
the size of horizon-specific transition tables. Supplied clocks are a
separate resource. The
[Cloitre counterpart](../cloitre-conway/five-window-closure.md#autonomous-memory-of-the-actual-top-plateau-diagnostic)
now gives an actual-C cap diagnostic and a full-graph state lower bound.
The [bounded-cap graph theorem](../cloitre-conway/five-window-closure.md#exact-state-bit-order-for-every-bounded-cap-graph)
also matches the state-bit order for each fixed-cap Cloitre value and
selected-split graph, with a deterministic sparse-trie upper bound.
See the [Conway interface](../cloitre-conway/five-window-closure.md) for the
cross-family closure question.

## Contents

- [A quantitative scale-memory obstruction from Campbell's ternary law](#a-quantitative-scale-memory-obstruction-from-campbells-ternary-law)
- [Five-pattern interaction on ternary scale interiors](#five-pattern-interaction-on-ternary-scale-interiors)

### A quantitative scale-memory obstruction from Campbell's ternary law

The cross-family problem has an unconditional obstruction even though
Campbell's inner cycles have length at most two. Its powers-of-three
scale law cannot be recognized by a bounded autonomous control on canonical
FIB five-window words. Here that obstruction is quantified at a finite
horizon. The result concerns exact word recognition and certificate
verification, not online computation of b or the minimum interface for C.

The starting points are Campbell's proved [scale formula](note.tex)
and the qualitative nonregularity argument in
[Trureturing PR11560, Section17.3](https://github.com/the-omega-institute/trureturing/blob/c71e2e9599ea407fae545287b024590c444b03ef/docs/develop/theory/FIB_RELATIONAL_CONTINUATION_GEOMETRY.md).
The finite-horizon estimate below is a quantitative refinement of that
argument; no historical priority claim is made.

**The recognition contract.** Write n in its canonical nonadjacent
Fibonacci digits, with weights F_2=1,F_3=2,F_4=3,... . Keep the unit digit
e at F_2 separately, group the remaining digits into triples, and read the
windows from high to low, followed by the distinct terminal symbol
underlined e. The five window letters are null,[2],[3],[5],[25], with
composition digits

$$
d_{\rm null}=(0,0),\quad d_{[2]}=(1,0),\quad
d_{[3]}=(0,1),\quad d_{[5]}=(1,1),\quad d_{[25]}=(2,1).
$$

The seam condition forbids adjacent nonzero Fibonacci digits across windows
and at the unit boundary. Highest windows are nonnull. If c is obtained
by the high-to-low Horner update c<-Sc+d, then

$$
S=\begin{pmatrix}1&2\\2&3\end{pmatrix},\qquad
n=e+qc,\quad q=(2,3),\quad
\Lambda=2+\sqrt5,\quad\Theta=2-\sqrt5.
$$

Thus exactly m windows encode the interval
[F_(3m),F_(3m+3)-1]. Let P be the canonical words encoding5*3^k,k>=0.
A horizon-L recognizer, with K states, must accept exactly P among all
words with at most L windows and one terminal symbol; its behavior on
longer words is unrestricted. States include the actual autonomous
control, including any internally maintained read-position counter.
Each finite horizon may have its own transition table; these finite-horizon
upper bounds are nonuniform and do not supply a fixed small-space program
that constructs or evaluates those tables at arbitrary horizons.
The argument applies to deterministic and nondeterministic finite automata.

**Finite-horizon lower bound.** Every such recognizer satisfies

$$
L\le4K+4,\qquad K\ge\left\lceil\frac{L-4}{4}\right\rceil.
$$

First, P has a word of every positive window length. Its first number is5
and has one window; multiplication by3 never skips a length, since
3F_t<F_(t+3) for t>=3. Lengths are nondecreasing and unbounded.

Suppose instead L>=4K+5. Choose an accepted word with exactly m=K
windows. Along one accepting run, two of the K+1 states before and after
its first K windows coincide. Write the window part uvw, where
ell=|v|>=1,|uv|<=K, and w has c windows. The terminal unit symbol
is kept at the end of w and is not pumped. Every uv^rw is accepted
when its window length m+(r-1)ell is at most L.

Here is a uniform estimate for the numerical value N_r of this pumped
word. For a block z let C_z be its Horner composition. Define the spectral
rows

$$
q_+=(1+2\sqrt5/5,\ 3/2+7\sqrt5/10),\qquad q_-=q-q_+.
$$

They satisfy q_+S=Lambda*q_+,q_-S=Theta*q_-. Horner expansion gives

$$
N_r=A\Lambda^{r\ell}+B+C\Theta^{r\ell},
\qquad
A=\Lambda^c\left(q_+C_u+
                  \frac{q_+C_v}{\Lambda^\ell-1}\right)>0.
$$

The strict positivity follows from the nonnull highest window, which
occurs in u or v. Every nonzero digit has q_+d>=1 and every digit has
q_+d<8,|q_-d|<1. Since Lambda-1>3 and1-|Theta|>3/4, every block z of
h windows satisfies q_+C_z<3Lambda^h and |q_-C_z|<4/3. If u is empty,
the highest digit of v gives q_+C_v>=Lambda^(ell-1); otherwise
q_+C_u>=1. Consequently A>=Lambda^(c-1). The exact constant terms are

$$
\begin{aligned}
B&=e+qC_w-\Lambda^c\frac{q_+C_v}{\Lambda^\ell-1}
                 -\Theta^c\frac{q_-C_v}{\Theta^\ell-1},\\
C&=\Theta^c\left(q_-C_u+
                    \frac{q_-C_v}{\Theta^\ell-1}\right).
\end{aligned}
$$

The preceding bounds give |B|<=11Lambda^c,|C|<4 and hence, for r>=0,

$$
|N_r-A\Lambda^{r\ell}|\le64A.
$$

If r*ell>=2ell+6, this implies

$$
\left|\frac{N_{r+1}}{N_r}-\Lambda^\ell\right|
\le256\Lambda^{\ell-r\ell}
<\frac1{16}\Lambda^{-\ell}. \tag{9.26}
$$

Indeed Lambda^(r*ell)>128, so the denominator is at least half its
leading term; use1+Lambda^ell<=2Lambda^ell and Lambda>4.

Both N_r and N_(r+1) cannot be5 times powers of3. If they were, their
ratio would be3^h with integer h>=1 by (9.26). The nonzero algebraic
integer norm

$$
(\Lambda^\ell-3^h)(\Theta^\ell-3^h)
$$

has absolute value at least1. But (9.26) gives3^h<2Lambda^ell, so

$$
|\Lambda^\ell-3^h|\ge\frac1{3}\Lambda^{-\ell},
$$

contradicting (9.26). Choose r=2+ceil(6/ell). Then r*ell<=3ell+5,
and the longer pumped word has at most m+3ell+5<=4K+5<=L windows.
It must be accepted yet cannot belong to P along with the other pumped
word. This contradiction proves the finite-horizon bound. QED.

**An exact memory order for this scalar diagnostic.** There are O(L)
words of P of length at most L, each of length O(L). A prefix trie and
reject state therefore give a deterministic recognizer with O(L^2) states.
For example2(L+1)^2+2 states suffice, using F_(3L+3)<5^(L+1).
Together with the lower bound, the minimum number of bits encoding an
autonomous recognizer state lies between log_2 L-O(1) and2log_2 L+O(1),
and therefore has order

$$
\Theta(\log L)=\Theta(\log\log N),
$$

where the finite numerical horizon is N=F_(3L+3)-1. This is a tight
memory order, not a claim that the exact state count is linear. It also
does not bound the size of the recognizer's read-only transition table.

**Consequence for Campbell's full graph.** The scale formula gives exactly

$$
\{n:5b(n)=2n\}=\{5\cdot3^k:k\ge0\}.
$$

Take a high-to-low synchronous FIB recognizer for(n,b(n)), with common
high-end null padding and the two terminal unit symbols. Intersect it
with the fixed finite-carry filter2n-5b=0 and the fixed canonical-language
filter on the n row, then project away the b row. The number of states
increases only by a constant factor, and the projected automaton recognizes
P through the same window horizon. Thus exact Campbell graph recognition
also requires Omega(L) states and Omega(log L) state bits.

For nondeterministic graph recognition this bit order is attainable.
There are O(L) possible scales s=3^k<=n. For each one, its padded
canonical word can be supplied by an O(L)-state word matcher. Combine
it with the fixed finite automata for the four linear/parity branches
of Campbell's formula, then take their union and project out the scale
row. Fixed integer linear relations and inequalities in canonical FIB
words have finite automata: addition with finitely many carries and
canonical lexicographic comparison suffice. The resulting graph NFA
has O(L^2) states. This is a certificate-recognition upper bound, not a
matching deterministic decoder or an algorithm for C.

**Where supplied context can hide this memory.** If both the exact word
length m and current position are supplied as free external clocks,
there are at most two P words of that length: its numerical interval has
ratio less than9. Comparing against those two stored words needs only
two surviving-match flags. This does not contradict the lower bound:
the clock and length-dependent table are no longer counted as autonomous
states. A proposed minimum additional five-window payload must therefore
declare whether these scale, position and contextual resources are free.
Campbell's short period/parity certificate does not pay their cost in FIB;
its native ternary representation does not have this scale obstruction.
The Cloitre counterpart obtains an actual full-graph lower bound from its
moving top plateau. A matching upper bound for that graph remains open.

The maintained closure checker verifies the canonical window/Horner
correspondence, the exact Campbell level set on a finite prefix, and the
pumped-number obstruction for every window-block cut in a declared set of
actual powers-of-three words. Those checks corroborate this general proof;
they are not the premise for its lower bound.

### Five-pattern interaction on ternary scale interiors

The same five legal canonical window patterns have a scalar interaction
in Campbell's family, despite its inner periods being at most two.
For a canonical higher context h with all digits below F_7 removed,
write f_h(x)=b(h+2x_1+3x_2+5x_3) and

$$
\kappa_b(h)=b(h+7)-b(h+2)-b(h+5)+b(h).
$$

**Strip/parity theorem.** Let s be a power of three and suppose all
five arguments lie in the same indicated interval. Then

| Interval | Even-argument slope | Odd-argument slope | Interaction |
|---|---:|---:|---|
|[3s,4s)|1|0|-2(-1)^h|
|[4s,5s)|0|0|0|
|[5s,6s)|0|1|2(-1)^h|

**Proof.** In these intervals the even branch is min(n-s,3s) and
the odd branch is max(2s,n-3s), using the same scale s. If h is even,
b(h+7)-b(h+5) is twice the odd slope, whereas b(h+2)-b(h) is twice
the even slope. If h is odd these roles reverse. Their difference
gives the table. QED.

**Infinite shared canonical contexts.** For q>=3 and
lambda in{10,14,16}, expand lambda*3^q canonically and retain only its
digits at F_7 and above; call the resulting integer h_(lambda,q).
The removed lower contribution is between0 and12. The remaining
higher word is canonical, its unit digit and F_6 separator are0,
and adding0,2,3,5,7 changes only the legal F_3,F_4,F_5 window.

Put s=3^(q+1). For lambda10,14,16 respectively, the whole window lies
in[3s,4s),[4s,5s),[5s,6s): its distance from every relevant endpoint
exceeds the possible12-unit truncation and7-unit addition because3^q>=27.
The table therefore applies for every q>=3. All three context families
grow without bound; the first and third have absolute interaction2,
and the middle has interaction0. No window-independent interaction
coefficient can represent all these readouts, even if the baseline and
singleton coefficients depend arbitrarily on the higher context.

**Exact current-coefficient classes.** For every n>=2,
b(n+2)-b(n) is0 or2. This follows from the explicit formula: each
parity branch alternates linear slope1 and flat segments, with continuous
joins. The even breakpoints4s,6s are even; the odd breakpoints5s,9s
are odd, so a two-step sample crosses no intermediate kink.
Thus every canonical higher context has kappa in{-2,0,2}; the checked
contexts realize all three values: h=7286,377,267 give-2,0,2,
respectively. Equivalence of higher contexts for
the current coefficient readout has exactly three classes. This is a
readout quotient, without a claim that it is closed under word continuation.

The displayed strip formula also uses the parity of h.
The parity is determined by the whole higher word, not its unit digit:
F_j is even exactly when j=0mod3. The strip/parity formula treats the
ternary scale as supplied context. The autonomous-memory theorem above
states its separate recognition contract; a coefficient-only memory
bound would require another argument.

The [Cloitre construction](../cloitre-conway/exact-collars.md#a-persistent-interaction-on-canonical-index-words)
has interaction1 on an infinite canonical family whose five root basins
are all fixed points, and the signal persists along arithmetic first-child
descent. Both constructions concern the same five digit patterns, with
different recurrence laws and different higher-context interfaces.

The checker generates18 contexts at q3..8 from the recurrence, checks
all90 canonical words, verifies every selected endpoint by literal
iteration, and compares against the proved formula. A separate literal
prefix supplies an evaluator cross-check. These calculations corroborate
the universal strip/truncation argument; they are not its premise.

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
The [modular symbolic selector](../cloitre-conway/recursive-descent.md#a-modular-symbolic-selector-with-small-working-memory)
gives a concrete supplied-profile decoder for Cloitre. Its cycle residue
reduces to parity on Campbell's certified period1/2 templates; this
conditional decoding resource is distinct from autonomous FIB recognition.

## Contents

- [A quantitative scale-memory obstruction from Campbell's ternary law](#a-quantitative-scale-memory-obstruction-from-campbells-ternary-law)
- [Five-pattern interaction on ternary scale interiors](#five-pattern-interaction-on-ternary-scale-interiors)
- [Golden-defect words and the period-two interface](#golden-defect-words-and-the-period-two-interface)

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

The [qualified additive window and direct descendant decoder](../cloitre-conway/exact-collars.md#additive-canonical-windows-and-a-direct-descendant-decoder)
make the comparison more precise. Cloitre's cap0/1 first spine has an exact
gap formula obtained by projection onto nested intervals; canonical carries
follow from its supplied order and gap. Campbell's displayed strip law uses
the ternary scale and whole-context parity instead. Neither construction
turns the five current feature labels into a context-free recursive state.
For Cloitre, adding the unit digit completes the first edge, but a second or
third edge already changes the higher canonical context. These semantic
coordinates are not independent bit costs when their context derives them.

The [child-cap allocation interface](../cloitre-conway/recursive-descent.md#actual-defect-allocation-and-phase-information)
also distinguishes the two scalar contracts. In Campbell's recurrence,
the parent value b(N) is itself the selected endpoint. Supplying that value
therefore identifies the endpoint directly. Cloitre's parent value is a
sum of two child values and can leave their allocation ambiguous, even on
an actual five-cycle. With lower profiles supplied, a second-child cap
determines a periodic seed and removes separate cycle/phase labels.

The checker generates18 contexts at q3..8 from the recurrence, checks
all90 canonical words, verifies every selected endpoint by literal
iteration, and compares against the proved formula. A separate literal
prefix supplies an evaluator cross-check. These calculations corroborate
the universal strip/truncation argument; they are not its premise.

### Golden-defect words and the period-two interface

The [golden-defect cyclic decoder](../cloitre-conway/inverse-reconstruction.md#golden-defect-words-give-a-uniform-cyclic-decoder)
also applies to Campbell's inner map. Set G(x)=floor((x+1)/phi) and
write d_i=b(x_i)-G(x_i). Supply the ordered integer word d_i and the
root N. Then the coordinates of a proposed closed orbit satisfy

$$
x_{i+1}=N-d_i-G(x_i).
$$

The diagnostic golden floor can be extended to all integers during
bisection, while b remains defined only at positive indices. The defect
integers may be negative: Campbell's values are not bounded below by G.
The decoder theorem permits signed constants and signed defects.

For a fixed point the inverse is unique. For an even word there are at
most three raw solutions, at consecutive initial indices. Thus a supplied
period-two defect word needs at most two seed bits before actual-value
and proper-period checks. This is a numeric inverse bound, not an
autonomous recognition theorem or a method for obtaining the defect word.

**Sharp shared example.** At N=5 the two sequences have the same earlier
values (1,1,2,3)=G(1),...,G(4). The ordered word d=(0,0) admits exactly

$$
(x_0,x_1)=(2,4),\quad(3,3),\quad(4,2).
$$

All three satisfy actual scalar-value qualification. Requiring proper
period2 removes the fixed word (3,3), leaving two oriented phases.
Campbell's prescribed start is4, its depth is b(4)=3, and its selected
endpoint is2. The [complete formula](note.pdf) supplies the actual basin
and parity information; the golden word by itself retains a phase choice.

This contrasts with an odd Cloitre child window: supplying its ordered
golden defects and alpha parameters leaves no numeric branch choice.
It does not remove the cost of supplying those integers or of verifying
actual nesting. The scale-memory obstruction above therefore remains a
separate result: a small residual phase label with clocks and defects
supplied does not imply bounded autonomous memory in Fibonacci encoding.

The [cap4 profile-response construction](../cloitre-conway/recursive-descent.md#cap4-query-profiles-and-the-information-they-carry)
isolates another distinction. Its captured-map models all have period2
and the same selected odd phase, but an omitted profile amplitude changes
the numerical children. For actual Campbell, the proved formula obtains
both amplitude and phase from n and its power-of-three scale. Transferring
that interface to Cloitre requires deriving its profile values as well;
matching short periods alone does not supply them. The construction is a
local-profile obstruction, not an asserted alternative actual C sequence.

The [generated actual cap4 band](../cloitre-conway/exact-collars.md#a-propagated-cap4-band-generates-its-own-profiles)
now supplies those responses arithmetically in an initial Cloitre region.
Its [canonical family](../cloitre-conway/exact-collars.md#a-canonical-cap4-window-reaches-the-next-fibonacci-digit)
has an affine numerical child map but nonzero joint coefficients in the
child's canonical digits; their Fibonacci weights cancel. A short-period
or affine numerical interface can therefore retain nonlinear digit
readouts. Both the new Cloitre interface and Campbell's formula derive
their scoped arithmetic data; the wider Cloitre profile problem stays open.

The [actual upper shelf](../cloitre-conway/exact-collars.md#a-bounded-upper-shelf-and-a-wider-zero-allocation-corridor)
also bounds a fixed D-position Cloitre tail by height max(4,D) at K>=27.
The actual first thirteen entries are generated; the remaining response
packing uses O(max(0,D-13) log(D+1)) bits independently of the supplied
order. At K>=31 the generated prefix extends through position16.
It derives zero allocation in a wider corridor, but still requires the
tail responses and parent value. Campbell's formula supplies its arithmetic
data directly; this bounded response envelope does not yet do so for C.
In Cloitre's first thirteen translated-tail positions the actual alphabet
closes to{4,8,9}. Its five-response word has an8-bit full-envelope code
and at most three periodic points. Four finite boundary words and a
propagated flat band make this actual word explicit in the order; its
decoder needs no residual word or cap labels with order and gaps supplied.
The wider response problem remains open. This scoped arithmetic evolution
is now derived for both families, with their different scale rules and
the autonomous FIB memory requirements kept separate.

The [finite-alphabet Cloitre tail](../cloitre-conway/exact-collars.md#a-finite-alphabet-propagates-beyond-the-zero-allocation-corridor)
has at most six periodic vertices and zero second-cap allocation through
forty-seven translated positions, but its wider response word remains an
input. High-cap spines have at most fifteen strict excess drops; all other
edges copy that excess. A{4,e} two-cycle additionally requires its
successor's response to be4; zero drop alone does not certify it.
Actual orders29/30 have the same local tail word, cycle and depth parity,
yet select different members because their entry clocks differ. Campbell's
complete ternary templates determine its entry and parity data; a cycle
alphabet or parity shortcut alone has not provided the corresponding
Cloitre word evolution. This isolates a temporal selection question beyond
the shared finite-cycle decoder and autonomous scale-memory comparison.

The [Cloitre frontier reset rule](../cloitre-conway/recursive-descent.md#an-even-landing-determines-a-frontier-phase)
now derives its phase bit from the first even landing below a Fibonacci
anchor and at most one tail query, without a supplied current parent cap.
The exterior landing still needs actual-C queries or a qualified certificate;
Campbell's formula derives its entry data arithmetically. On the five additive
patterns, the Cloitre phase transfers joint interaction between scalar values
and selected child indices while their difference remains e-4. Canonical
higher-word qualification and recursive evolution remain separate.

The [six-response Cloitre map](../cloitre-conway/recursive-descent.md#six-response-states-close-a-wider-selected-orbit-interface)
extends beyond that frontier: its alphabet map gives every periodic option
from six tail answers, with fifteen shared answers for five additive rows.
An actual three-cycle requires a modulo-three phase calculation, so the
general landing clock is not exhausted by parity. Qualified landing and
clock residues now give a fixed finite decoder without supplied parent
caps, but the response word and exterior data remain inputs. Campbell's
ternary templates derive those family data; the remaining cross-family
question is their construction, not the finite option-table decoding.

The [moving-frontier Cloitre clock](../cloitre-conway/exact-collars.md#a-moving-frontier-needs-recurring-cap4-holes)
adds a cross-order restriction: a surviving first nonflat tail position
must encounter cap4 holes on the actual inner path at order density at
least one third. The phase bit therefore has an explicit path witness,
and its possible recurrence is a word-evolution obstacle. Campbell's
ternary formulas derive its entry data; a finite cycle alphabet alone
does not give the corresponding hole-frequency control for Cloitre.
These inner-orbit counts do not supply the additive martingale occupation
needed for global dispersion.
Beyond that frontier, the [two-cycle clock tradeoff](../cloitre-conway/recursive-descent.md#copy-runs-trade-reset-events-against-adjacent-migrations)
forces resets or adjacent-row migrations, with additional reset entry
channels. An actual high-cap duplicate sustains a hole-free copy.
Campbell's derived entry templates avoid supplying these events as inputs;
controlling their recurrence in Cloitre's wider words remains open.
The [binary-prefix refinement](../cloitre-conway/recursive-descent.md#binary-prefixes-close-with-two-response-states)
derives period at most two when the responses are restricted to{4,8}.
Its actual first nineteen tail positions now have arithmetic values and
selected splits down to a finite base, paralleling Campbell's derived
entry data in a restricted domain. Nine shared map bits and five periodic
output bits describe relaxed wider binary words, not actual input minima.
The [actual support-cone refinement](../cloitre-conway/recursive-descent.md#arithmetic-support-cones-shrink-the-shared-response-word)
narrows the wider tail to{4,8,9} and constrains high responses by the
additive semigroup generated by4 and5. It derives permanent profile
holes and an exact16-bit shared-map envelope, with an8-bit periodic
output envelope. Campbell's power-of-three templates also derive its
exterior entry; Cloitre's support and periodic-only updates still permit
a three-cycle whose exterior clock has not been generated. Arithmetic
support, small conditional certificates and full graph recognition
remain different resources.

The shared [selector checker](../cloitre-conway/verification/selector_payload_check.py)
independently evaluates Campbell's first32 terms by literal iteration and
checks the displayed three-solution inverse. The sharpness statement
follows directly from the three equations at N=5, without extrapolation.

The [two-split moment policy](../cloitre-conway/dispersion.md#two-split-moment-policies-and-cycle-average-dispersion)
is a different asymptotic contract for Cloitre's additive readout. Even
its exact-mean variant fails for Campbell at N5: b(5)=2, while all
four complementary sums are4,3,3,4, so no mixture has mean2.
The inequality-only variant would be feasible, but Campbell lacks the
nonnegative golden-defect hypothesis used by the Cloitre criterion.
Short cycles alone do not transfer its global rate argument.

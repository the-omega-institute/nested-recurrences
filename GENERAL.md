# What are we studying?

[Project home](README.md) · [Research status](STATUS.md)

## The question

A nested recurrence looks up earlier terms repeatedly to decide its next
term. Here the number of lookups is itself an earlier sequence value. A large
depth might explore complicated dynamics, or it might merely select a phase
of a very short cycle. We study both possibilities.

This is connected to the recursive sequences discussed by Hofstadter and to
Conway's recursive sequence. The two specific definitions below are the
objects studied here; their behavior needs its own proofs.

## Campbell's example

Set b(1)=1. For n>=2, let T_n(x)=n-b(x), start at x_0=n-1, and define

$$
b(n)=T_n^{\,b(n-1)}(n-1).
$$

The exponent means exactly b(n-1) applications of T_n, starting from x_0.
John M. Campbell proposed this recurrence. It has a complete formula in
power-of-three intervals, and its inner orbit has at most four transient
steps before reaching a fixed point or a two-cycle. In particular,

$$
\liminf_{n\to\infty}\frac{b(n)}n=\frac25,
\qquad
\limsup_{n\to\infty}\frac{b(n)}n=\frac34.
$$

Read the [Campbell guide](campbell/README.md) or the
[complete proof PDF](campbell/note.pdf).

## Cloitre's Conway-type example

Set C(1)=C(2)=1. For n>=3, let T_n(x)=n-C(x), start at x_0=n-1, and put

$$
g=T_n^{\,C(n-1)}(n-1),\qquad C(n)=C(g)+C(n-g).
$$

Benoît Cloitre proposed this candidate. The starting point and the exact
iteration count are part of the definition. Unlike Campbell's example, the
orbit endpoint determines two child terms that are then added.

With alpha=(sqrt(5)-1)/2, the golden ratio enters through the lower bound
C(n)>=floor(alpha(n+1)) and the identities C(F_k)=F_(k-1).
We have proved liminf C(n)/n=alpha and convergence within sublinear-width
neighborhoods of Fibonacci indices. The limit over all integers is still open:
the centers of the intervening blocks require further control.

Read the [Conway guide](cloitre-conway/README.md) for the proof route.

## A small example

At n=5, both sequences have previous value 3. Starting at 4, repeat the
lookup x -> 5-a(x) exactly three times:

$$
4\ \longrightarrow\ 2\ \longrightarrow\ 4\ \longrightarrow\ 2.
$$

Campbell's rule keeps the endpoint: b(5)=2. Cloitre's rule uses that endpoint
as a split: C(5)=C(2)+C(3)=1+2=3. The same short inner orbit can therefore
produce different outer sequences. In each rule, the previous value sets the
number of steps; stopping as soon as a cycle appears would change the definition.

## Where the five-window question enters

Near a Fibonacci index, the inner map can be written as a reflection plus
a nonnegative defect. A five-cycle has five local reflection equations, but
these alone do not determine its actual selected phase or its descendants.
We ask what additional scale, profile, branch, and phase information is needed
to close that recursion.

The five legal canonical Fibonacci digit patterns provide a related encoding
question. Their five labels alone are not a complete recursive state.
Campbell's power-of-three formula already forces growing autonomous memory
when expressed in this Fibonacci encoding. The
[technical research map](cloitre-conway/README.md#technical-research-map)
separates the local-cycle interface, recursive reconstruction, and asymptotic
dispersion questions.

## How to read the evidence

A written propagation or induction argument proves an infinite statement.
Some arguments also need a stated finite base; independent programs verify
those exact premises. Those results are called computer-assisted proofs.
Other large computations only test conjectures over a finite range and do
not establish a limit or a decay exponent. The [status page](STATUS.md) makes
these distinctions; proof notes give the detailed hypotheses and certificates.

No Lean formalization is currently included. Reproduction instructions are
in [CONTRIBUTING.md](CONTRIBUTING.md#reproduce-the-evidence).

## Attribution and context

Campbell and Cloitre are credited for their respective recurrence proposals.
The Campbell note remains unsigned; a paper author list and submission have
not been established here. AI assistance was used in exploration, proof
development, implementation, and writing.

A related reference is Grytczuk, *Another variation on Conway's recursive
sequence* (2004), [DOI: 10.1016/j.disc.2003.10.022](https://doi.org/10.1016/j.disc.2003.10.022).
The precise relationship and priority questions require literature review.

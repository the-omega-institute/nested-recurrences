# Nested recurrences

A research collaboration on two recurrences proposed by John M. Campbell and
Benoît Cloitre, inspired by the nested recurrences discussed by Hofstadter.
In both examples, an earlier value decides how many times to repeat a lookup.

**The main open question:** does Cloitre's sequence approach the golden-ratio
proportion, C(n)/n -> (sqrt(5)-1)/2, over all integers? We have proved the
lower bound and exact Fibonacci structure, but the full limit remains open.
Campbell's example is completely solved; its ratio does not converge.

## Read the mathematics

**New here? Read [What are we studying?](GENERAL.md)** for the two definitions,
how the iteration works, and the connection to Hofstadter. Then choose a proof:

| Sequence | Current result | Read next |
|---|---|---|
| Campbell | Complete formula; the ratio does not converge. | [Three-page proof PDF](campbell/note.pdf) |
| Cloitre | Golden lower bound and Fibonacci identities; the full limit is open. | [Definition and main theorem](cloitre-conway/README.md) |

**[Results and open questions](STATUS.md)** separates established results from
the remaining problems. The sequence guides lead to the detailed arguments.

No installation or GitHub account is needed. Click a note to read it in your
browser; use the download-arrow button if the PDF preview does not load.

## Work on the project

**[main](https://github.com/the-omega-institute/nested-recurrences/tree/main)**
is the reviewed reading edition. Developing work belongs in
**[pull requests](https://github.com/the-omega-institute/nested-recurrences/pulls)**:
draft while unfinished, checked and merged when ready, then its branch removed.

See **[Contributing and verification](CONTRIBUTING.md)** for that workflow and
optional programs and evidence. Comments in the existing collaboration thread
are welcome; using GitHub is optional.

The current results are written proofs and computer-assisted proofs with
explicit finite certificates. This repository does not currently contain
a Lean formalization.

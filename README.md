# Nested recurrences

How much complexity can a recurrence create when its own earlier values
decide how deeply to recurse? This project studies two examples proposed by
John M. Campbell and Benoît Cloitre, inspired by the nested recurrences
discussed by Hofstadter.

**Campbell's example has a complete solution. For Cloitre's example, the
main open question is whether the ratio of each term to its index converges
to the reciprocal of the golden ratio.**

## Read the mathematics

**[What are we studying?](GENERAL.md)** explains the question and defines
both sequences. Then choose one of these two routes:

- **[Campbell: the complete solution](campbell/README.md)** — explicit formula
  and short inner cycles; **[read the three-page proof PDF](campbell/note.pdf)**.
- **[Cloitre: the golden-ratio problem](cloitre-conway/README.md)** — what is
  proved, the main proof, and the remaining convergence question.

**[Results and open questions](STATUS.md)** separates established results
from the problems still to solve. The current research asks what information
determines the actual recursive choices, and whether those choices force
Cloitre's ratio to converge.

All reading links work in your browser; no installation or GitHub account is
needed. If the PDF preview does not load, use its download-arrow button.
The source programs and JSON evidence are optional for readers.

## Work on the project

The default branch, **main**, presents reviewed results by mathematical topic.
Follow work in progress in **[open pull requests](https://github.com/the-omega-institute/nested-recurrences/pulls)**.
Completed work is checked, merged, and its branch deleted. Scratch experiments
and correspondence stay outside the public tree.

See **[Contributing and verification](CONTRIBUTING.md)** for the PR workflow
and reproduction command. Mathematical comments are also welcome in the
existing collaboration thread; using GitHub is optional.

The current results are written proofs and computer-assisted proofs with
explicit finite certificates. This repository does not currently contain
a Lean formalization.

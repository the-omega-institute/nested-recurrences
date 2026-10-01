# Nested recurrences

How much complexity can a recurrence create when its own earlier values
decide how deeply to recurse? This project studies two examples proposed by
John M. Campbell and Benoît Cloitre, inspired by the nested recurrences
discussed by Hofstadter.

We have solved Campbell's example. For Cloitre's example, we have proved
golden-ratio bounds and exact Fibonacci structure; convergence over all
integers remains open.

## Read the mathematics

**Start with [What are we studying?](GENERAL.md)** for the definitions and
motivation. Then choose a sequence:

| Sequence | Current result | Read next |
|---|---|---|
| Campbell | Complete formula; the ratio does not converge. | [Three-page proof PDF](campbell/note.pdf) · [Guide](campbell/README.md) |
| Cloitre | Golden lower bound and Fibonacci identities; the full limit is open. | [Definition and proof route](cloitre-conway/README.md) |

For a project-wide overview, read **[Results and open questions](STATUS.md)**.
The current research asks what determines Cloitre's recursive choices and
whether those choices force its ratio to converge.

No installation or GitHub account is needed to read the notes. If the PDF
preview does not load, use its download-arrow button. Programs and JSON
evidence sit in each sequence's `verification/` folder and are optional reading.

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

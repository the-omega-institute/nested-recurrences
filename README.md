# Nested recurrences

This project studies sequences whose earlier values determine how deeply
the next term recurses. John M. Campbell and Benoît Cloitre proposed the
two examples below. We study their exact values, inner cycles, and
long-term behavior.

**Campbell's example has a complete solution. For Cloitre's example, the
main open question is whether the ratio of each term to its index converges
to the reciprocal of the golden ratio.**

## Read the mathematics

Start with **[What are we studying?](GENERAL.md)** for the definitions and
motivation, then choose a reading route:

- **[Campbell: the complete solution](campbell/README.md)** — explicit formula
  and short inner cycles; **[read the three-page proof PDF](campbell/note.pdf)**.
- **[Cloitre: the golden-ratio problem](cloitre-conway/README.md)** — what is
  proved, the main proof, and the remaining convergence question.

**[Results and open questions](STATUS.md)** gives an overview of both examples.
Detailed arguments and their finite premises live in the linked proof notes.

All reading links work in your browser; no installation or GitHub account is
needed. If the PDF preview does not load, use its download-arrow button.
The source programs and JSON evidence are optional for readers.

## Work on the project

The default branch, **main**, presents reviewed results by mathematical topic.
Work in progress belongs in **pull requests**; ready work is checked and merged.
Scratch experiments, alternate drafts, and correspondence stay outside the
public tree. Earlier versions remain available in Git history.

See **[Contributing and verification](CONTRIBUTING.md)** for the PR workflow
and reproduction command. Mathematical comments are also welcome in the
existing collaboration thread; using GitHub is optional.

The current results are written proofs and computer-assisted proofs with
explicit finite certificates. This repository does not currently contain
a Lean formalization.

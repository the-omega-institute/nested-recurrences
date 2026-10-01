# Nested recurrences

What happens when a recursive sequence decides how deeply to recurse using
its own earlier values? This project studies two examples proposed by
John M. Campbell and Benoît Cloitre. We seek exact formulas, a description
of their inner cycles, and proofs of their long-term behavior.

**Campbell's example is solved by an explicit formula. Cloitre's Conway-type
example has a proved golden-ratio structure; its full limit and decay rate
remain open.**

## Read the mathematics

Everything here can be read in your browser, without installing software or
having a GitHub account. Start with either example:

- **[Campbell's recurrence](campbell/README.md)** — definition and complete
  solution, with a **[three-page proof PDF](campbell/note.pdf)**.
- **[Cloitre's Conway-type recurrence](cloitre-conway/README.md)** — definition,
  main results, and a guided route to the open limit question.

For context, read **[What are we studying?](GENERAL.md)**. For a compact account
of what is proved and what remains open, read **[Research status](STATUS.md)**.

Click a document link to read it, then use your browser's Back button to return.
If the PDF preview does not load, use GitHub's download-arrow button.
You can ignore the Code button and the source-file list.

## Work on the project

The public default branch contains reviewed proofs and reproducible evidence.
New work is developed in **pull requests** and merged when ready. Intermediate
experiments and correspondence stay outside the public tree; earlier versions
remain available in Git history.

See **[Contribution and verification guide](CONTRIBUTING.md)** for the workflow
and the command that reproduces the computations. Mathematical comments can
also be shared in our existing discussion; using GitHub is optional.

The current results are written proofs and computer-assisted proofs with
explicit finite certificates. This repository does not currently contain
a Lean formalization.

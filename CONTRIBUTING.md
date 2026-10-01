# Contributing and verifying results

[Project home](README.md) · [Research status](STATUS.md)

Mathematical comments, corrections, and proofs are welcome. You can use our
existing discussion without learning GitHub. This guide is for contributors
who want to change the repository or reproduce its evidence.

## Branch, pull request, review, merge

1. Fetch the latest default branch and develop each coherent change on its
   own branch, using an isolated worktree when other work is in progress.
2. Keep a pull request focused on one result or one documentation change.
   Open a draft PR for ongoing work. Explain the problem, the resulting
   statement, and the validation performed; update that description to match
   the final scope before requesting review.
   Readers should be able to tell from the PR description which question is
   being investigated, what is established, and what still needs checking.
3. Update the relevant proof, compact evidence, and status together. Separate
   proved statements, computer-assisted proofs, finite observations, and open
   conjectures. Preserve attribution and exact initial conditions.
4. Before marking a research PR ready, give the complete argument, exact
   domains, attribution, and any finite premises together with their
   independent verification. A promising computation alone does not qualify
   as a proved infinite result.
5. Review the complete diff and run checks appropriate to the change. Merge
   ready work to `main` only after the checks and review pass, then delete
   its completed branch. Do not push research changes directly to `main`.
   Remove the completed local worktree and branch as well, after confirming
   the merge and preserving any unrelated local work.

For documentation-only PRs, check relative links and anchors, review the
rendered reading route, and confirm that mathematical claims still agree
with the linked proofs. Reproduce the affected mathematical evidence when
proofs, programs or finite certificates change.

There is currently no `dev` branch. Creating another integration branch is
unnecessary for this workflow. A PR records developing work; `main` presents
the current reviewed material. Do not change shared CI or publication
infrastructure to accommodate an individual experiment.

## Keep the public tree readable

Use [the research map](cloitre-conway/README.md#technical-research-map) to find
the note corresponding to a topic. Maintain that note rather than appending
unrelated results to a single file. Add a separate topic only when it helps
a reader follow the mathematical dependency.

Keep the root README an introduction and reading route. Summarize durable
results and open questions in STATUS.md; put theorem thresholds, selector
cases, and individual computational witnesses in the relevant proof note.
Do not turn either entry page into a log of successive experiments.
Keep theorem constants and computational counts in proof notes and evidence;
the entry pages should explain what the result means and where to read it.

Keep programs and compact, reproducible JSON evidence in the family's
`verification/` directory. Scratch runs, alternate drafts, correspondence,
mailbox identifiers, and collaboration-management records belong outside
this public repository. Git history retains earlier stages; do not add dated
public archives. Preserve cited proof paths and anchors with short navigation
links if material moves.

## Reproduce the evidence

With Python 3.10 or newer, from the repository's root:

```sh
python3 scripts/verify.py
```

Only the Python standard library is required. The command reruns eight checks,
compares exact JSON output against committed evidence, and checks recorded
source hashes. It does not overwrite the evidence.

The checks cover Campbell's symbolic proof and independent sequence evaluation;
the Conway evaluators and golden-structure finite premises; Fibonacci collar
and cycle diagnostics; the first arch blocks' five-window certificate; the
generic reflection-window interface; and the selector payload audit.

For the larger Fibonacci landing and shifted-family audit through F_36:

```sh
python3 scripts/verify.py --extended
```

Run without `-O` or `PYTHONOPTIMIZE`: assertions perform mathematical checks.
Narrower programs are suitable while developing; run the affected checks before
merging. A prose-only reorganization requires link and content checks, rather
than new sequence calculations when programs and evidence are unchanged.

The Conway checks use independent full-orbit and Brent evaluators, with
a separate literal calculation over a smaller prefix. The original
[evaluator](cloitre-conway/verification/conway_explore.py) defaults to
1,048,576 terms and a literal check through 4096; its
[recorded output](cloitre-conway/verification/conway-results.json) contains
the finite certificates and orbit witnesses. The extended
[audit](cloitre-conway/verification/landing_audit.py) reaches
F_36=14,930,352 and checks three shifted variants. That larger finite audit
does not prove a limit or universal shifted-family law.

The [Campbell guide](campbell/README.md#optional-computational-checks) explains
optional PDF rebuilding.

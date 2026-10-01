# Research collaboration

Read README.md and STATUS.md before continuing a recurrence. Attribute the
initial b-sequence to John M. Campbell and the variable-depth Conway candidate
to Benoît Cloitre. Preserve the unsigned Campbell note; a paper author list
has not been established here.

Read GENERAL.md for context and CONTRIBUTING.md for the PR workflow. Use the
Conway guide's topic map instead of appending unrelated work to a single note.

Keep written proofs, computer-assisted theorems, finite observations and open
conjectures distinct. State indexing and initial conditions exactly. Never
promote a checked prefix into a theorem without an independent propagation or
induction argument. No Lean validation is claimed for the present results.

This is a PUBLIC repository. Keep private correspondence, mailbox identifiers,
addresses, credentials and collaboration-management records outside it.
Research code, mathematical notes and compact evidence belong here.

Keep the public tree small and readable. Maintain the current proofs and status
in place; put necessary code and evidence in verification/ subdirectories.
Keep exploratory runs, draft variants and correspondence local or private.
Use Git history for superseded stages instead of adding dated public archives.
Keep README.md a short introduction and reading route; STATUS.md summarizes
durable results and open questions rather than successive research stages.
Keep thresholds, selector cases and individual witnesses in topic proof notes.
Preserve published proof URLs and distinguish historical experiment labels
from current theorem status. Formalization is a separate research decision,
not a prerequisite for every update.

The user explicitly authorized creation and timely synchronization of this
repository on 2026-09-30, and a PR-only workflow on 2026-10-01. Fetch first and
reconcile concurrent changes. Develop work on focused branches, with isolated
worktrees as needed; do not commit or push research directly to main. Update
STATUS.md, the relevant proofs and evidence, run the appropriate checks, and
review the complete diff. Open a PR and merge ready, verified work into the
existing main branch. The user authorized these merges; no dev branch is needed.
Use draft PRs for ongoing work. Before a research PR is ready, complete the
argument and state domains, attribution, and independently checked finite
premises. Delete the completed remote branch after merging.
Update the corresponding private collaboration record
with the exact public commit and remaining proof questions. Report push failures.

Use scripts/verify.py for full reproduction; narrower checks are suitable
while developing. Do not run Python with optimizations that disable assertions.
Do not add CI or publication infrastructure merely to run a local experiment.
No email sending is authorized by these repository instructions.

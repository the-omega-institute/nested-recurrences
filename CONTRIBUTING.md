# Contributing and verifying results

[Project home](README.md) · [Research status](STATUS.md)

Mathematical comments, corrections, and proofs are welcome. You can use our
existing discussion without learning GitHub. This guide is for contributors
who want to change the repository or reproduce its evidence.

## Branch, pull request, review, merge

1. Fetch the latest default branch and develop each coherent change on its
   own branch, using an isolated worktree when other work is in progress.
2. Keep a pull request focused on one result or one documentation change.
   Open a draft PR when the first coherent change can be reviewed, and keep
   unfinished arguments on that branch. Explain the problem, the resulting
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

The default branch is a reading edition: introductions, current proofs and
compact reproducibility evidence. A draft PR is the place for an unfinished
change; its description carries the current question and validation status.
Do not add a second public copy of the same developing note to `main`.

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

For selected landing displacements through 2^24, run
`python3 cloitre-conway/verification/landing_displacement.py`.
It reports exact dyadic-shell extrema, checks the prescribed depth and
successor indexing, and compares with independent evaluators and literal
nesting. This separate larger check is not part of the eight default
replays. Its finite shell maxima do not prove an asymptotic displacement
bound; see the [one-sided criterion](cloitre-conway/dispersion.md#a-one-sided-landing-displacement-criterion).

For the [maximum principle, contact budget and canonical clock rules](cloitre-conway/dispersion.md#a-finite-window-maximum-principle),
the compact evidence is
[canonical-erosion.json](cloitre-conway/verification/canonical-erosion.json).
Its three components have separate reproduction commands:

```sh
c++ -O3 -std=c++17 -Wall -Wextra -Werror cloitre-conway/verification/canonical_erosion.cpp -o /tmp/canonical_erosion
/tmp/canonical_erosion 267914295 --certificate
/tmp/canonical_erosion 33554432
python3 cloitre-conway/verification/canonical_erosion_check.py
```

The first run reproduces `tail_certificate`, the second `contacts`, and
the Python run `clock_check`. Source hashes are recorded alongside them.
The full certificate stores about 1 GiB of sequence values and checks
every index in [F_40,F_42); it does not depend on an author-supplied array.
The contact run stores about 256 MiB and covers complete contact domains
through level 37. The Python checker uses a different, full visited-state
orbit evaluator through 131072. These optional larger checks are separate
from the eight default replays. Only the finite-window maximum principle
turns its stated finite comparisons into an infinite-tail assertion;
the contact and clock observations do not establish global convergence.

For the complementary-drawdown conjecture and parity geometry, build
the separate two-evaluator check:

```sh
c++ -O3 -std=c++17 -Wall -Wextra -Werror cloitre-conway/verification/drawdown_geometry.cpp -o /tmp/drawdown_geometry
/tmp/drawdown_geometry 134217728
/tmp/drawdown_geometry 134217728 --visited
```

The two commands must return identical JSON, recorded in
[drawdown-geometry.json](cloitre-conway/verification/drawdown-geometry.json).
The default route uses Brent cycle skipping and about 512 MiB for this
prefix; `--visited` stores each full orbit with timestamped state arrays
and uses about 1.5 GiB. Both check literal values and selected splits
through 4096. Run either with a smaller limit while developing.
The recorded 495-term witness is a fixed interval; a larger run can find
a different longest interval. The prefix observations do not prove the
conjectured inequality or a convergence rate.

For the contact-frontier entrance bounds and five-input clock theorem:

```sh
python3 cloitre-conway/verification/frontier_dynamics_check.py
```

Compare its JSON with
[frontier-dynamics.json](cloitre-conway/verification/frontier-dynamics.json).
This separate check tests both propagated minorants, quantitative first
capture, cycle localization, all eligible gated frontiers in its prefix,
the explicit nongating counterexample, and the exact cycle-geometry
inequalities at all non-anchor contacts in its prefix. The infinite conclusions use
the written arguments in [frontier dynamics](cloitre-conway/frontier-dynamics.md).

For the exact earlier-row feedback and uniform basin exclusion:

```sh
python3 cloitre-conway/verification/earlier_row_check.py
```

Compare its JSON with
[earlier-row.json](cloitre-conway/verification/earlier-row.json).
The checker uses only values below F_20 to evaluate all 909 paired seeds
and remaining clocks, then repeats every case by literal iteration. It
checks the interval synchronization certificate and compares the earlier
prefix with an independent literal construction through 6919. The finite
certificate proves its stated six-input exclusion; it gives no uniform
asymptotic contraction.

For canonical copy or erasure in the doubled saturated band:

```sh
python3 cloitre-conway/verification/doubled_band_check.py
```

Compare its JSON with
[doubled-band.json](cloitre-conway/verification/doubled-band.json).
Independent full-orbit and Brent values agree through832302; all326selected
clocks in four bands are replayed literally. Complete captured-seed cycles
and a finite abstract profile check corroborate the
[infinite theorem](cloitre-conway/exact-collars.md#canonical-copying-in-a-doubled-saturated-band).
This optional check is separate from the eight default replays.

For simultaneous extinction of binary or even cap defects:

```sh
python3 cloitre-conway/verification/binary_erasure_check.py
```

Compare its JSON with
[binary-erasure.json](cloitre-conway/verification/binary-erasure.json).
The exhaustive 18-state certificate proves an arbitrary-length binary
feedback identity; the [written proof](cloitre-conway/exact-collars.md#simultaneous-extinction-of-binary-cap-defects)
derives that identity from the actual orbit and prescribed depth.
Independent full-orbit and Brent values through 832302, with a literal prefix
through 4096, corroborate its canonical application. These finite sequence
checks alone do not prove extinction. This optional check is separate from
the eight default replays.

The same program exhausts small even source profiles and single-position
lower probes, with the proved parity restrictions, to corroborate the
[even-defect argument](cloitre-conway/exact-collars.md#even-cap-defects-vanish-by-parity).
That argument is a written proof and does not require a finite-state certificate.

For simultaneous extinction of mixed zero/unit/amplitude-two cap defects:

```sh
python3 cloitre-conway/verification/ternary_erasure_check.py
```

Compare its JSON with
[ternary-erasure.json](cloitre-conway/verification/ternary-erasure.json).
Two separately implemented whole-word transductions agree as languages at
every stage, for both collar parities, and certify the arbitrary-length zero
rows. The [written argument](cloitre-conway/exact-collars.md#simultaneous-extinction-of-ternary-cap-defects)
derives the actual gated routing rule and accounts for the right boundary
of the finite source window. No sequence data or spatial cutoff enters the
automaton certificate. This optional check is separate from the eight default
replays; it does not establish an unconditional collar-growth rate or full
convergence.

The same checker verifies an explicit amplitude-three traveling history
for the relaxed routing rule. Its finite prefix and periodic tail give an
infinite obstruction to extending that relaxation's uniform extinction
claim. This is not a counterexample to the canonical recurrence; see the
[method limitation](cloitre-conway/exact-collars.md#an-amplitude-three-traveling-history-limits-the-relaxed-routing-method).

For the global selected-tree golden-excess budget:

```sh
python3 cloitre-conway/verification/golden_budget_check.py
```

Compare its JSON with
[golden-budget.json](cloitre-conway/verification/golden-budget.json).
Full-orbit and Brent construction agree through131072; literal construction
and selected phases agree through4096. The explicit finite premise is every
actual split below65536. Higher cases and tree/spine counts corroborate the
[infinite budget proof](cloitre-conway/golden-proof.md#9-a-global-integer-budget-for-the-selected-recursion-tree).
This separate check does not claim global dispersion or convergence.

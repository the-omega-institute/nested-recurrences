# Cloitre's variable-depth Conway candidate

[Back to the research overview](../README.md) · [Current research status](../STATUS.md)

## Read the research note

**[Open the global golden-structure proof](golden-proof.md).** It is displayed directly as a
web page; no download, installation or GitHub account is needed.

**Latest proof:** [Global golden structure](golden-proof.md). The introduction
lists the completed theorems: the G lower bound, exact equality set, Fibonacci
identities and landing, upper cap and golden-ratio liminf. Sections 4 and 6
contain the two inductions; Section 7 explains the finite certificate and how
to reproduce it.

The [earlier landing development](landing.md) records the intermediate route,
the independent checks through F_36 and the corrected decay observations.

For the earlier proofs and computational context, read the
[first-results note](proof.md) in this order:

1. [Definition and result summary](proof.md#definition-and-result-status): the
   precise recurrence and the distinction between proofs and observations.
2. [Global ratio bounds](proof.md#3-finite-window-propagation-and-explicit-infinite-bounds):
   how a finite exact certificate yields a bound for every sufficiently large index.
3. [Corrections to the numerical conjectures](proof.md#5-independent-reproduction-and-corrections):
   the four additional equality indices and the refined conjecture.
4. [The next proof problem](proof.md#6-more-structural-evidence-and-the-remaining-proof-problem):
   the Fibonacci fixed point and what is still needed to prove that the orbit reaches it.

Sections 1, 2 and 4 supply the detailed well-definedness, split-separation and
cycle-entry arguments. The exact G lower bound, Fibonacci identity and refined
equality-set description were open at that first-results stage and are now proved
in the latest note. Comments and proposed arguments
can be shared in the existing email thread.

## Optional computational checks

The recorded data and code are for auditing the computation; they are not
required reading. With Python 3.10 or newer, open a terminal in this directory
and run:

```sh
python3 conway_explore.py --output replay.json
```

The default limit is 1,048,576. The program generates separate sequences using
full-orbit and Brent evaluators, checks their equality, and also compares a
literal 4,096-term calculation. It uses only Python's standard library. Run
without `-O` or `PYTHONOPTIMIZE` because assertions implement the checks.

[conway-results.json](conway-results.json) contains the committed output,
including source and sequence hashes, exact finite-window certificates,
equality counterexamples, Fibonacci checks and complete long-cycle witnesses.
The root command `python3 scripts/verify.py` reruns all repository checks and
compares their output with committed evidence.

The larger [landing audit](landing_audit.py) has separate recorded output in
[landing-audit.json](landing-audit.json). From the repository's main folder,
`python3 scripts/verify.py --extended` also replays and compares this audit.
It reaches 14,930,352 terms and takes longer than the original checks; it uses
a compact array to keep sequence storage modest.

The finite-window certificates yield universal rational bounds through the
propagation proof. The new [finite golden-structure certificate](golden-check.json)
supports the universal induction and is replayed by `python3 scripts/verify.py`.
Full convergence to 1/phi and decay rates remain conjectures.

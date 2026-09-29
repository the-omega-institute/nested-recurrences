# Cloitre's variable-depth Conway candidate

Read [proof.md](proof.md) for the precise recurrence, proved results, corrected
finite observations and open conjectures.

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

The finite-window certificates yield universal rational bounds through the
separate propagation proof. The exact G lower bound, Fibonacci identity and
refined equality-set description remain conjectures.

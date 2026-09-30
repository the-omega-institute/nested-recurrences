"""Replay the committed mathematical evidence without changing it."""

import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--extended', action='store_true', help='Also replay the Fibonacci landing audit through F_36.')
    arguments = parser.parse_args()
    if not __debug__ or os.environ.get('PYTHONOPTIMIZE'):
        raise SystemExit('Run without -O or PYTHONOPTIMIZE; assertions perform the checks.')
    root = Path(__file__).resolve().parents[1]
    checks = [
        ('Campbell symbolic interval proof', root / 'campbell/check_proof.py', root / 'campbell/proof-check.json'),
        ('Campbell million-term and literal comparison', root / 'campbell/explore.py', root / 'campbell/results.json'),
        ('Cloitre Conway independent evaluators and certificates', root / 'cloitre-conway/conway_explore.py', root / 'cloitre-conway/conway-results.json'),
        ('Global golden-structure finite premises', root / 'cloitre-conway/golden_check.py', root / 'cloitre-conway/golden-check.json'),
    ]
    if arguments.extended:
        checks.append(('Fibonacci landing and shifted family audit',
                       root / 'cloitre-conway/landing_audit.py', root / 'cloitre-conway/landing-audit.json'))
    for label, program, expected_path in checks:
        print(label, flush=True)
        completed = subprocess.run(
            [sys.executable, str(program)], check=True, capture_output=True, text=True,
            cwd=program.parent,
        )
        actual = json.loads(completed.stdout)
        expected = json.loads(expected_path.read_text())
        if actual != expected:
            raise SystemExit(f'Recorded evidence differs: {expected_path.relative_to(root)}')
        if 'source_sha256' in expected:
            digest = hashlib.sha256(program.read_bytes()).hexdigest()
            if digest != expected['source_sha256']:
                raise SystemExit(f'Source hash differs: {program.relative_to(root)}')
        if 'evaluator_source_sha256' in expected:
            evaluator = root / 'cloitre-conway/conway_explore.py'
            if hashlib.sha256(evaluator.read_bytes()).hexdigest() != expected['evaluator_source_sha256']:
                raise SystemExit('Shared Conway evaluator source hash differs.')
        print('  passed; exact JSON matches committed evidence', flush=True)
    print(f'All {len(checks)} reproduction checks passed.')


if __name__ == '__main__':
    main()

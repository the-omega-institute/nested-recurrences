"""Replay the committed mathematical evidence without changing it."""

import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys


def main():
    if not __debug__ or os.environ.get('PYTHONOPTIMIZE'):
        raise SystemExit('Run without -O or PYTHONOPTIMIZE; assertions perform the checks.')
    root = Path(__file__).resolve().parents[1]
    checks = [
        ('Campbell symbolic interval proof', root / 'campbell/check_proof.py', root / 'campbell/proof-check.json'),
        ('Campbell million-term and literal comparison', root / 'campbell/explore.py', root / 'campbell/results.json'),
        ('Cloitre Conway independent evaluators and certificates', root / 'cloitre-conway/conway_explore.py', root / 'cloitre-conway/conway-results.json'),
    ]
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
        print('  passed; exact JSON matches committed evidence', flush=True)
    print('All three reproduction checks passed.')


if __name__ == '__main__':
    main()

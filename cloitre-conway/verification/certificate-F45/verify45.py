# Independent check of the certificate p*C(n) <= q*n on [F_j, F_{j+2}) from a raw uint32 dump of C.
import sys, numpy as np
path, j, ns, cs = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
C = np.memmap(path, dtype='<u4', mode='r')
F = [0, 1]
while len(F) < 60: F.append(F[-1] + F[-2])
lo, hi = F[j], F[j + 2]
assert len(C) > hi - 1, "dump too short"
assert int(C[ns]) == cs, "witness value differs"
viol = eq = 0
for start in range(lo, hi, 20_000_000):
    end = min(hi, start + 20_000_000)
    c = np.asarray(C[start:end], dtype=np.int64)
    n = np.arange(start, end, dtype=np.int64)
    lhs, rhs = c * ns, n * cs
    viol += int(np.count_nonzero(lhs > rhs)); eq += int(np.count_nonzero(lhs == rhs))
print(f"[F_{j}, F_{j+2}) = [{lo}, {hi}): {hi - lo} indices, violations {viol}, equalities {eq}, witness C({ns}) = {cs}")
from fractions import Fraction
r = Fraction(cs, ns); print("ratio", r, float(r), "minus alpha", float(r) - (5 ** 0.5 - 1) / 2)

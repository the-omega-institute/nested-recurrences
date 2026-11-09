/* Meta Conway C(n) up to N with C only in memory (uint32), cycle detection by a small hash table.
 * Exact maximum of C(n)/n on every Fibonacci block [F_k, F_{k+1}), prefix check against an earlier dump,
 * optional dump of C as little-endian uint32 C[0..N].
 * usage: cmax N prefix_C.bin prefix_len out_C.bin|-  */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <math.h>
#include <time.h>

#define HB 16
#define HS (1u << HB)
static uint32_t hkey[HS], hidx[HS], hstamp[HS], orb[HS];

int main(int argc, char **argv) {
    long N = atol(argv[1]);
    uint32_t *a = malloc((size_t)(N + 1) * sizeof(uint32_t));
    if (!a) { fprintf(stderr, "malloc failed\n"); return 1; }
    long F[100]; F[0] = 0; F[1] = 1;
    for (int j = 2; j <= 92; j++) F[j] = F[j - 1] + F[j - 2];
    int K = 1; while (F[K + 1] <= N) K++;
    /* block maxima: bn/bd, indexed by k with F_k <= n < F_{k+1} */
    uint64_t bnum[100] = {0}, bden[100] = {0};
    a[0] = 0; a[1] = a[2] = 1;
    int k = 3; while (F[k + 1] <= 3) k++;
    long maxlen = 0, maxper = 0;
    time_t t0 = time(NULL);
    for (long n = 3; n <= N; n++) {
        uint32_t h = a[n - 1], x = (uint32_t)(n - 1), i = 0, g = 0;
        for (;;) {
            uint32_t s = (x * 2654435761u) >> (32 - HB);
            int found = 0;
            while (hstamp[s] == (uint32_t)n) {
                if (hkey[s] == x) { found = 1; break; }
                s = (s + 1) & (HS - 1);
            }
            if (found) {
                uint32_t mu = hidx[s], L = i - mu;
                g = orb[mu + (h - mu) % L];
                if (L > maxper) maxper = L;
                break;
            }
            if (i == h) { g = x; break; }
            if (i + 1 >= HS / 2) { fprintf(stderr, "orbit too long at n=%ld\n", n); return 1; }
            hstamp[s] = (uint32_t)n; hkey[s] = x; hidx[s] = i; orb[i] = x; i++;
            x = (uint32_t)(n - a[x]);
        }
        if (i > maxlen) maxlen = i;
        a[n] = a[g] + a[n - g];
        while (F[k + 1] <= n) k++;
        if (bden[k] == 0 || (unsigned __int128)a[n] * bden[k] > (unsigned __int128)bnum[k] * (uint64_t)n) { bnum[k] = a[n]; bden[k] = n; }
        if ((n & ((1L << 26) - 1)) == 0) { fprintf(stderr, "n = 2^%d reached after %ld s (max orbit %ld, max period %ld)\n", (int)log2((double)n), (long)(time(NULL) - t0), maxlen, maxper); }
    }
    fprintf(stderr, "done after %ld s, max orbit length %ld, max period %ld\n", (long)(time(NULL) - t0), maxlen, maxper);
    /* prefix check */
    long P = atol(argv[3]);
    FILE *f = fopen(argv[2], "rb");
    if (f) {
        long bad = 0; uint32_t buf[1 << 16]; long pos = 0;
        while (pos <= P) {
            size_t want = (P + 1 - pos) < (1 << 16) ? (size_t)(P + 1 - pos) : (1 << 16);
            size_t got = fread(buf, 4, want, f); if (got == 0) break;
            for (size_t j = 0; j < got; j++) if (buf[j] != a[pos + j]) bad++;
            pos += got;
        }
        fclose(f);
        printf("prefix check against %s on 0..%ld: %ld mismatches (%ld values read)\n", argv[2], P, bad, pos);
    }
    const double al = (sqrt(5.0) - 1) / 2;
    printf(" k   block max C(n)/n - alpha      at n           C(n)\n");
    for (int j = 20; j < K; j++) if (bden[j] && F[j + 1] - 1 <= N)
        printf("%2d   %.12f            %11lu   %11lu\n", j, (double)bnum[j] / bden[j] - al, (unsigned long)bden[j], (unsigned long)bnum[j]);
    /* certificates over two consecutive complete blocks [F_j, F_{j+2}) */
    for (int j = 38; j + 2 <= K && F[j + 2] - 1 <= N; j++) {
        int w = ((unsigned __int128)bnum[j] * bden[j + 1] >= (unsigned __int128)bnum[j + 1] * bden[j]) ? j : j + 1;
        uint64_t p = bnum[w], q = bden[w], r = p, s2 = q; while (s2) { uint64_t t = r % s2; r = s2; s2 = t; }
        printf("certificate on [F_%d, F_%d): max at n* = %lu, C(n*) = %lu, ratio = %.12f, reduced %lu/%lu\n",
               j, j + 2, (unsigned long)q, (unsigned long)p, (double)p / q, (unsigned long)(p / r), (unsigned long)(q / r));
    }
    if (strcmp(argv[4], "-") != 0) {
        FILE *o = fopen(argv[4], "wb");
        if (!o || fwrite(a, 4, (size_t)(N + 1), o) != (size_t)(N + 1)) { fprintf(stderr, "write failed\n"); return 1; }
        fclose(o); fprintf(stderr, "wrote %s\n", argv[4]);
    }
    return 0;
}

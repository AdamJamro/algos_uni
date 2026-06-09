#include <stdio.h>
#include <string.h>
#include <stdlib.h>


#define uint size_t

size_t max_prefix_suffix_overlap(const char *x, const size_t len_x, const char *y, const size_t len_y) {
    for (size_t k = len_x > len_y ? len_y : len_x; k > 0; k--) {
        if (memcmp(x, &y[len_y - k], k) == 0) {
            return k;
        }
    }
    return 0;
}

int* build_kmp_table(const char *W, const size_t length_W) {
    int* T = malloc((length_W + 1) * sizeof(int));

    T[0] = -1;
    if (length_W == 0) return T;
    T[1] = 0;

    for (size_t k = 2; k <= length_W; k++) {
        T[k] = (int)max_prefix_suffix_overlap(W, k - 1, &W[1], k - 1);
    }
    return T;
}

size_t* kmp_search(const char *S, const char *W, int *nP) {
    // returns a pointer to an m-allocated array
    // returns positions where W is found in S, and sets nP to the number of positions found

    size_t length_S = strlen(S); // char stream
    size_t length_W = strlen(W); // pattern
    *nP = 0;

    if (length_W == 0) return NULL;
    int* T = build_kmp_table(W, length_W);
    size_t* P = malloc(length_S * sizeof(size_t));

    size_t j = 0; // current position in S
    int k = 0; // current position in W

    while (j < length_S) {
        if (W[k] == S[j]) {
            j = j + 1;
            k = k + 1;
            if (k == length_W) {
                P[*nP] = j - k;
                (*nP)++;
                k = T[k];
            }
        } else {
            k = T[k];
            if (k < 0) {
                j = j + 1;
                k = k + 1; // k = 0
            }
        }
    }

    free(T);
    return P;
}

int main() {

    // Test max_prefix_suffix_overlap
    const char* x = "abcdef";
    const char* y = "xyzabc";

    size_t k = max_prefix_suffix_overlap(x,strlen(x), y, strlen(y));
    printf("Najwieksze k dla (%s, %s): %zu\n", x, y, k);

    // Test build_kmp_table
    const char *pattern = "ABABCAB";
    const size_t pattern_len = strlen(pattern);
    int* T = build_kmp_table(pattern, pattern_len);
    printf("KMP Table for W: %s\n", pattern);
    for (size_t i = 0;i < pattern_len; i++) {
        printf("T[%zu] = %d\n", i, T[i]);
    }
    free(T);


    // Test kmp_search
    const char *S = "ABCABCDABABABCDABBAABABCDABDEABCDABABCDABCDABDEABABABABCDABBAABABCDABBAABAB";
    const char *W = "ABABCDABBAABAB";
    int nP = 0;

    size_t* P = kmp_search(S, W, &nP);

    printf("Match count (nP): %d\n", nP);
    for (int i = 0; i < nP; i++) {
        printf("Match no %d: %zu\n", i, P[i]);
        // printf("Text: ");
        // size_t radius = 10;
        // for (size_t j = i)
    }

    free(P);
    return 0;
}

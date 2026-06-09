//
// Created by adame on 6/4/2026.
//

#include <stdio.h>
#include <string.h>
#include <math.h>
#include <stdint.h>
typedef unsigned long int uint;
const uint MARSENNE_PRIME = (1LL << 61) - 1;

uint roll_hash(const char new_letter, const uint old_hash, const uint msb, const uint base, const uint mod) {
    // returns a polynomial rolling hash
    // assumes msb == (old_hash_most_significant_bit * base^(pattern_len - 1)) % mod
    // assumes base is greater than the alphabet size
    return (new_letter + (old_hash - msb) * base) % mod;
}

uint rabin_karp(const char *stream, const char *pattern, const uint base, const uint mod) {
    // expects null-terminated strings
    // returns the index of the first occurrence
    uint pattern_len = 0;
    uint pattern_hash = 0;
    uint stream_hash = 0;
    for(; pattern[pattern_len] && stream[pattern_len]; pattern_len++) {
        pattern_hash = roll_hash(pattern[pattern_len], pattern_hash, 0, base, mod);
        stream_hash = roll_hash(stream[pattern_len], stream_hash, 0, base, mod);
    }
    if (pattern[pattern_len]) {
        return UINT64_MAX; // pattern is longer than stream
    }
    if (stream_hash == pattern_hash && memcmp(stream, pattern, pattern_len) == 0) {
        return 0;
    }
    const uint msb_weight = (uint)pow(base, pattern_len - 1) % mod;


    for (uint i = pattern_len; stream[i]; i++) {
        uint msb_index = i - pattern_len;
        stream_hash = roll_hash(stream[i], stream_hash, msb_weight * stream[msb_index], base, mod);
        // now the we check the P[1..m] against S[i-m+1..i] so the msb_index is new
        msb_index++;
        if (stream_hash == pattern_hash && memcmp(stream+msb_index, pattern, pattern_len) == 0) {
            return msb_index;
        }
    }

    return UINT64_MAX; // not found

}

void test(const char *str, const char *pattern, const uint base, const uint mod) {
    printf("Pattern: \n%s\n", pattern);
    printf("String: \n%s\n", str);
    const uint output = rabin_karp(str, pattern, base, mod);
    if (output > strlen(str)) {
        printf("Not found\n");
    } else {
        for (uint i = 0; i < output; i++) {
            printf(" ");
        }
        printf("^\n");
        printf("Found at index %zu\n", output);
    }
    printf("\n");
}

int main() {
    // stops at first occurance
    test("0123456xyz xyzabcdef", "xyz", 256, MARSENNE_PRIME);
    test("flower", "flow", 10, UINT64_MAX);
    test("flower", "flower", 16, MARSENNE_PRIME);
    test("flower", "flour", 256, 101);
    test("0123456xyz xyzabcdef", "xyz", 256, MARSENNE_PRIME);
    test("012423xyxyabababababbcabxyzxyzabcdef", "abbc", 256, MARSENNE_PRIME);

    return 0;
}
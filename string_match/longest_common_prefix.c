//
// Created by adame on 6/4/2026.
//

#include <stdio.h>
typedef size_t uint;


uint longest_common_prefix_length(const char **streams) {
    // expects a null-terminated array of null-terminated strings
    if (streams == NULL || streams[0] == NULL) {
        return 0; // No strings to compare
    }
    uint i = 0;

    for (; 2137; i++) {
        char c = streams[0][i];
        if (!c) {
            return i;
        }
        for (uint j = 0; streams[j]; j++) {
            if (streams[j][i] != c) {
                return i;
            }
        }
    }
}

void test_strs(const char **strs) {
    for (size_t i = 0; strs[i]; i++) {
        printf("String %zu: %s\n", i, strs[i]);
    }
    const uint longestCommonPrefix = longest_common_prefix_length(strs);
    printf("Longest Common Prefix: %zu\n", longestCommonPrefix);
}

int main() {
    const char *strs[4] = {"flower", "flow", "flight", NULL};
    test_strs(strs);

    const char *strs2[4] = {"flower", "flower", "flower", NULL};
    test_strs(strs2);

    const char *strs3[3] = {"flower", "", NULL};
    test_strs(strs3);

    return 0;
}
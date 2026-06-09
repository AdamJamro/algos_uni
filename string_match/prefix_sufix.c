#include <stdio.h>
#include <string.h>
#include <stdbool.h>

bool is_prefix(const char *str, const char *prefix) {
    size_t str_len = strlen(str);
    size_t prefix_len = strlen(prefix);

    if (prefix_len > str_len) {
        return false;
    }

    return memcmp(str, prefix, prefix_len) == 0;
}

bool is_suffix(const char *str, const char *suffix) {
    size_t str_len = strlen(str);
    size_t suffix_len = strlen(suffix);

    if (suffix_len > str_len) {
        return false;
    }

    return memcmp(&str[str_len - suffix_len], suffix, suffix_len) == 0;
}

int main() {
    const char *text = "programming";
    const char *input_A = "program";
    const char *input_B = "ing";
    const char *input_C = "ABC";

    printf("Tekst: %s\n", text);
    printf("Czy \t%s\t to prefix? %s\n", input_A, is_prefix(text, input_A) ? "Tak" : "Nie");
    printf("Czy \t%s\t to suffix? %s\n", input_B, is_suffix(text, input_B) ? "Tak" : "Nie");
    printf("Czy \t%s\t to prefix? %s\n", input_C, is_prefix(text, input_C) ? "Tak" : "Nie");
    
    return 0;
}

#include <stdio.h>
#include <string.h>

int naive_search_memcmp(const char *text, const char *pattern) {
    size_t text_len = strlen(text);
    size_t pattern_len = strlen(pattern);

    if (pattern_len == 0 || pattern_len > text_len) {
        return -1;
    }

    // Maksymalny indeks, pod którym może się jeszcze zmieścić wzorzec
    size_t max_shift = text_len - pattern_len;

    for (size_t i = 0; i <= max_shift; i++) {
        if (memcmp(&text[i], pattern, pattern_len) == 0) {
            return i;
        }
    }

    return -1;
}

int main() {
    const char *text = "ABABDABACDABABCABAB";
    const char *pattern = "ABABC";

    printf("Tekst: %s, ", text);
    printf("Wzorzec: %sn\n", pattern);
    printf("--- Wyniki wyszukiwania ---\n");
    
    size_t result = naive_search_memcmp(text, pattern);

    if (result == -1) {
        printf("Wzorzec nie znaleziony\n");
    } else {
        printf("Wzorzec znaleziony na indeksie: %zu\n", result);
    }
    return 0;
}

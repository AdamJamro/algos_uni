from functools import partial
from typing import Sequence

import numpy as np
from itertools import product


def lcs(seq1: Sequence, seq2: Sequence):
    m = len(seq1)
    n = len(seq2)

    # Create a 2D array to store lengths of longest common subsequence.
    L = [[0] * (n + 1) for _ in range(m + 1)]

    # Build the L array from bottom up
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if seq1[i - 1] == seq2[j - 1]:
                L[i][j] = L[i - 1][j - 1] + 1
            else:
                L[i][j] = max(L[i - 1][j], L[i][j - 1])

    return L[m][n]


def expected_value_of_lcs(alphabet_size=2, seq_length=5):
    """
    Uniform distribution is assumed for the sequences.
    """
    all_strings = np.array(list(product(range(2), repeat=5)))
    return np.mean(list(lcs(s1, s2) for s1 in all_strings for s2 in all_strings))


def test_lcs():
    seq1 = "A G G   T   A   B"
    seq2 =     "G X T Y A Z B"
    # GTAB
    strip = lambda x: str(x).replace(" ", "")
    assert lcs(strip(seq1), strip(seq2)) == 4
    assert lcs("AAAA", "AAAA") == 4
    assert lcs("AAAA", "BBBB") == 0
    assert lcs("", "BBBB") == 0
    assert lcs("AAAA", "") == 0

if __name__ == "__main__":
    test_lcs()

    alphabet_size, seq_length = 2, 5
    problem_set = f"{list(range(alphabet_size))}^{seq_length}"
    print(f"Expected length of LCS between: \n{problem_set} x {problem_set}\nis {expected_value_of_lcs(alphabet_size, seq_length)}")

import numpy as np


def get_omega(N, k=1.0, inverse=False):
    sign = 1 if inverse else -1
    return np.exp(sign * 2j * np.pi * k / N)


def get_omega_array(N, k=1, inverse=False):
    """
    get the k-th array of omega matrix
    """
    omega = get_omega(N, inverse)
    return omega ** np.arange(0, stop=N * k, step=k)


def get_omega_matrix(N, inverse=False):
    omega = get_omega(N, inverse)
    n = np.arange(N)
    k = n.reshape((N, 1))
    return omega ** (k * n)


def dft_matrix(x):
    """
    Worst: separately construct each entry of the DFT matrix W.
    W size N x N, where W[j, k] = omega^(j*k).
    This is the standard DFT matrix used in direct DFT computation.
    """
    return get_omega_matrix(len(x)) @ x


def dft_halfwaythere(x):
    """
    Better: DFT via Matrix Multiplication that tries to avoid redundant calculations.
    While the matrix construction is O(N^2),
    to evaluate the polynomial representation of each DFT bin.
    """
    x = np.asarray(x, dtype=np.complex128)
    N = len(x)
    W = np.zeros((N, N), dtype=np.complex128)
    omega_base = get_omega(N)

    for k in range(N):
        # The k-th row corresponds to the k-th harmonic
        # W_jk = (omega_base^k)^j. We compute this using Horner-like powers.
        row_omega = omega_base**k
        current_val = 1.0 + 0j
        for j in range(N):
            W[k, j] = current_val
            current_val *= row_omega

    return W @ x


def dft_horner(x):
    """
    DFT via Horner's Rule.
    Evaluates the polynomial representation of each DFT bin using Horner's method.
    This avoids explicitly constructing the full DFT matrix and reduces redundant calculations.
    """
    x = np.asarray(x, dtype=np.complex128)
    N = len(x)
    result = np.zeros(N, dtype=np.complex128)

    for k in range(N):
        # Compute the k-th DFT bin using Horner's method
        omega_k = get_omega(N, k)
        current_val = 0.0 + 0j
        for j in range(N - 1, -1, -1):
            current_val = current_val * omega_k + x[j]
        result[k] = current_val

    return result


def fdft(x):
    """
    Case 2: Fast DFT (Recursive implementation).
    Utilizes the Danielson-Lanczos lemma:
    DFT(x) = DFT(even) + weight * DFT(odd)
    Constraints: len(x) must be a power of 2.
    """
    N = len(x)

    # Base case
    if N <= 1:
        return x

    if N % 2 != 0:
        raise ValueError("Size of x must be a power of 2 for this FDFT implementation.")

    # Split into even and odd terms
    X_even = fdft(x[0::2])
    X_odd = fdft(x[1::2])

    # Calculate the twiddle factors: exp(-2j * pi * k / N)
    # We only need N/2 factors due to symmetry
    twiddles = np.exp(-2j * np.pi * np.arange(N // 2) / N)

    # Combine results
    # X[k] = E[k] + twiddle * O[k]
    # X[k + N/2] = E[k] - twiddle * O[k]
    first_half = X_even + twiddles * X_odd
    second_half = X_even - twiddles * X_odd

    return np.concatenate((first_half, second_half))


# --- Example Usage ---
if __name__ == "__main__":
    signal0 = np.array([1.0, 2.0, 1.0, -1.0, 1.5, 3.0, 4.0, 2.0])
    signal1 = np.array([1.0, 2.0, 1.0, -1.0, 1.5, 2.5, 3.5, 2.0])
    signal2 = np.array(
        [
            1.0,
            2.0,
            1.0,
            -1.0,
            1.5,
            2.5,
            3.5,
            2.0,
            1.0,
            2.0,
            1.0,
            -1.0,
            1.5,
            2.5,
            3.5,
            2.0,
        ]
    )
    for test_id, signal in enumerate(
        (
            signal0,
            signal1,
            signal2,
        )
    ):
        print(f"Testing case no.{test_id}\n{signal}...")

        res_matrix = dft_matrix(signal)
        res_horner = dft_horner(signal)
        res_recursive = fdft(signal)
        res_numpy = np.fft.fft(signal)

        assert np.allclose(res_matrix, res_numpy)
        assert np.allclose(res_horner, res_numpy)
        assert np.allclose(res_recursive, res_numpy)
        print("=" * 40)

    sample_input = np.random([1.0, 2.0, 1.0, -1.0, 1.5, 2.5, -0.5, 0.0])

    print("Original Input:\n", sample_input)
    print("-" * 40)

    # Compute using Case 1
    dft_result = dft_horner(sample_input)
    print("Case 1 (Horner's Rule Matrix) Result:\n", np.round(dft_result, 4))
    print("-" * 40)

    # Compute using Case 2
    fdft_result = fdft(sample_input)
    print("Case 2 (Recursive FDFT) Result:\n", np.round(fdft_result, 4))
    print("-" * 40)

    # Verify against numpy's highly optimized FFT
    np_result = np.fft.fft(sample_input)
    print("NumPy built-in FFT Result:\n", np.round(np_result, 4))

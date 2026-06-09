from typing import Sequence, List
import numpy as np

def naive_poly_mul(a, b) -> np.ndarray:
    """
    Naive polynomial multiplication (O(n^2)).
    Coefficients are assumed in increasing order (a[0] + a[1] x + ...).
    Returns numpy array of length len(a)+len(b)-1.
    """
    a = np.asarray(a, dtype=np.complex128)
    b = np.asarray(b, dtype=np.complex128)
    na, nb = a.size, b.size
    if na == 0 or nb == 0:
        return np.zeros(0, dtype=a.dtype)

    res = np.zeros(na + nb - 1, dtype=np.complex128)
    for i in range(na):
        for j in range(nb):
            res[i + j] += a[i] * b[j]
    # if inputs were real-valued, drop tiny imaginary parts
    if np.isrealobj(a) and np.isrealobj(b):
        res = np.real_if_close(res, tol=1000)
    return res


def _next_power_of_two(n: int) -> int:
    return 1 << (n - 1).bit_length()


def fft_polymul(a, b) -> np.ndarray:
    """
    Polynomial multiplication via FFT (using numpy.fft).
    Pads to next power of two >= len(a)+len(b)-1, computes FFTs, multiplies pointwise,
    then inverse FFT and trims to the correct length.
    """
    a = np.asarray(a)
    b = np.asarray(b)
    na, nb = a.size, b.size
    if na == 0 or nb == 0:
        return np.zeros(0, dtype=a.dtype)
    out_len = na + nb - 1
    nfft = _next_power_of_two(out_len)
    A = np.fft.fft(a, n=nfft)
    B = np.fft.fft(b, n=nfft)
    C = A * B
    c = np.fft.ifft(C)[:out_len]
    c = np.real_if_close(c, tol=1000)
    # # If both inputs were integer-valued, round to nearest integer
    # if np.allclose(a, np.round(a)) and np.allclose(b, np.round(b)):
    #     c = np.rint(c).astype(np.int64)
    return c


# --- quick checks ---
if __name__ == "__main__":
    a = [1, 2, 3]   # 1 + 2x + 3x^2
    b = [4, 0, -1]  # 4 - x^2
    r_naive = naive_poly_mul(a, b)
    r_fft = fft_polymul(a, b)
    r_conv = np.convolve(a, b)
    print("naive:", r_naive)
    print("fft:  ", r_fft)
    print("np.convolve:", r_conv)
    assert np.allclose(r_naive, r_conv)
    assert np.allclose(r_fft, r_conv)

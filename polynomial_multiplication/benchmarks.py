import numpy as np
import time
import matplotlib.pyplot as plt
import pandas as pd
from scipy.signal import fftconvolve

from polynomial_multiplication.poly_mul import naive_poly_mul, fft_polymul

sizes = [2**i for i in range(2, 12)]
times_naive = []
err_naive = []
times_fft = []
err_fft = []

for N in sizes:
    x = np.random.random(N)
    y = np.random.random(N)



    start = time.perf_counter()
    res_naive = naive_poly_mul(x, y)
    end = time.perf_counter()
    times_naive.append(end - start)


    start = time.perf_counter()
    res_fft = fft_polymul(x, y)
    end = time.perf_counter()
    times_fft.append(end - start)

    res_scipy = fftconvolve(x, y)

    # Accuracy (Max absolute difference)
    err_naive.append(np.max(np.abs(res_naive - res_scipy)))
    err_fft.append(np.max(np.abs(res_fft - res_scipy)))

# Plotting

# Time Plot
# plt.subplot(1, 2, 1)
plt.figure(figsize=(12, 5))
plt.plot(sizes, times_naive, "o-", label="Naive convolve $O(N^2)$")
plt.plot(sizes, times_fft, "s-", label="FFT convolve $O(N log N)$")
plt.xscale("log", base=2)
plt.yscale("log", base=2)
plt.xlabel("Input Size (N)")
plt.ylabel("Time (seconds)")
plt.title("Execution Time Comparison")
plt.legend()
plt.grid(True, which="both", ls="-", alpha=0.5)

plt.tight_layout()
plt.savefig("polynomial_time_benchmarks.png")

# # Accuracy Plot
# plt.subplot(1, 2, 2)
plt.figure(figsize=(12, 5))
plt.plot(sizes, err_naive, "o-", label="Naive Error")
plt.plot(sizes, err_fft, "s-", label="Ftt Error")
plt.xscale("log", base=2)
plt.yscale("log", base=2)
plt.xlabel("Input Size (N)")
plt.ylabel("Max Absolute Error")
plt.title("Accuracy Relative to SciPy")
plt.legend()
plt.grid(True, which="both", ls="-", alpha=0.5)

plt.tight_layout()
plt.savefig("polynomial_error_benchmarks.png")

# Save results to CSV
df = pd.DataFrame(
    {
        "Size": sizes,
        "Time_Horner": times_naive,
        "Time_FDFT": times_fft,
        "Error_Horner": err_naive,
        "Error_FDFT": err_fft,
    }
)
df.to_csv("dft_benchmarks.csv", index=False)

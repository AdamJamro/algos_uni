import numpy as np
import time
import matplotlib.pyplot as plt
import pandas as pd

from transforms.discrete_fourier_transform import dft_horner, fdft

sizes = [2 ** i for i in range(2, 14)]
times_horner = []
times_fdft = []
times_numpy = []
err_horner = []
err_fdft = []

for N in sizes:
    x = np.random.random(N) + 1j * np.random.random(N)

    # Benchmarking Horner
    start = time.perf_counter()
    res_horner = dft_horner(x)
    end = time.perf_counter()
    times_horner.append(end - start)

    # Benchmarking FDFT
    start = time.perf_counter()
    res_fdft = fdft(x)
    end = time.perf_counter()
    times_fdft.append(end - start)

    # Benchmarking Numpy
    start = time.perf_counter()
    res_numpy = np.fft.fft(x)
    end = time.perf_counter()
    times_numpy.append(end - start)

    # Accuracy (Max absolute difference)
    err_horner.append(np.max(np.abs(res_horner - res_numpy)))
    err_fdft.append(np.max(np.abs(res_fdft - res_numpy)))

# Plotting
plt.figure(figsize=(12, 5))

# Time Plot
plt.subplot(1, 2, 1)
plt.plot(sizes, times_horner, 'o-', label='Horner $O(N^2)$')
plt.plot(sizes, times_fdft, 's-', label='Recursive FDFT $O(N log N)$')
plt.plot(sizes, times_numpy, 'd-', label='NumPy FFT')
plt.xscale('log', base=2)
plt.yscale('log', base=2)
plt.xlabel('Input Size (N)')
plt.ylabel('Time (seconds)')
plt.title('Execution Time Comparison')
plt.legend()
plt.grid(True, which="both", ls="-", alpha=0.5)

# Accuracy Plot
plt.subplot(1, 2, 2)
plt.plot(sizes, err_horner, 'o-', label='Horner Error')
plt.plot(sizes, err_fdft, 's-', label='FDFT Error')
plt.xscale('log', base=2)
plt.yscale('log', base=2)
plt.xlabel('Input Size (N)')
plt.ylabel('Max Absolute Error')
plt.title('Accuracy Relative to NumPy')
plt.legend()
plt.grid(True, which="both", ls="-", alpha=0.5)

plt.tight_layout()
plt.savefig('dft_benchmarks.png')

# Save results to CSV
df = pd.DataFrame({
    'Size': sizes,
    'Time_Horner': times_horner,
    'Time_FDFT': times_fdft,
    'Time_Numpy': times_numpy,
    'Error_Horner': err_horner,
    'Error_FDFT': err_fdft
})
df.to_csv('dft_benchmarks.csv', index=False)
import numpy as np

import pandas as pd
import matplotlib.pyplot as plt

from openmeteo.get_data import fetch_meteo_data

hourly_data = fetch_meteo_data()


#################################################################################
def get_dominant_frequencies(data, d=1):
    N = len(data)
    fft_values = np.fft.fft(data)
    magnitudes = np.abs(fft_values)**2
    frequencies = np.fft.fftfreq(N, d=d)

    positive_mask = frequencies > 0
    freqs = frequencies[positive_mask]
    mags = magnitudes[positive_mask]

    # 5. Find the index of the highest peak
    peak_index = np.argmax(mags)
    dominant_freq = freqs[peak_index]

    return dominant_freq, freqs, mags

def denoise(data, threshold = 5e8):
    """denoises a signal by applying FFT, zeroing out small coefficients, and then applying inverse FFT."""
    fft_values = np.fft.fft(data)
    magnitudes = np.abs(fft_values)**2

    fft_values[magnitudes < threshold] = 0

    denoised_signal = np.fft.ifft(fft_values)
    return denoised_signal.real


def temp_forecast(data, num_future_points=1000, denoise_threshold=5e10):
    """Predicts future values of a signal using its FFT."""
    data = np.asarray(data)
    data_sum = np.sum(data)
    mean = data.mean()
    fft_values = np.fft.rfft(data - mean)
    fft_values = np.abs(fft_values**2)
    #denoise
    fft_values[fft_values < denoise_threshold] = 0.0
    fft_values *= data_sum / np.sum(fft_values)

    N = len(data)
    new_N = N + num_future_points // 2 + 1
    forecast = np.zeros(new_N, dtype=np.float64)
    for i in range(len(fft_values)):
        forecast[int(round((i * (new_N/N))))] = fft_values[i]
    # forecast[:len(fft_values)] = fft_values
    forecast_reified = -np.fft.irfft(forecast, n=new_N) + mean
    x = np.arange(len(forecast_reified), dtype=float)
    m, b = np.polyfit(x[:N], forecast_reified[:N], 1)
    return m * x + forecast_reified

hourly_dataframe = pd.DataFrame(data=hourly_data)
print("\nHourly data\n", hourly_dataframe)
samples_size = len(hourly_dataframe["temperature_2m"])

plt.figure(figsize=(64, 10))
plt.plot(
    hourly_dataframe["date"], hourly_dataframe["temperature_2m"], label="temperature_2m"
)
plt.xlabel("Date")
plt.ylabel("Temperature at 2m (°C)")
plt.title("Temperature at 2m over time")
plt.legend()
plt.grid()
plt.savefig("temperature_2m_hourly.png")


plt.figure(figsize=(110,12))
# freqs = np.fft.fftfreq(len(hourly_dataframe["temperature_2m"])))
freqs = np.arange(0, samples_size, 1)
fft_hourly_temperatures = np.fft.fft(
    hourly_dataframe["temperature_2m"],
)

original_fft_sum = np.sum(np.abs(fft_hourly_temperatures))
fft2 = np.abs(fft_hourly_temperatures**2)

mid_noise_range = 5
mid_slice = slice(len(fft_hourly_temperatures) // 2 - mid_noise_range,len(fft_hourly_temperatures) // 2 + mid_noise_range)
print(np.max(fft_hourly_temperatures[mid_slice]))
print(fft_hourly_temperatures[0])
fft_hourly_temperatures = fft_hourly_temperatures[:len(fft_hourly_temperatures) // 2]
freqs = freqs[:len(freqs) // 2]
cut = 90000
fft_hourly_temperatures = fft_hourly_temperatures[:-cut]
freqs = freqs[:-cut]
fft_hourly_temperatures[:mid_noise_range] = 0
plt.plot(freqs, np.abs(fft_hourly_temperatures), label="FFT of temperature_2m")
from matplotlib import ticker
# plt.xticks(np.arange(0, 10, 0.5))  # tighter steps (every 0.5)
special_values = [0,26,9497, 9573, 18994, 19146,]
special_values = [0,26, samples_size/ 24, samples_size / 12]
plt.xticks(np.union1d(np.arange(0.0, len(freqs), 3000), special_values))
plt.savefig("fft_hourly_temperature_2m.png")
######################################################################################
plt.figure(figsize=(250,12))
trimmed=np.abs(fft_hourly_temperatures)**2
max_val=1e10
trimmed[trimmed > max_val] = max_val
trimmed = trimmed / samples_size
plt.plot(freqs, trimmed, label="abs(FFT^2) of temperature_2m")
plt.xticks(np.union1d(np.arange(0.0, len(freqs), 3000), special_values))
plt.savefig("cleancut_fft_hourly_temperature_2m.png")
######################################################################################

plt.figure(figsize=(110,12))
plt.plot(freqs, np.abs(fft_hourly_temperatures)**2, label="abs(FFT^2) of temperature_2m")
# plt.xticks(np.arange(0.0, 0.2, 0.002))
plt.xticks(np.union1d(np.arange(0.0, len(freqs), 3000), special_values))
plt.savefig("absfft2_hourly_temperature_2m.png")
######################################################################################
cfs = fft2[:]
mask = cfs < 5e4
cfs[mask] = 0
scaling_factor = original_fft_sum / np.sum(cfs)
cfs *= scaling_factor
plt.figure(figsize=(110,12))
np_freqs=np.arange(0, len(cfs), 1)
plt.plot(np_freqs, cfs, label="CFS of temperature_2m")
# plt.xticks(np.arange(0.0, 0.2, 0.002))
plt.xticks(np.union1d(np.arange(3000, len(np_freqs), 9000), special_values))
plt.savefig("cfs_hourly_temperature_2m.png")


#################### PREDICT FUTURE ######################


# def get_next_peak_frequency():
#     indices = np.argsort(np.abs(cfs))
#     # peaks = freqs[indices]
#     recorded_peaks = set()
#     max_length=3
#     for idx in reversed(indices):
#         peak = freqs[idx]
#         if any(np.abs(idx -  recorded) < 5000 for recorded in recorded_peaks):
#             continue
#
#         recorded_peaks.add(idx)
#         yield idx
#
#         if len(recorded_peaks) > max_length:
#             break
#
# print(f"Dominant frequencies (in cycles per hour): {list(get_next_peak_frequency())}")


print(f"MEAN: {hourly_dataframe['temperature_2m'].mean()}")
print(f"Standard Deviation: {hourly_dataframe['temperature_2m'].std()}")
print(f"Min: {hourly_dataframe['temperature_2m'].min()}")
print(f"Max: {hourly_dataframe['temperature_2m'].max()}")
print(f"Median: {hourly_dataframe['temperature_2m'].median()}")
print(f"Abs[dft]^2: {np.sum(np.abs(fft_hourly_temperatures)**2)}")

denoised = denoise(hourly_dataframe["temperature_2m"])
plt.figure(figsize=(64, 10))
plt.plot(hourly_dataframe["date"], denoised, label="Denoised temperature")
plt.xlabel("Date")
plt.ylabel("Temperature at 2m (°C)")
plt.title("Denoised Temperature at 2m over time")
plt.legend()
plt.grid()
plt.savefig("denoised_temperature_2m_hourly.png")

ten_years_in_hours = int(10 * 365.25 * 24)
forecast = temp_forecast(hourly_dataframe["temperature_2m"], num_future_points=ten_years_in_hours, denoise_threshold=5e8)
plt.figure(figsize=(64, 10))
# plt.plot( np.arange(0,len(hourly_dataframe["date"]) + ten_years_in_hours), forecast, label="Denoised temperature")
plt.plot( np.arange(0,len(forecast)), forecast, label="Denoised temperature")
plt.plot(np.arange(0, len(hourly_dataframe["temperature_2m"])), hourly_dataframe["temperature_2m"], label="Original; temperature", alpha=0.7, color="orange")
plt.xlabel("Date")
plt.ylabel("Temperature at 2m (°C)")
plt.title("Denoised Temperature at 2m over time")
plt.legend()
plt.grid()
plt.savefig("forecast_temperature_2m_hourly.png")

# compare denoised with original
plt.figure(figsize=(64, 10))
plt.plot(hourly_dataframe["date"], hourly_dataframe["temperature_2m"], label="Original; temperature")
plt.plot(hourly_dataframe["date"], denoised, label="Denoised temperature", alpha=0.7)
plt.xlabel("Date")
plt.ylabel("Temperature at 2m (°C)")
plt.title("Original vs Denoised Temperature at 2m over time")
plt.legend()
plt.grid()
plt.savefig("original_vs_denoised_temperature_2m_hourly.png")

from openmeteo.get_data import fetch_meteo_data


import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def plot_linear_fit(y, x=None, ax=None, label='data', fit_label=None, show=True):
    """
    Zwraca: (slope, intercept)
    """
    y = np.asarray(y, dtype=float)
    if x is None:
        x = np.arange(len(y), dtype=float)
    else:
        x = np.asarray(x, dtype=float)

    mask = np.isfinite(x) & np.isfinite(y)
    x = x[mask]
    y = y[mask]
    if x.size == 0:
        raise ValueError("no data points to fit")

    m, b = np.polyfit(x, y, 1)
    y_fit = m * x + b

    if ax is None:
        fig, ax = plt.subplots()
    ax.plot(x, y, 'o', label=label)
    ax.plot(x, y_fit, '-', label=(fit_label or f'linear fit: slope={m:.3e}'))
    ax.set_xlabel('index' if x is not None else 'x')
    ax.set_ylabel('y')
    ax.legend()
    if show:
        plt.tight_layout()
        plt.show()

    return m, b


hourly_data = fetch_meteo_data()
temperatures = hourly_data["temperature_2m"]
m, b = plot_linear_fit(temperatures)
def predict_temperature(x):
    return m * x + b

plt.figure()
predict_range = np.arange(len(temperatures),len(temperatures) + 100000)  # Extend the range for prediction
hours_to_years = 1 / (24 * 365.25)
plt.plot(predict_range * hours_to_years + 2000, predict_temperature(predict_range), label='temperature_2m')
plt.tight_layout()
plt.show()
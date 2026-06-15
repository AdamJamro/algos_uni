import numpy as np
import matplotlib.pyplot as plt


def standard_monte_carlo(n):
    """Standardowy algorytm Monte Carlo dla N punktów."""
    x = np.random.rand(n)
    y = np.random.rand(n)
    inside = (x ** 2 + y ** 2) <= 1.0
    return np.mean(inside)


def antithetic_monte_carlo(n):
    """Modyfikacja antytetyczna dla łącznej liczby N punktów."""
    n_half = n // 2
    x1 = np.random.rand(n_half)
    y1 = np.random.rand(n_half)

    x2 = 1.0 - x1
    y2 = 1.0 - y1

    inside1 = (x1 ** 2 + y1 ** 2) <= 1.0
    inside2 = (x2 ** 2 + y2 ** 2) <= 1.0

    return (np.mean(inside1) + np.mean(inside2)) / 2


N_values = [10, 20, 50, 100, 200, 500, 1000, 2000, 5000, 10000, 20000, 50000, 100000, 200000]
num_simulations = 200  # Liczba symulacji dla każdego N, aby uśrednić wyniki
true_value = np.pi / 4

means_std, means_anti = [], []
mses_std, mses_anti = [], []
variance_reductions = []

for n in N_values:
    results_std = [standard_monte_carlo(n) for _ in range(num_simulations)]
    results_anti = [antithetic_monte_carlo(n) for _ in range(num_simulations)]

    # Expected value estimate
    means_std.append(np.mean(results_std))
    means_anti.append(np.mean(results_anti))

    # MSE
    mses_std.append(np.mean((np.array(results_std) - true_value) ** 2))
    mses_anti.append(np.mean((np.array(results_anti) - true_value) ** 2))

    # Variance
    v_std = np.var(results_std)
    v_anti = np.var(results_anti)
    red_pct = np.abs(((v_std - v_anti) / v_std) * 100)
    variance_reductions.append(red_pct)

# --- GENEROWANIE WYKRESÓW ---
plt.figure(figsize=(18, 8))

# Figura 1: Zmiana średniej estymaty
plt.subplot(1, 3, 1)
plt.plot(N_values, means_std, label='Monte Carlo', marker='o', color='tab:blue')
plt.plot(N_values, means_anti, label='Antithetic Monte Carlo', marker='s', color='tab:orange')
plt.axhline(y=true_value, color='red', linestyle='--', label=r'Wartość prawdziwa ($\pi/4$)')
plt.xscale('log')
plt.xlabel('Liczba punktów N (skala log)')
plt.ylabel('Średnia wartość estymatora')
plt.title('1. Zbieżność średniej do wartości prawdziwej')
plt.legend()
# plt.grid(True, which="both", ls="--")

# Figura 2: Zmiana błędu (MSE)
plt.subplot(1, 3, 2)
plt.plot(N_values, mses_std, label='Monte Carlo', marker='o', color='tab:blue')
plt.plot(N_values, mses_anti, label='Antithetic Monte Carlo', marker='s', color='tab:orange')
plt.xscale('log')
plt.yscale('log')  # Skala logarytmiczna dla osi Y, ponieważ błąd szybko maleje
plt.xlabel('Liczba punktów N (skala log)')
plt.ylabel('Błąd średniokwadratowy (MSE)')
plt.title('2. Zmiana błędu (MSE)')
plt.legend()
# plt.grid(True, which="both", ls="--")

# Figura 3: Procentowa redukcja wariancji
plt.subplot(1, 3, 3)
plt.plot(N_values, variance_reductions, marker='^', color='tab:purple', linestyle='-', linewidth=2)
plt.xscale('log')
plt.xlabel('Liczba punktów N (skala log)')
plt.ylabel('Redukcja wariancji (%)')
plt.title('3. Procentowa redukcja wariancji')
# plt.ylim(0, 100)
# plt.grid(True, which="both", ls="--")

plt.tight_layout()
plt.show()
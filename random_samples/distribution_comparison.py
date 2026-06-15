import numpy as np
import matplotlib.pyplot as plt

N = 200000
phi = np.random.uniform(0, 2 * np.pi, N)

r1 = np.random.uniform(0, 1, N)
x1 = r1 * np.cos(phi)
y1 = r1 * np.sin(phi)

r2 = np.random.uniform(0, 1, N)
x2 = np.sqrt(r2) * np.cos(phi)
y2 = np.sqrt(r2) * np.sin(phi)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 9))

circle1 = plt.Circle((0, 0), 1, color='black', fill=False, linestyle='--', zorder=10)
circle2 = plt.Circle((0, 0), 1, color='black', fill=False, linestyle='--', zorder=10)

ax1.scatter(x1, y1, s=1, alpha=0.5, color='blue')
ax1.add_patch(circle1)
ax1.set_xlim(-1.1, 1.1)
ax1.set_ylim(-1.1, 1.1)
ax1.set_aspect('equal')
ax1.set_title('Metoda 1: (r*cos(φ), r*sin(φ))\nZagęszczenie w środku')
ax1.set_xlabel('x')
ax1.set_ylabel('y')

# Wykres dla Metody 2
ax2.scatter(x2, y2, s=1, alpha=0.5, color='green')
ax2.add_patch(circle2)
ax2.set_xlim(-1.1, 1.1)
ax2.set_ylim(-1.1, 1.1)
ax2.set_aspect('equal')
ax2.set_title('Metoda 2: (√r*cos(φ), √r*sin(φ))\nRozkład jednostajny')
ax2.set_xlabel('x')
ax2.set_ylabel('y')

# Wyświetlenie całości
plt.tight_layout()
plt.show()
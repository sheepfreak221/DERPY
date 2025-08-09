import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import linregress

# Daten für 1-Propanol
x = np.array([49.8465, 24.9437, 74.8106])
y = np.array([4.0292, 2.0074, 6.0561])

# Lineare Regression
slope, intercept, r_value, p_value, std_err = linregress(x, y)

# Gerade berechnen
x_fit = np.linspace(min(x), max(x), 100)
y_fit = slope * x_fit + intercept

# Plot
plt.figure(figsize=(6,6))
plt.scatter(x, y, color='green', label='Data points')
plt.plot(x_fit, y_fit, 'k--', label=f'Fit line: y={slope:.4f}x+{intercept:.4f}')
plt.xlabel('Concentration (mM)')
plt.ylabel('Area (µRIU*min)')
plt.title('Calibration curve for 1-propanol quantification')
plt.legend()
plt.grid(True)
plt.tight_layout()

# Bild speichern
plt.savefig('calibration_1propanol.png', dpi=300)
print("Plot saved as 'calibration_1propanol.png'")
# plt.show()  # Nur aktivieren, wenn GUI verfügbar ist

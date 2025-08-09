import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import linregress

# Daten
x = np.array([153.6508, 15.638, 229.6669, 76.3428, 30.7014])
y = np.array([14.9389, 1.4871, 22.348, 7.4038, 2.9553])

# Lineare Regression berechnen
slope, intercept, r_value, p_value, std_err = linregress(x, y)

# Ausgleichsgerade berechnen
x_fit = np.linspace(min(x), max(x), 100)
y_fit = slope * x_fit + intercept

# Label mit Vorzeichen von intercept (+ oder -)
label_eq = f'Fit line: y = {slope:.4f}x {intercept:+.4f}'

# Plot
plt.figure(figsize=(6,6))
plt.scatter(x, y, color='blue', label='Data points')
plt.plot(x_fit, y_fit, 'r--', label=label_eq + f'\n$R^2 = {r_value**2:.4f}$')
plt.xlabel('Concentration (mM)')
plt.ylabel('Area (µRIU*min)')
plt.title('Calibration curve for 2-butanone quantification from UV280 data')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig('calibration_plot.png', dpi=300)
print("Plot saved as calibration_plot.png")

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# Define the Gaussian function
def gauss(x, a, x0, sigma):
    return a * np.exp(-(x - x0)**2 / (2 * sigma**2))

# Generate some sample data
x = np.linspace(0, 10, 1000)
y = gauss(x, 1, 5, 1) + np.random.normal(0, 0.1, len(x))

# Find the peak using argmax of the y values
peak_index = np.argmax(y)
peak_x = x[peak_index]
peak_y = y[peak_index]

# Define the fitting range around the peak
fit_range = (x > peak_x - 1) & (x < peak_x + 1)

# Fit a Gaussian function to the data within the fitting range
popt, pcov = curve_fit(gauss, x[fit_range], y[fit_range], p0=[peak_y, peak_x, 0.5])

# Plot the original data and the fitted Gaussian curve
plt.plot(x, y, 'b-', label='data')
plt.plot(x[fit_range], gauss(x[fit_range], *popt), 'r-', label='fit')
plt.legend()
plt.show()

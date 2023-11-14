import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import linregress

'''
###############################################
## Print a scatter plot with equation and R2 ##
###############################################
'''


# INPUT DATA MUST BE NUMPY ARRAYS
np.random.seed(42)
X = np.random.rand(50) * 10
Y = 2 * X + 1 + np.random.randn(50)

# Perform linear regression
slope, intercept, r_value, p_value, std_err = linregress(X, Y)

# Create scatter plot
plt.figure()
plt.scatter(X, Y)

# Add trend line
line = slope * X + intercept
plt.plot(X, line, color='red')

# Add equation, R2 value, title, and axis labels
equation = f'Y = {slope:.2f}X + {intercept:.2f}'
r_squared = f'R2 = {r_value**2:.2f}'

# Equation and R2 can be placed in (x, y) coordinates just removing transform=plt.gca().transAxes
plt.text(0.05, 0.9, equation, fontsize=10, color='blue', transform=plt.gca().transAxes)
plt.text(0.05, 0.85, r_squared, fontsize=10, color='blue', transform=plt.gca().transAxes)

plt.title('Scatter Plot with Trend Line')
plt.xlabel('X-axis Label')
plt.ylabel('Y-axis Label')

# Save the figure
plt.savefig('scatter_plot_with_trend_line.png', bbox_inches='tight')

# Show the plot
plt.legend()
plt.grid(False)
plt.show()
plt.close()
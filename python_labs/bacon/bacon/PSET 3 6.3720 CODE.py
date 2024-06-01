# -*- coding: utf-8 -*-
"""
Created on Mon Mar  4 10:26:11 2024

@author: gava1
"""

import numpy as np
from scipy.stats import f

# Given data
xi = np.array([0.39, 0.72, 1.00, 1.52, 5.20, 9.58, 19.20, 30.05, 39.48])
yi = np.array([0.24, 0.615, 1.00, 1.88, 11.86, 29.46, 84.01, 164.8, 248.1])

# Step 1: Calculate log(xi) and log(yi)
log_xi = np.log(xi)
log_yi = np.log(yi)

# Step 2: Calculate means
mean_log_x = np.mean(log_xi)
mean_log_y = np.mean(log_yi)
beta1 = np.sum((log_xi - mean_log_x) * (log_yi - mean_log_y)) / np.sum((log_xi - mean_log_x) ** 2)
beta0 = mean_log_y - beta1 * mean_log_x

print(beta1)
print(beta0)
print(mean_log_x)
print(mean_log_y)

n = len(xi)
y_pred = beta0 + beta1 * log_xi
SE_beta1 = np.sqrt(np.sum((log_yi - y_pred)**2) / ((n - 2) * np.sum((log_xi - mean_log_x)**2)))
print(SE_beta1)


# Given values
n = len(xi)
p = 1  # Since there is only one predictor variable (x)

# Calculate R-squared
y_pred = beta0 + beta1 * log_xi
SSR = np.sum((y_pred - np.mean(log_yi))**2)
SST = np.sum((log_yi - np.mean(log_yi))**2)
R_squared = SSR / SST
print(SSR)
print(SST)
print(R_squared)


# Calculate the F-statistic
F_statistic = (R_squared / (1 - R_squared) * ((n - p - 1) / p))
print(f"{F_statistic=}")
# Calculate critical value from the F-distribution
alpha = 0.05  # Significance level
dfn = p
dfd = n - p - 1
critical_value = f.ppf(1 - alpha, dfn, dfd)
print(f'{critical_value=}')
# Check if F-statistic exceeds the critical value
strong_correlation = F_statistic > critical_value

# Display the results
print(f"F-statistic: {F_statistic}")
print(f"Critical value: {critical_value}")
print(f"Strong correlation? {'Yes' if strong_correlation else 'No'}")

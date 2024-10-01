import numpy as np

# Example midpoints and frequencies for 24 buckets
# Data for Kybunpark charging station
midpoints = [0.5,1.5,2.5,3.5,4.5,5.5,6.5,7.5,8.5,9.5,10.5,11.5,12.5,13.5,14.5,15.5,16.5,17.5,18.5,19.5,20.5,21.5,22.5,23.5]
frequencies = [3,3,3,3,3,9,24,42,60,57,75,87,81,69,71,84,90,84,63,45,36,27,15,9]

# Calculate the mean (weighted average)
mean = np.average(midpoints, weights=frequencies)

# Calculate the weighted variance
variance = np.average((midpoints - mean) ** 2, weights=frequencies)

# Standard deviation is the square root of the variance
std_dev = np.sqrt(variance)

print(f"Mean: {mean}")
print(f"Standard Deviation: {std_dev}")
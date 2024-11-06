import pandas as pd
from scipy.fft import fft, ifft
import numpy as np
import matplotlib.pyplot as plt
from scipy import interpolate


data = pd.read_csv("CustomerGeneration\\Live_public_ CS_swiss_eMobility.csv")
data['Date'] = pd.to_datetime(data['Date'])

start_time = data['Date'][0]
"""
end_time = data['Date'][len(data['Date']) - 1]
#time interval
time_interval = (end_time-start_time).total_seconds() / 60
#extend the time interval from 5 days to 30 days
extended_interval = time_interval*6
"""

largest_occupied = max(data['Occupied'])
print(f'test: {largest_occupied}')

""" interpolate the data to get a continous function
interpolate_data = interpolate.interp1d(data['Date'], data['Occupied'], kind='linear', fill_value="extrapolate")
"""
x = (data['Date'] - start_time).dt.total_seconds() / 60
x = np.ceil(x)
y = data['Occupied'] / largest_occupied

print(x)

# Apply FFT
y_freq = fft(y)

# Define the number of frequency components to keep (More frequencies equals more detail)
N = 20
y_freq[N:-N] = 0 

# Apply inverse FFT
y_approx = ifft(y_freq)

plt.subplot(2, 1, 1)
plt.plot(x, y, label='Original', color='blue')
plt.title('Original Data based on Swiss eMobility')

plt.subplot(2, 1, 2)
plt.plot(x, np.real(y_approx), label=f'FFT Approximation', color='black')
plt.title(f'Data Approximation')

plt.tight_layout()
plt.show()

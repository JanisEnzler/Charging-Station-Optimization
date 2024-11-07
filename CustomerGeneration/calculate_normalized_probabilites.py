import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

START_TIME = pd.Timestamp('2024-10-26 00:00:00')
NUMBER_OF_DAYS = 5
SECONDS_PER_DAY = 3600 * 24
MINUTES_PER_DAY = 60 * 24

def normalize(probs):
    prob_factor = 1 / sum(probs)
    return [prob_factor * p for p in probs]

data = pd.read_csv("CustomerGeneration/79pU6.csv")
data['Date'] = pd.to_datetime(data['Date'])

x = (data['Date'] - START_TIME).dt.total_seconds()
y = data['Occupied']
xnew = np.linspace(0, NUMBER_OF_DAYS * SECONDS_PER_DAY, num = NUMBER_OF_DAYS * MINUTES_PER_DAY)
ynew = np.interp(xnew, x, y)


plt.plot(xnew, ynew, label='Interpolated', color='red')
plt.title('Original Data based on Swiss eMobility')
plt.show()

normalized_probs = normalize(ynew)

hist = []

for i in range(0, 100000):
    hist.append(np.random.choice(np.arange(0, len(normalized_probs)), p=normalized_probs))

plt.hist(hist, bins=120)
plt.title('Generated Data')
plt.show()
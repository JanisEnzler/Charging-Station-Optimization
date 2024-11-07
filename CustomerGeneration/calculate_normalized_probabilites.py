import pandas as pd
import numpy as np
#import matplotlib.pyplot as plt


def normalize(probs):
    prob_factor = 1 / sum(probs)
    return [prob_factor * p for p in probs]

# Extend the probabilities, by copying the values and adding them to the end, until the length is equal to the number of days required for the simulation
def extend(probs, number_of_days):
    MINUTES_PER_DAY = 60 * 24
    while len(probs) < (number_of_days * MINUTES_PER_DAY):
        probs = np.append(probs, probs)
    return probs[0:number_of_days * MINUTES_PER_DAY]


def get_normalized_probs(file_path, start_timestamp, number_of_days_in_simulation, number_of_days_in_dataset):
    SECONDS_PER_DAY = 3600 * 24
    MINUTES_PER_DAY = 60 * 24

    #start_timestamp = pd.Timestamp(config.get('availability dataset', 'STARTING_TIMESTAMP'))
    #number_of_days_in_simulation = (config.getint('availability dataset', 'NUMBER_OF_DAYS_IN_DATASET'))

    data = pd.read_csv(file_path)
    data['Date'] = pd.to_datetime(data['Date'])

    x = (data['Date'] - start_timestamp).dt.total_seconds()
    y = data['Occupied']
    xnew = np.linspace(0, number_of_days_in_dataset * SECONDS_PER_DAY, num = number_of_days_in_dataset * MINUTES_PER_DAY)
    ynew = np.interp(xnew, x, y)

    extended_y = extend(ynew, number_of_days_in_simulation)

    return normalize(extended_y)

"""
hist = []

for i in range(0, 3000):
    hist.append(np.random.choice(np.arange(0, len(normalized_probs)), p=normalized_probs))

plt.hist(hist, bins=(6*NUMBER_OF_DAYS))
plt.title('Generated Data')
plt.show()
"""
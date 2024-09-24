# Uses the customers.csv and simulates a day of charging for a single charging station.
# New cars are just arriving, and if the charging station is available, they charge to their target battery level:
# If someone else is charging they wait in queue, until the station is available, or they have no more waiting-time left

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import math

# Charging power of station in watts
charging_power = 200000

# First the customers are sorted by arrival time
df = pd.read_csv('customers.csv')

df_sorted = df.sort_values(by='arrival_time_in_minutes', ascending=True)
df_sorted['arrival_time_in_minutes'].plot(kind='hist', bins=20, label='arrival_time_in_minutes')
plt.show()
# This will be used to plot when the station was used
availability = [0] * (24 * 60)
next_available_time = 0
unserved_customers = []


def calculate_duration(current_battery_level, target_battery_level, charging_speed):
    duration_in_hours = (target_battery_level - current_battery_level) / charging_speed
    # Duration is in hours, because capacity is in watt-hours, but we want rounded minutes
    return math.ceil(duration_in_hours * 60)


for row in df_sorted.iterrows():
    charging_dur = calculate_duration(row[1]['current_battery_level'], row[1]['target_battery_level'], charging_power)
    arrival_time = row[1]['arrival_time_in_minutes']
    waiting_time = row[1]['waiting_time_in_minutes']
    # If the station is empty at arrival the customer takes the station and charges his car
    if arrival_time >= next_available_time:
        next_available_time = arrival_time + charging_dur
        availability[arrival_time:next_available_time] = [1] * charging_dur
    # If the station is still in use, the customer waits for as long as he can, and starts charging as soon as the
    # other car leaves
    elif arrival_time + waiting_time >= next_available_time:
        availability[next_available_time:next_available_time + charging_dur] = [1] * charging_dur
        next_available_time += charging_dur
    # If the station is still in use once the customers waiting tolerance is up, he leaves
    else:
        unserved_customers.append(arrival_time)


plt.plot(availability)
plt.show()
plt.hist(unserved_customers, bins=10)
plt.show()

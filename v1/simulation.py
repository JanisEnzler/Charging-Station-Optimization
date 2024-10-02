# Uses the customers.csv and simulates a day of charging for a single charging station.
# New cars are just arriving, and if the charging station is available, they charge to their target battery level:
# If someone else is charging they wait in queue, until the station is available, or they have no more waiting-time left

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import math
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

# Charging power of station in watts
CHARGING_POWER = config.getint('charging_station', 'CHARGING_POWER_IN_WATTS')
NUMBER_OF_CHARGING_STATIONS = config.getint('charging_station', 'NUMBER_OF_CHARGING_STATIONS')

# First the customers are sorted by arrival time
df = pd.read_csv('customers.csv')

df_sorted = df.sort_values(by='arrival_time_in_minutes', ascending=True)
df_sorted['arrival_time_in_minutes'].plot(kind='hist', bins=24, label='arrival_time_in_minutes', range=(0,24*60))
plt.show()
# This will be used to plot when the station was used
schedule = [[0] * (24*60) for _ in range(NUMBER_OF_CHARGING_STATIONS)]
next_available_time = 0
unserved_customers = []


def calculate_duration(current_battery_level, target_battery_level, charging_speed):
    duration_in_hours = (target_battery_level - current_battery_level) / charging_speed
    # Duration is in hours, because capacity is in watt-hours, but we want rounded minutes
    return math.ceil(duration_in_hours * 60)


# Checks if a station is available within the charging duration, and schedules it if available
def schedule_charging(start_time, duration, waiting_time):
    for station in schedule:
        # Check if a particular station is available, within the waiting time tolerance
        for i in range(start_time, start_time + waiting_time+1):
            if(i >= len(station)):
                # Only one day is simulated, so if the waiting time crosses midnight we break the for loop
                break
            if station[i] == 0:
                # Because the customers are sorted by arrival, we don't need to check for availability
                for j in range(i, i+duration):
                    if(j >= len(station)):
                        # If the customer wants to charge over midnight, we don't care, because we only simulate one day
                        return True
                    station[j] = 1
                return True
    print(start_time, duration, waiting_time)
    return False

schedule_charging(1,1,1)

for row in df_sorted.iterrows():
    charging_dur = calculate_duration(row[1]['current_battery_level'], row[1]['target_battery_level'], CHARGING_POWER)
    arrival_time = row[1]['arrival_time_in_minutes']
    waiting_time = row[1]['waiting_time_in_minutes']
    # If the station is empty at arrival the customer takes the station and charges his car
    if not schedule_charging(arrival_time, charging_dur, waiting_time):
        unserved_customers.append(arrival_time)

def get_utilization_stats():
    schedule_matrix = np.array(schedule)
    return np.sum(schedule_matrix, axis=0)


plt.plot(get_utilization_stats())
plt.show()
plt.hist(unserved_customers, bins=24, range=(0,24*60))
plt.show()

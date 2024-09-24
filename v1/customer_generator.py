import pandas as pd
import numpy as np
from datetime import timedelta

num_of_customers = 200

# Creating a normal distribution of Timeslots for Customers, centered at 13:00
mean_time_in_minutes = 13 * 60
std_dev_minutes = 60 * 5
arrival_times_in_minutes = np.random.normal(loc=mean_time_in_minutes, scale=std_dev_minutes, size=num_of_customers).astype(int)

# Ensure all times fall within the 24-hour range (0 to 1439 minutes)
arrival_times_in_minutes = np.mod(arrival_times_in_minutes, 24 * 60)

# generating max waiting times for customers
waiting_times_in_minutes = np.random.randint(low=0, high=20, size=num_of_customers)

# Battery capacity (for now 50kw/h or 50000w/h for all cars)
battery_capacity = 50000

# We assume that people wanting to charge have a battery level between 10% and 60%
current_battery_level = np.random.randint(low=5000, high=30000, size=num_of_customers)



# Create a DataFrame with the times
df = pd.DataFrame()
df['arrival_time_in_minutes'] = arrival_times_in_minutes
df['waiting_time_in_minutes'] = waiting_times_in_minutes
df['battery_capacity'] = battery_capacity
df['current_battery_level'] = current_battery_level

# We assume that people want to charge their battery somewhere between adding 10% to fully charging it
df['target_battery_level'] = np.random.randint(low=df['current_battery_level']+5000, high=df['battery_capacity'])

df.to_csv('customers.csv', index=False)
print(df.head())

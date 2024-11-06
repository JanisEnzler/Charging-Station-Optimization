import pandas as pd
import numpy as np
from datetime import timedelta
import configparser
from scipy import interpolate

config = configparser.ConfigParser()
config.read('config.ini')

# We have three customer profiles, 
# - PRIORITY_CHARGERS are customers how are willing to pay extra if the can charge their car faster, and dont have to wait in queue as long as others:
# - FLEXIBLE_CHARGERS would be willing to release a spot and finish charging at another time of day, if the would get better prices.
# - NORMAL_CHARGERS who just arrive, and charge if possible and leave otherwise




NUMBER_OF_CUSTOMERS_PER_DAY = config.getint('customer', 'NUMBER_OF_CUSTOMERS_PER_DAY')
MEAN_ARRIVAL_TIME = config.getint('customer', 'MEAN_ARRIVAL_TIME_IN_MINUTES')
STD_DEV_ARRIVAL_TIME = config.getint('customer', 'STD_DEV_ARRIVAL_TIME_IN_MINUTES')
MAX_WAITING_TIME = config.getint('customer', 'MAX_WAITING_TIME_IN_MINUTES')
NUMBER_OF_DAYS = config.getint('simulation', 'NUMBER_OF_DAYS')


#relationship between OCV and SOC
ocv_df = {
    "U_OCV": [4.1617, 4.0913, 4.0749, 4.0606, 4.0153, 3.9592, 3.9164, 3.8687, 
              3.8163, 3.7735, 3.7317, 3.6892, 3.6396, 3.5677, 3.5208, 3.4712, 
              3.386, 3.288, 3.2037, 3.0747],
    "SOC": [1.0, 0.9503, 0.9007, 0.851, 0.8013, 0.7517, 0.702, 0.6524, 
            0.6027, 0.553, 0.5034, 0.4537, 0.404, 0.3543, 0.3046, 0.255, 
            0.2053, 0.1556, 0.1059, 0.0563]
}


final_df = pd.DataFrame()


for day in range(NUMBER_OF_DAYS):
    print(f"Generating customers for day {day+1}/{NUMBER_OF_DAYS}")
    # Creating a normal distribution of Timeslots for Customers, centered at 13:00
    arrival_times_in_minutes = np.random.normal(loc=MEAN_ARRIVAL_TIME, scale=STD_DEV_ARRIVAL_TIME, size=NUMBER_OF_CUSTOMERS_PER_DAY).astype(int)

    # Ensure all times fall within the 24-hour range (0 to 1439 minutes)
    arrival_times_in_minutes = np.mod(arrival_times_in_minutes, 24 * 60)

    arrival_times_in_minutes = arrival_times_in_minutes + day * 24 * 60

    # generating max waiting times for customers
    waiting_times_in_minutes = np.random.randint(low=0, high=MAX_WAITING_TIME, size=NUMBER_OF_CUSTOMERS_PER_DAY)

    # Battery capacity (for now 50kw/h or 50000w/h for all cars)
    battery_capacity = 50000

    # We assume that people wanting to charge have a battery level between 10% and 40%
    current_battery_level = np.random.randint(low=5000, high=20000, size=NUMBER_OF_CUSTOMERS_PER_DAY)

    # Create a DataFrame with the times
    customer_df = pd.DataFrame()
    customer_df['arrival_time_in_minutes'] = arrival_times_in_minutes
    customer_df['waiting_time_in_minutes'] = waiting_times_in_minutes
    customer_df['battery_capacity'] = battery_capacity
    customer_df['current_battery_level'] = current_battery_level

    # We assume that people want to charge their battery somewhere between adding 30% to fully charging it
    customer_df['target_battery_level'] = np.random.randint(low=customer_df['current_battery_level']+15000, high=customer_df['battery_capacity'])

    # Each customer has an amount of Money he would be willing to pay extra for a kilowatt hour (between 0.05 and 0.2 CHF), if the could skip the queue 
    customer_df['willingness_to_pay_extra_per_kwh'] = np.random.randint(low=5, high=21, size=NUMBER_OF_CUSTOMERS_PER_DAY)/100

    # Each customer has an discount per kilowatt hour threshold with which he would be willing to release his spot and charge at another time (between 0.05 and 0.15 CHF)
    customer_df['minimum_discount_per_kwh'] = np.random.randint(low=5, high=16, size=NUMBER_OF_CUSTOMERS_PER_DAY)/100

    customer_df['soc'] = (customer_df['current_battery_level']/customer_df['battery_capacity'])


    interpolation = interpolate.interp1d(ocv_df["SOC"], ocv_df["U_OCV"], kind='linear', fill_value="extrapolate")
    current_ocv = interpolation(customer_df["soc"])
    
    customer_df["ocv"] = np.round(current_ocv,4)

    final_df = pd.concat([final_df, customer_df], ignore_index=True)


final_df.to_csv('customers.csv', index=False)






import pandas as pd
import numpy as np
from datetime import timedelta
import configparser
from scipy import interpolate
from calculate_normalized_probabilites import get_normalized_probs
from customer_profile import CustomerProfile
import matplotlib.pyplot as plt
import json

config = configparser.ConfigParser()
config.read('config.ini')

data = open('CustomerGeneration/customer_profiles.json')
data = json.load(data)

profiles = []

for profile in data["cutomer_profiles"]:
    profiles.append(CustomerProfile(data, profile))


# We have three customer profiles, 
# - PRIORITY_CHARGERS are customers how are willing to pay extra if the can charge their car faster, and dont have to wait in queue as long as others:
# - FLEXIBLE_CHARGERS would be willing to release a spot and finish charging at another time of day, if the would get better prices.
# - NORMAL_CHARGERS who just arrive, and charge if possible and leave otherwise




NUMBER_OF_CUSTOMERS = config.getint('customer', 'NUMBER_OF_CUSTOMERS')
MEAN_ARRIVAL_TIME = config.getint('customer', 'MEAN_ARRIVAL_TIME_IN_MINUTES')
STD_DEV_ARRIVAL_TIME = config.getint('customer', 'STD_DEV_ARRIVAL_TIME_IN_MINUTES')
MAX_WAITING_TIME = config.getint('customer', 'MAX_WAITING_TIME_IN_MINUTES')
NUMBER_OF_DAYS = config.getint('simulation', 'NUMBER_OF_DAYS')
AVAILABILITY_DATASET_PATH = config.get('availability dataset', 'FILE_PATH')
NUMBER_OF_DAYS_IN_DATASET = config.getint('availability dataset', 'NUMBER_OF_DAYS_IN_DATASET')
DATASET_STARTING_TIMESTAMP = config.get('availability dataset', 'STARTING_TIMESTAMP')

probs = get_normalized_probs(AVAILABILITY_DATASET_PATH, DATASET_STARTING_TIMESTAMP, NUMBER_OF_DAYS, NUMBER_OF_DAYS_IN_DATASET)


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

for profile in profiles:
    # np.random.choice(np.arange(0, len(normalized_probs)), p=normalized_probs)
    arrival_times_in_minutes = np.random.choice(np.arange(0, len(probs)), p=probs,size=profile.number_of_customers)
    # generating max waiting times for customers
    waiting_times_in_minutes = profile.s()
    # Battery capacity (for now 50kw/h or 50000w/h for all cars)
    battery_capacity = 50000
    # We assume that people wanting to charge have a battery level between 10% and 40%
    current_battery_level = np.random.randint(low=5000, high=20000, size=profile.number_of_customers)
    # Each customer has an amount of Money he would be willing to pay extra for a kilowatt hour (between 0.05 and 0.2 CHF), if the could skip the queue 
    willingness_to_pay_extra_per_kwh = profile.get_willingness_to_pay()
    # Each customer has an discount per kilowatt hour threshold with which he would be willing to release his spot and charge at another time (between 0.05 and 0.15 CHF)
    willingness_to_release = profile.get_willingness_to_release()

    # Create a DataFrame with the times
    df = pd.DataFrame()
    df['arrival_time_in_minutes'] = arrival_times_in_minutes
    df['waiting_time_in_minutes'] = waiting_times_in_minutes
    df['battery_capacity'] = battery_capacity
    df['current_battery_level'] = current_battery_level
    df['willingness_to_pay_extra_per_kwh'] = willingness_to_pay_extra_per_kwh
    df['willingness_to_release'] = willingness_to_release

    # We assume that people want to charge their battery somewhere between adding 30% to fully charging it
    df['target_battery_level'] = np.random.randint(low=df['current_battery_level']+15000, high=df['battery_capacity'])


    df['soc'] = (df['current_battery_level']/df['battery_capacity'])

    interpolation = interpolate.interp1d(ocv_df["SOC"], ocv_df["U_OCV"], kind='linear', fill_value="extrapolate")
    current_ocv = interpolation(df["soc"])
        
    df["ocv"] = np.round(current_ocv,4)

    final_df = final_df.append(df)

        


final_df.to_csv('customers.csv', index=False)






import json
import numpy as np
import pandas as pd

class CustomerProfile:
    
    def __init__(self, data, profile):

        self.profile_name = profile
        self.starting_soc_minimum = data["cutomer_profiles"][profile]['starting_soc_minimum']
        self.starting_soc_maximum = data["cutomer_profiles"][profile]['starting_soc_maximum']

        if self.starting_soc_minimum >= self.starting_soc_maximum:
            raise ValueError("Starting SOC minimum is greater than or equal to the maximum")

        self.minimum_soc_charged = data["cutomer_profiles"][profile]['minimum_soc_charged']

        if self.minimum_soc_charged + self.starting_soc_maximum > 1:
            raise ValueError("Minimum SOC charged and starting SOC maximum are greater than 1")

        self.number_of_customers = data["cutomer_profiles"][profile]['number_of_customers']
        self.min_willingness_to_pay = data["cutomer_profiles"][profile]['min_willingness_to_pay']
        self.max_willingness_to_pay = data["cutomer_profiles"][profile]['max_willingness_to_pay']

        if self.min_willingness_to_pay >= self.max_willingness_to_pay:
            raise ValueError("Minimum willingness to pay is greater than maximum")

        self.min_willingness_to_wait = data["cutomer_profiles"][profile]['min_willingness_to_wait']
        self.max_willingness_to_wait = data["cutomer_profiles"][profile]['max_willingness_to_wait']

        if self.min_willingness_to_wait >= self.max_willingness_to_wait:
            raise ValueError("Minimum willingness to wait is greater than maximum")

        self.min_willingness_to_release = data["cutomer_profiles"][profile]['min_willingness_to_release']
        self.max_willingness_to_release = data["cutomer_profiles"][profile]['max_willingness_to_release']

        if self.min_willingness_to_release >= self.max_willingness_to_release:
            raise ValueError("Minimum willingness to release is greater than maximum")
        
    
    def get_willingness_to_pay(self):
        willingness_to_pay = np.random.uniform(self.min_willingness_to_pay, self.max_willingness_to_pay, self.number_of_customers)
        return np.round(willingness_to_pay, 2)


    def get_willingness_to_wait(self):
        return np.random.randint(low=self.min_willingness_to_wait, high=self.max_willingness_to_wait, size=self.number_of_customers)


    def get_willingness_to_release(self):
        willingness_to_release = np.random.uniform(self.min_willingness_to_release, self.max_willingness_to_release, self.number_of_customers)
        return np.round(willingness_to_release, 2)

    def get_min_starting_soc(self):
        return self.starting_soc_minimum
    
    def get_max_starting_soc(self):
        return self.starting_soc_maximum
    
    def get_min_soc_charged(self):
        return self.minimum_soc_charged

""""0
    profileName = Name of profile
    willingness_to_pay = willingness to pay CHF for kW
        - low = 0.00 - 0.05
        - medium = 0.05 - 0.1
        - high = 0.1 - 0.2
    willingness_to_wait = willingness to wait in minutes
        - low = 0 - 5
        - medium = 5 - 10
        - high = 10 - 20
    willingness_to_release = willingness to release for a specific amount of payment per kWh remaining
        - low = 0.15 - 0.25
        - medium = 0.05 - 0.15
        - high = 0 - 0.05
    preferrs_low_rate = boolean value (prefers to charge only on low rats, for example weekends and outside of peak times)
        - True 
        - False
    willingness_to_subscribe = probability that the customer will subscribe
        - low = 0
        - medium = 0.05 - 0.2
        - high = 0.2 - 1
     '''


def __init__(self, profileName, willingness_to_pay, willingness_to_wait, willingness_to_release, preferres_low_rates, willingness_to_subscribe):
        self.profileName = profileName
        self.willingness_to_pay = willingness_to_pay
        self.willingness_to_wait = willingness_to_wait
        self.willingness_to_release = willingness_to_release
        self.preferres_low_rates = preferres_low_rates
        self.willingness_to_subscribe = willingness_to_subscribe

    def createCustomer():
        pass




We have three customer profiles: Priority Chargers, Flexible chargers and normal charges:

- PRIORITY_CHARGERS are customers how are willing to pay extra if the can charge their car faster, and dont have to wait in queue as long as others.
    - willingness_to_pay is high 
    - willingness_to_wait is low
    - willingness_to_release is low
    - preferres_low_rates is False
    - willingness_to_subscribe between medium and high

- FLEXIBLE_CHARGERS would be willing to release a spot and finish charging at another time of day, if the would get better prices. Decisions often based on opposite customer.
    - willingness_to_pay is medium
    - willingness_to_wait is medium
    - willingness_to_release is high
    - preferres_low_rates is True
    - willingness_to_subscribe is between medium and high

- NORMAL_CHARGERS who just arrive, and charge if possible and leave otherwise
    - willingness_to_pay is low
    - willingness_to_wait is high
    - willingness_to_release is medium and low
    - preferres_low_rates is True
    - willingness_to_subscribe between medium and low

    
    """

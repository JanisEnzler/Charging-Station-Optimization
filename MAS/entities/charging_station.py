import math
import numpy as np

class ChargingStation:
    def __init__(self, charging_spots, station_amperage, station_voltage, cc_cv_threshold, charging_beta_value, price_per_kwh):
        self.charging_spots = charging_spots
        self.occupied_spots = []
        self.station_amperage = station_amperage
        self.station_voltage = station_voltage
        self.cc_cv_threshold = cc_cv_threshold
        self.price_per_kwh = price_per_kwh
        self.beta = charging_beta_value
        
    def occupy_spot(self, customer):
        if len(self.occupied_spots) < self.charging_spots and customer not in self.occupied_spots:
            self.occupied_spots.append(customer)
            return True
        else:
            return False
        
    def release_spot(self, customer):
        if customer in self.occupied_spots:
            self.occupied_spots.remove(customer)
            return True
        else:
            return False
        
    def swap_spot(self, customer1, customer2):
        if customer1 in self.occupied_spots and customer2 not in self.occupied_spots:
            self.occupied_spots.remove(customer1)
            self.occupied_spots.append(customer2)
            return True
        else:
            return False
        

    def charge(self, customer, time_elapsed_in_hours):

        charging_delta = 0

        if customer not in self.occupied_spots:
            print("ERROR: Customer charging without occuoing a spot in the charging station")
            return 0
        else:
            soc = customer.getSoc()
            if (soc < self.cc_cv_threshold):
                # CC charging
                charging_delta = self.station_amperage * self.station_voltage * time_elapsed_in_hours
                customer.current_battery_level += charging_delta
            else:
                # CV charging
                I = self.station_amperage * np.exp(-self.beta * (soc - self.cc_cv_threshold)) 
                charging_delta = I * self.station_voltage * time_elapsed_in_hours
                if customer.current_battery_level + charging_delta > customer.battery_capacity:
                        charging_delta = customer.battery_capacity - customer.current_battery_level
                        customer.fully_charged = True
                customer.current_battery_level += charging_delta
                if I < 0.01:
                        customer.fully_charged = True
            return charging_delta
            

            
""" time_elapsed +=1
        I = self.station_model.power/self.ocv

        MIN_CURRENT = 0.01

        if self.ocv < 1:
            while self.ocv < 4.2:
                 self.ocv += 0.05

                 I = I_0 * math.exp(-time_elapsed/tau)
time_elapsed +=1 """



#linear  -> I -= 0.01
#exponential decay  -> I *= 0.99
# mathmatical decay using time constant -> I(t) = I_0 * e ^ -t/tau

"""
            I = self.model.station_power/self.ocv
            if self.soc < 1:
                while self.ocv < 4.2:
                    #self.print(f'Customer {self.unique_id} is CC charging')
                    self.ocv += 0.05 #temp value
                    #self.print(self.ocv)
                    if self.ocv > 4.2:
                        self.ocv == 4.2 #keep it at 4.2V
                    #self.print(f'Customer {self.unique_id} is not at {self.ocv} OCV')

                while self.ocv >= 4.2 and I > 0.01: #cv charging
                    #self.print(f'Customer {self.unique_id} is CV charging')
                    #keep voltage at 4.2V and decrease current until threshold is reached
                    I = I*0.99
                    #self.print(f'Current {I}')
                #self.print(f'Customer {self.unique_id} is fully charged')
            else:
                pass
                # self.print("no Charging needed")
            """
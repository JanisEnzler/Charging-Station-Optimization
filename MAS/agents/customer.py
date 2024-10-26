import mesa
import numpy as np
import pandas as pd
from enum import Enum

class CustomerState(Enum):
    NOT_ARRIVED = 1
    WAITING = 2
    CHARGING = 3
    LEFT_STATION = 4
    
      
class CustomerAgent(mesa.Agent):
# Customer is equivalent to the agent in the MAS

    def __init__(self, unique_id, model, arrival_time_in_minutes, waiting_time_in_minutes, battery_capacity, current_battery_level, target_battery_level,willingness_to_pay_extra_per_kwh, minimum_discount_per_kwh, soc, ocv):
        super().__init__(unique_id, model)
        self.state = CustomerState.NOT_ARRIVED
        self.arrival_time_in_minutes = arrival_time_in_minutes
        self.waiting_time_in_minutes = waiting_time_in_minutes
        self.battery_capacity = battery_capacity
        self.current_battery_level = current_battery_level
        self.target_battery_level = target_battery_level
        self.willingness_to_pay_extra_per_kwh = willingness_to_pay_extra_per_kwh
        self.minimum_discount_per_kwh = minimum_discount_per_kwh
        self.soc = soc
        self.ocv = ocv


    def step(self):
        match self.state:
            case CustomerState.NOT_ARRIVED:
                if self.arrival_time_in_minutes == self.model.schedule.time:
                    self.arrival()
            case CustomerState.WAITING:
                self.wait()
            case CustomerState.CHARGING:
                self.charge()
            case CustomerState.LEFT_STATION:
                pass


    def arrival(self):
        if(self.model.charging_station.occupy_spot(self.unique_id)):
            self.state = CustomerState.CHARGING
            print(f'occupied by: {self.unique_id}')
        else:
            self.state = CustomerState.WAITING
            print(f'{self.unique_id} is waiting!')


    def negotiate_skip_queue(self):
        self.state = CustomerState.WAITING

    
    def negotiate_release_spot(self):
        pass


    def charge(self):
        # TODO Simulate charging here
        
        #Temp
        self.current_battery_level += self.model.station_power/60
        if (self.current_battery_level > self.battery_capacity):
            current_battery_level = self.battery_capacity
        #Temp
        
        if(self.current_battery_level >= self.target_battery_level):
            if (self.model.charging_station.release_spot(self.unique_id)):
                self.state = CustomerState.LEFT_STATION
                print(f'Customer {self.unique_id} left after charging his car for {self.model.schedule.time - self.arrival_time_in_minutes} minutes.')
            else:
                # TODO Replace with acutall error
                print('ERROR: Customer was charging without occuping station')

    
    def wait(self):
        if(self.model.charging_station.occupy_spot(self.unique_id)):
            self.state = CustomerState.CHARGING
            print(f'occupied by: {self.unique_id}')
        elif(self.model.schedule.time - self.arrival_time_in_minutes >= self.waiting_time_in_minutes):
            self.state = CustomerState.LEFT_STATION
            print(f'Customer {self.unique_id} left after waiting for {self.model.schedule.time - self.arrival_time_in_minutes} minutes.')


    def evaluateSpotReleaseForBonus(self):
        pass

    def evaluateSkipQueueForExtraPayment(self):
        # Calculate how much the extra payment would affect the cost per kwh for the amount the customer wants to charge
        self.extra_per_kwh = (self.model.provider.skip_queue_price /(self.target_battery_level - self.current_battery_level))
        if (self.extra_per_kwh <= self.willingness_to_pay_extra_per_kwh):
            return True
        else:
            return False
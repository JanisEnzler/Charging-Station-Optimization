import mesa
import numpy as np
import pandas as pd
from enum import Enum

class CustomerState(Enum):
    NOT_ARRIVED = 1
    WAITING = 2
    CHARGING = 3
    
      
class CustomerAgent(mesa.Agent):
#customer is equivalent to the agent in the MAS

    def __init__(self, unique_id, model, arrival_time_in_minutes, waiting_time_in_minutes, battery_capacity, current_battery_level, target_battery_level, soc):
        super().__init__(unique_id, model)
        self.state = CustomerState.NOT_ARRIVED
        self.arrival_time_in_minutes = arrival_time_in_minutes
        self.waiting_time_in_minutes = waiting_time_in_minutes
        self.battery_capacity = battery_capacity
        self.current_battery_level = current_battery_level
        self.target_battery_level = target_battery_level
        self.soc = soc
        #self.ocv = ocv


    def step(self):
        match self.state:
            case CustomerState.NOT_ARRIVED:
                if self.arrival_time_in_minutes == self.model.schedule.time:
                #print("Customer with ID: ", self.unique_id, " is starting to charge at : ", self.arrival_time_in_minutes)
                    if(self.model.charging_station.occupy_spot(self.unique_id)):
                        self.state = CustomerState.CHARGING
                        print(f'occupied by: {self.unique_id}')
                    else:
                        self.state = CustomerState.WAITING
                        print(f'{self.unique_id} is waiting!')
            case CustomerState.WAITING:
                pass
            case CustomerState.CHARGING:
                pass

    def negotiate(self):
        # Negotiation with the charging station
        pass

    def charge(self):
        # Charging the car
        pass

    def wait(self):
        # Waiting for the station to be available
        # if the negotiation failed, the customer can choose between waiting (queue) or he might leave, if the waiting time exceeds the MAX_WAITING_TIME_IN_MINUTES
        pass

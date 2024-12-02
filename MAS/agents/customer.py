import mesa
import numpy as np
import pandas as pd
from enum import Enum
from MAS.environment.time_converter import convert_time_to_string

class CustomerState(Enum):
    NOT_ARRIVED = 1
    WAITING = 2
    CHARGING = 3
    LEFT_STATION = 4

class CustomerActions(Enum):
    ARRIVED = 1
    LEFT_AFTER_CHARGING = 2
    LEFT_BECAUSE_PRICE_IS_TO_HIGH = 3
    LEFT_AFTER_WAITING = 4
    SKIPED_QUEUE = 5
    RELEASED_SPOT = 6
    REFUSED_TO_RELEASE = 7
    BIDDED_FOR_SPOT = 8
    PROVIDER_EARNED = 9
    CUSTOMER_EARNED = 10
    STARTING_TO_CHARGE = 11
    STARTED_TO_WAIT_IN_QUEUE = 12
    PROVIDER_EARNED_FROM_AUCTION = 13

      
class CustomerAgent(mesa.Agent):
# Customer is equivalent to the agent in the MAS

    def __init__(self, unique_id, model, arrival_time_in_minutes, waiting_time_in_minutes, battery_capacity, current_battery_level, target_battery_level,willingness_to_pay_extra_per_kwh, willingness_to_pay_release, soc, ocv):
        super().__init__(unique_id, model)
        self.state = CustomerState.NOT_ARRIVED
        self.arrival_time_in_minutes = arrival_time_in_minutes
        self.waiting_time_in_minutes = waiting_time_in_minutes
        self.battery_capacity = battery_capacity
        self.current_battery_level = current_battery_level
        self.target_battery_level = target_battery_level
        self.willingness_to_pay_extra_per_kwh = willingness_to_pay_extra_per_kwh
        self.willingness_to_pay_release = willingness_to_pay_release
        self.soc = soc
        self.ocv = ocv
        self.waiting_customers = {self: self.willingness_to_pay_extra_per_kwh}


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


    # Returns True if charging price is below personal threshold
    def check_price_threshold(self):
        return ((self.model.provider.price_per_kwh + self.willingness_to_pay_extra_per_kwh) >= self.model.provider.dynamic_pricing_rate(self))


    def arrival(self):
        self.save_action_to_csv(CustomerActions.ARRIVED, self.getSoc())
        if not self.check_price_threshold():
            self.model.number_of_customers_that_could_not_charge += 1
            self.save_action_to_csv(CustomerActions.LEFT_BECAUSE_PRICE_IS_TO_HIGH,self.getSoc())
            print(f'{convert_time_to_string(self.model.schedule.time)}: Customer {self.unique_id} left because the charging rate was too high. SOC: {self.getSoc()}') 
            self.state = CustomerState.LEFT_STATION
        elif(self.model.charging_station.occupy_spot(self)):
            self.state = CustomerState.CHARGING
            self.save_action_to_csv(CustomerActions.STARTING_TO_CHARGE, self.getSoc())
            self.model.number_of_customers += 1
        elif(self.evaluateSkipQueueForExtraPayment()):
            if(self.model.provider.request_skip_queue(self)):
                self.state = CustomerState.CHARGING
                self.model.number_of_customers += 1
                print(f'{convert_time_to_string(self.model.schedule.time)}: Customer {self.unique_id} skipped the queue, and is now charging.')
                self.save_action_to_csv(CustomerActions.SKIPED_QUEUE, self.getSoc())
        elif(self.model.provider.attend_auction()):
            winner = self.model.provider.won_auction(self.waiting_customers)
            if winner == self:
                self.state = CustomerState.CHARGING
                self.model.number_of_customers += 1
                print(f'{convert_time_to_string(self.model.schedule.time)}: Customer {self.unique_id} won the auction, and is now charging.')
                self.save_action_to_csv(CustomerActions.BIDDED_FOR_SPOT, self.getSoc())
            else:
                self.state = CustomerState.WAITING
                print(f'{convert_time_to_string(self.model.schedule.time)}: Customer {self.unique_id} '
                      f'lost the auction and continues waiting.')
        else:
            self.state = CustomerState.WAITING
            print(f'{convert_time_to_string(self.model.schedule.time)}: Customer {self.unique_id} is waiting for a spot to charge.')
            self.save_action_to_csv(CustomerActions.STARTED_TO_WAIT_IN_QUEUE, self.getSoc())
    def charge(self):
        # Check if electricity price is within personal threshold, otherwise leave the station
        if self.check_price_threshold(): #over the remaining time and charge the car and how much the customer has to pays
            if(self.getSoc() >= 0.8):
                print(f'{convert_time_to_string(self.model.schedule.time)}: Customer {self.unique_id} is charging with a SOC of {self.getSoc()}')
                #self.save_action_to_csv(CustomerActions.STARTING_TO_CHARGE, self.getSoc())
            if (self not in self.model.charging_station.occupied_spots):
                # TODO Replace with acutall error
                print('ERROR: Customer was charging without occuping station')
            
            """
            I = self.model.station_power/self.ocv
            if self.soc < 1:
                while self.ocv < 4.2:
                    #print(f'Customer {self.unique_id} is CC charging')
                    self.ocv += 0.05 #temp value
                    #print(self.ocv)
                    if self.ocv > 4.2:
                        self.ocv == 4.2 #keep it at 4.2V
                    #print(f'Customer {self.unique_id} is not at {self.ocv} OCV')

                while self.ocv >= 4.2 and I > 0.01: #cv charging
                    #print(f'Customer {self.unique_id} is CV charging')
                    #keep voltage at 4.2V and decrease current until threshold is reached
                    I = I*0.99
                    #print(f'Current {I}')
                #print(f'Customer {self.unique_id} is fully charged')
            else:
                pass
                # print("no Charging needed")
            """
            #Temp - some adjustments needed
            if (self.current_battery_level + self.model.station_power/60 > self.battery_capacity):
                payment_amount = self.model.provider.pay(self.battery_capacity - self.current_battery_level, self)
                self.save_action_to_csv(CustomerActions.PROVIDER_EARNED, payment_amount)
                self.current_battery_level = self.battery_capacity
            else:
                payment_amount = self.model.provider.pay(self.model.station_power/60, self)
                self.save_action_to_csv(CustomerActions.PROVIDER_EARNED,payment_amount)
                self.current_battery_level += self.model.station_power/60
                # self.save_action_to_csv() ?
            #Temp 
            
            if(self.current_battery_level >= self.target_battery_level):
                if (self.model.charging_station.release_spot(self)):
                    self.state = CustomerState.LEFT_STATION
                    print(f'{convert_time_to_string(self.model.schedule.time)}: Customer {self.unique_id} left after charging his car for {self.model.schedule.time - self.arrival_time_in_minutes} minutes.')
                    self.save_action_to_csv(CustomerActions.LEFT_AFTER_CHARGING, self.getSoc())
                else:
                    # TODO Replace with acutall error
                    # print('ERROR: Customer was charging without occuping station')
                    pass
        else:
            if (self.model.charging_station.release_spot(self)):
                self.state = CustomerState.LEFT_STATION
                print(f'{convert_time_to_string(self.model.schedule.time)}: Customer {self.unique_id} left after charging his car for {self.model.schedule.time - self.arrival_time_in_minutes} minutes, because the charging rate was too high SOC: {self.getSoc()}')
                self.save_action_to_csv(CustomerActions.LEFT_BECAUSE_PRICE_IS_TO_HIGH, self.getSoc())
    
    # Here the provider asks the customer if he would be willing to release the spot for a bonus
    def negotiateReleaseSpot(self):
        if (self.evaluateSpotReleaseForBonus()):
            self.state = CustomerState.LEFT_STATION
            self.save_action_to_csv(CustomerActions.RELEASED_SPOT, self.getSoc())
            self.save_action_to_csv(CustomerActions.CUSTOMER_EARNED, self.model.provider.skip_queue_price - self.model.provider.skip_queue_provider_cut)
            return True
        else:
            print(f'{convert_time_to_string(self.model.schedule.time)}: Customer {self.unique_id} refused to release his spot for a bonus.')
            self.save_action_to_csv(CustomerActions.REFUSED_TO_RELEASE, self.getSoc())
            return False

    def negotiateReleaseSpotAuctionModel(self):
        if (self.evaluateSpotReleaseForBonusAuctionModel()):
            self.state = CustomerState.LEFT_STATION
            self.save_action_to_csv(CustomerActions.RELEASED_SPOT, self.getSoc())
            
            winning_bid = self.model.provider.current_winning_bid
            provider_cut = self.model.provider.current_provider_cut 
            earned_amount = winning_bid - provider_cut  #customer earns the difference between the winning bid and the provider cut
            self.save_action_to_csv(CustomerActions.CUSTOMER_EARNED, earned_amount)
            self.save_action_to_csv(CustomerActions.PROVIDER_EARNED_FROM_AUCTION, provider_cut)
            print(f'{convert_time_to_string(self.model.schedule.time)}: Customer {self.unique_id} release his spot for a bonus after the auction. Customer earned {earned_amount} and provider earned {provider_cut}')
            return True
        else:
            print(f'{convert_time_to_string(self.model.schedule.time)}: Customer {self.unique_id} refused to release his spot for a bonus.')
            self.save_action_to_csv(CustomerActions.REFUSED_TO_RELEASE, self.getSoc())
            return False
    
    def wait(self):
        if(self.model.charging_station.occupy_spot(self)):
            self.state = CustomerState.CHARGING
            self.model.number_of_customers += 1
            print(f'{convert_time_to_string(self.model.schedule.time)}: Customer {self.unique_id} started charging his car.')
            self.save_action_to_csv(CustomerActions.STARTING_TO_CHARGE, self.getSoc())
        elif(self.model.schedule.time - self.arrival_time_in_minutes >= self.waiting_time_in_minutes):
            self.state = CustomerState.LEFT_STATION
            self.model.number_of_customers_that_could_not_charge += 1
            print(f'{convert_time_to_string(self.model.schedule.time)}: Customer {self.unique_id} left after waiting for {self.model.schedule.time - self.arrival_time_in_minutes} minutes.')
            self.save_action_to_csv(CustomerActions.LEFT_AFTER_WAITING, self.getSoc())


    def evaluateSpotReleaseForBonus(self):
        self.discount_per_kwh = ((self.model.provider.skip_queue_price - self.model.provider.skip_queue_provider_cut) /(self.target_battery_level - self.current_battery_level)*1000)
        return (self.discount_per_kwh >= self.willingness_to_pay_release)
   
   
    def evaluateSpotReleaseForBonusAuctionModel(self):
        winning_bid = self.model.provider.current_winning_bid
        provider_cut = self.model.provider.current_bid_fee - winning_bid
        self.discount_per_kwh = ((winning_bid - provider_cut) / (self.target_battery_level - self.current_battery_level) * 1000)
        return (self.discount_per_kwh >= self.willingness_to_pay_release)


    def evaluateSkipQueueForExtraPayment(self):
        # try catch
            #check skip queue price (provider) if false
            #expected error
        try:
            skip_queue_price = self.model.provider.skip_queue_price
        except:
            return False

        # Calculate how much the extra payment would affect the cost per kwh for the amount the customer wants to charge
        self.extra_per_kwh = (skip_queue_price /(self.target_battery_level - self.current_battery_level)*1000)
        return (self.extra_per_kwh <= self.willingness_to_pay_extra_per_kwh)

    def getSoc(self):
        return self.current_battery_level/self.battery_capacity
    

    def save_action_to_csv(self, action, parameter):
        if(self.model.doPrints):
            print(f'{convert_time_to_string(self.model.schedule.time)}: Customer {self.unique_id}: {action} with parameter {parameter}')
        self.model.add_to_csv(self.unique_id, action, parameter)
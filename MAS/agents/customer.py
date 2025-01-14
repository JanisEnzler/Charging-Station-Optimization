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
    PAYMENT_FOR_CHARGING = 9
    CUSTOMER_EARNED = 10
    STARTING_TO_CHARGE = 11
    STARTED_TO_WAIT_IN_QUEUE = 12
    PAYMENT_FOR_AUCTION = 13

      
class CustomerAgent(mesa.Agent):
# Customer is equivalent to the agent in the MAS

    def __init__(self, unique_id, model, arrival_time_in_minutes, waiting_time_in_minutes, battery_capacity, current_battery_level, target_battery_level,willingness_to_pay_extra_per_kwh, willingness_to_pay_release, soc, ocv):
        super().__init__(unique_id, model)
        self.state = CustomerState.NOT_ARRIVED
        self.unique_id = unique_id
        self.model = model
        self.arrival_time_in_minutes = arrival_time_in_minutes
        self.waiting_time_in_minutes = waiting_time_in_minutes
        self.battery_capacity = battery_capacity
        self.current_battery_level = current_battery_level
        self.starting_battery_level = current_battery_level
        self.totalPaymentToProvider = 0
        self.target_battery_level = target_battery_level
        self.willingness_to_pay_extra_per_kwh = willingness_to_pay_extra_per_kwh
        self.willingness_to_pay_release = willingness_to_pay_release
        self.soc = soc
        self.ocv = ocv
        self.fully_charged = False

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
        self.perform_action(CustomerActions.ARRIVED, 0, 0, 0)
        if not self.check_price_threshold():
            self.model.number_of_customers_that_could_not_charge += 1
            self.perform_action(CustomerActions.LEFT_BECAUSE_PRICE_IS_TO_HIGH, 0, 0, 0)
            self.state = CustomerState.LEFT_STATION
        elif(self.model.charging_station.occupy_spot(self)):
            self.state = CustomerState.CHARGING
            self.perform_action(CustomerActions.STARTING_TO_CHARGE, 0, 0, 0)
            self.model.number_of_customers += 1
        elif hasattr( self.model.provider, 'request_skip_queue' ):
            if(self.evaluateSkipQueueForExtraPayment()):
                if(self.model.provider.request_skip_queue(self)):
                    self.state = CustomerState.CHARGING
                    self.model.number_of_customers += 1
                    self.perform_action(CustomerActions.SKIPED_QUEUE, self.model.provider.pay_skip_queue(), self.model.provider.skip_queue_price - self.model.provider.skip_queue_provider_cut, 0)
                    self.perform_action(CustomerActions.STARTING_TO_CHARGE, 0, 0, 0)
                    return
            self.state = CustomerState.WAITING
            self.perform_action(CustomerActions.STARTED_TO_WAIT_IN_QUEUE, 0, 0, 0)
        elif hasattr( self.model.provider, 'attend_auction' ):
            self.attend_auction()
        else:
            self.state = CustomerState.WAITING
            self.perform_action(CustomerActions.STARTED_TO_WAIT_IN_QUEUE, 0, 0, 0)


    def charge(self):
        # Check if electricity price is within personal threshold, otherwise leave the station
        if self.check_price_threshold(): #over the remaining time and charge the car and how much the customer has to pays
            if (self not in self.model.charging_station.occupied_spots):
                print('ERROR: Customer was charging without occuping station')
    
            delta = self.model.charging_station.charge(self, 1/60)

            # The payment is deducted from the customer's account every minute, because the price can change every minute
            self.perform_action(CustomerActions.PAYMENT_FOR_CHARGING, self.model.provider.pay(delta, self), 0, delta)
            
            if(self.current_battery_level >= self.target_battery_level or self.fully_charged):
                if (self.model.charging_station.release_spot(self)):
                    self.state = CustomerState.LEFT_STATION
                    self.perform_action(CustomerActions.LEFT_AFTER_CHARGING, 0, 0, 0)
                else:
                    print('ERROR: Customer was charging without occuping station')
                    pass
        else:
            if (self.model.charging_station.release_spot(self)):
                self.state = CustomerState.LEFT_STATION
                self.perform_action(CustomerActions.LEFT_BECAUSE_PRICE_IS_TO_HIGH, 0, 0, 0)
    
    # Here the provider asks the customer if he would be willing to release the spot for a bonus
    def negotiateReleaseSpot(self):
        if (self.evaluateSpotReleaseForBonus()):
            self.state = CustomerState.LEFT_STATION
            self.perform_action(CustomerActions.RELEASED_SPOT, 0, 0, 0)
            return True
        else:
            self.perform_action(CustomerActions.REFUSED_TO_RELEASE, 0, 0, 0)
            return False

    def negotiateReleaseSpotAuctionModel(self, winning_bid, provider_cut):
        earned_amount = winning_bid - provider_cut  #customer earns the difference between the winning bid and the provider cut
        if (self.evaluateSpotReleaseForBonusAuctionModel(earned_amount)):
            self.state = CustomerState.LEFT_STATION
            self.perform_action(CustomerActions.RELEASED_SPOT, 0, 0, 0)
            self.perform_action(CustomerActions.PAYMENT_FOR_AUCTION, provider_cut, earned_amount, 0)
            return True
        else:
            self.perform_action(CustomerActions.REFUSED_TO_RELEASE, 0, 0, 0)
            return False
    
    def wait(self):
        if(self.model.charging_station.occupy_spot(self)):
            self.state = CustomerState.CHARGING
            self.model.number_of_customers += 1
            self.perform_action(CustomerActions.STARTING_TO_CHARGE, 0, 0, 0)
        elif(self.model.schedule.time - self.arrival_time_in_minutes >= self.waiting_time_in_minutes):
            self.state = CustomerState.LEFT_STATION
            self.model.number_of_customers_that_could_not_charge += 1
            self.perform_action(CustomerActions.LEFT_AFTER_WAITING, 0, 0, 0)


    def evaluateSpotReleaseForBonus(self):
        self.discount_per_kwh = ((self.model.provider.skip_queue_price - self.model.provider.skip_queue_provider_cut) /(self.target_battery_level - self.current_battery_level)*1000)
        return (self.discount_per_kwh >= self.willingness_to_pay_release)
   
   
    def evaluateSpotReleaseForBonusAuctionModel(self, customer_cut):
        self.discount_per_kwh = ((customer_cut) /(self.target_battery_level - self.current_battery_level)*1000)
        return (self.discount_per_kwh >= self.willingness_to_pay_release)

    def attend_auction(self):
        bid = self.calculateBid()
        self.perform_action(CustomerActions.BIDDED_FOR_SPOT, 0, 0, 0)
        if(self.model.provider.attend_auction(self, bid)):
            #if self.state == CustomerState.CHARGING:
            if self in self.model.charging_station.occupied_spots:
                self.perform_action(CustomerActions.PAYMENT_FOR_CHARGING, self.model.provider.current_provider_cut, self.model.provider.current_bid_fee - self.model.provider.current_provider_cut, 0)
                self.model.number_of_customers += 1
                self.perform_action(CustomerActions.STARTING_TO_CHARGE, 0, 0, 0)
                self.state = CustomerState.CHARGING
                return True
            else:
                self.state = CustomerState.WAITING
                return False
        return False

    # A customer bids the amount he is willing to pay extra per kilowatt, for each kilowatt he plans to charge
    def calculateBid(self):
        return self.willingness_to_pay_extra_per_kwh * ((self.target_battery_level - self.current_battery_level) / 1000)

    def evaluateSkipQueueForExtraPayment(self):
        # Calculate how much the extra payment would affect the cost per kwh for the amount the customer wants to charge
        self.extra_per_kwh = (self.model.provider.skip_queue_price /(self.target_battery_level - self.current_battery_level)*1000)
        return (self.extra_per_kwh <= self.willingness_to_pay_extra_per_kwh)

    def getSoc(self):
        return self.current_battery_level/self.battery_capacity
    
    def perform_action(self, action, payment_to_provider, payment_to_customer, deltaWatthours):
        if(self.model.doPrints):
            print(f'{convert_time_to_string(self.model.schedule.time)}: Customer {self.unique_id} performed {action}')
        self.model.add_to_csv(action, self, payment_to_provider, payment_to_customer, deltaWatthours)
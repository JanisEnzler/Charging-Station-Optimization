import mesa
import pandas as pd

#from MAS.agents.provider import ProviderAgent
from MAS.agents.provider_dynamic_pricing_model import DynamicPricingProviderAgent
from MAS.agents.provider_negotiation_model import NegotiationModelProviderAgent
from MAS.agents.provider_auction_model import AuctionModelProviderAgent
from MAS.agents.provider import ProviderAgent
from MAS.agents.customer import CustomerAgent, CustomerState
from MAS.entities.charging_station import ChargingStation


class EnvironmentModel(mesa.Model):

    def __init__(self, num_charge_spots, station_power, skip_queue_price, skip_queue_provider_cut, price_per_kwh, doPrints, provider):
        super().__init__()

        self.schedule = mesa.time.BaseScheduler(self)
        self.charging_station = ChargingStation(num_charge_spots)
        self.station_power = station_power
        self.customers = []

        self.customers_charging = []
        self.customers_waiting = []
        self.changes = []
        self.number_of_customers = 0
        self.number_of_customers_that_could_not_charge = 0
        self.doPrints = doPrints
        data = {"Timestamp":[], "Agent":[], "Action":[], "SOC":[], "PaymentToProvider":[], "PaymentToCustomer":[] }
        self.df = pd.DataFrame(data)
        
        match provider:
            case 1:
                self.provider = ProviderAgent(1, self, price_per_kwh)
            case 2:
                self.provider = NegotiationModelProviderAgent(2,self, skip_queue_price, skip_queue_provider_cut, price_per_kwh)
            case 3:
                self.provider = DynamicPricingProviderAgent(3,self, price_per_kwh)
            case 4:
                self.provider = AuctionModelProviderAgent(4,self, price_per_kwh)
            case other:
                #error
                print("No provider selected")

        df = pd.read_csv('customers.csv')
        df_sorted = df.sort_values(by='arrival_time_in_minutes', ascending=True)
    
        for row in df_sorted.iterrows():
            a = CustomerAgent(row[0]+1, self, row[1]['arrival_time_in_minutes'], row[1]['waiting_time_in_minutes'], row[1]['battery_capacity'], row[1]['current_battery_level'], row[1]['target_battery_level'], row[1]['willingness_to_pay_extra_per_kwh'], row[1]['willingness_to_release'], row[1]['soc'], row[1]['ocv'])
            self.customers.append(a)
            self.schedule.add(a)

    def step(self):

        self.schedule.step()

    
        self.customers_charging.append(len(self.charging_station.occupied_spots))
        number_waiting = 0
        for customer in self.customers:
            if customer.state == CustomerState.WAITING:
                number_waiting += 1
        self.customers_waiting.append(number_waiting)


    def show_stats(self):
        print(f'\nNumber of customers that could not charge: {self.number_of_customers_that_could_not_charge}')
        print(f'Number of customers that charged: {self.number_of_customers}')
        self.provider.show_stats()

    def add_to_csv(self, action, customer, payment_to_provider, payment_to_customer):
        if len([self.schedule.time, customer.unique_id, action, customer.getSoc(), payment_to_provider, payment_to_customer]) == len(self.df.columns):
            self.df.loc[len(self.df)] = [self.schedule.time, customer.unique_id, action, customer.getSoc(), payment_to_provider, payment_to_customer]
        else:
            print("Error: wrong number of columns")
        

    def save_to_csv(self, name):
        self.df.to_csv(name, index=False)

import mesa

"""
The provider is the interface for the customer in the dynamic pricing model
If a customers soc is above 80% there is an additional fee added to each kilowatt charged, 
this additional fee is dynamicaly adjusted to steer the demand, and increase profitability

factors for dynamic pricing:
- soc
- high and low tarrif
-- standard price given, high during peak hours and low during off peak hours
- demand (queue)
"""


class DynamicPricingProviderAgent(mesa.Agent):
    def __init__(self, unique_id, model, price_per_kwh):
        super().__init__(unique_id, model)
        self.price_per_kwh = price_per_kwh
        self.earnings = 0
        self.kwh_consumed = 0


    def request_skip_queue(self, customer):
        return False
    
    def pay(self, watt_hours, customer):
        self.kwh_consumed += watt_hours/1000
        self.earnings += watt_hours/1000 * self.dynamic_pricing_rate(customer)
        return watt_hours/1000 * self.dynamic_pricing_rate(customer)

    def show_stats(self):
        print(f'\nProvider earned: {self.earnings:.2f} CHF')
        print(f'{self.kwh_consumed:.2f} kw/h of electricity was consumed')
        print(f'CHF per kw/h earned: {self.earnings/self.kwh_consumed:.4f}')

    def demand(self):
        #based on queue length
        pass

    def attend_auction(self,customer, bid) -> bool:
        return False
        
    
    def dynamic_pricing_rate(self, customer):
        if (customer.getSoc()) >= 0.8:
            return self.price_per_kwh * 1.05
        else:
            return self.price_per_kwh 

    

import mesa

# the provider is the interface if a customer wants to pay to skip the queue

class ProviderAgent(mesa.Agent):
    def __init__(self, unique_id, model, price_per_kwh):
        super().__init__(unique_id, model)
        self.price_per_kwh = price_per_kwh
        self.earnings = 0
        self.kwh_consumed = 0
        self.customer_swaps_for_payment = 0
    
    def pay(self, watt_hours, customer):
        self.kwh_consumed += watt_hours/1000
        self.earnings += watt_hours/1000 * self.price_per_kwh
        return watt_hours/1000 * self.price_per_kwh

    def show_stats(self):
        print(f'\nProvider earned: {self.earnings:.2f} CHF')
        print(f'{self.kwh_consumed:.2f} kw/h of electricity was consumed')
        print(f'{self.customer_swaps_for_payment} customers swapped spots for payment')
        print(f'CHF per kw/h earned: {self.earnings/self.kwh_consumed:.4f}')

    def dynamic_pricing_rate(self, customer):
        return self.price_per_kwh
        

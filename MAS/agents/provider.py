import mesa

# the provider is the interface if a customer wants to pay to skip the queue

class ProviderAgent(mesa.Agent):
    def __init__(self, unique_id, model, skip_queue_price, skip_queue_provider_cut, price_per_kwh):
        super().__init__(unique_id, model)
        self.skip_queue_price = skip_queue_price
        self.skip_queue_provider_cut = skip_queue_provider_cut
        self.price_per_kwh = price_per_kwh
        self.earnings = 0
        self.kwh_cunsumed = 0
        self.customer_swaps_for_payment = 0

    def request_skip_queue(self, customer):
        for Customer in sorted(self.model.charging_station.occupied_spots, key=lambda obj: obj.soc, reverse=True):
            if (Customer.negotiateReleaseSpot()):
                self.earnings += self.skip_queue_provider_cut
                self.model.charging_station.swap_spot(Customer, customer)
                self.customer_swaps_for_payment += 1
                return True
        return False
    
    def pay(self, watt_hours):
        self.kwh_cunsumed += watt_hours/1000
        self.earnings += watt_hours/1000 * self.price_per_kwh

    def show_stats(self):
        print(f'\nProvider earned: {self.earnings:.2f} CHF')
        print(f'{self.kwh_cunsumed:.2f} kw/h of electricity was consumed')
        print(f'{self.customer_swaps_for_payment} customers swapped spots for payment')
        print(f'CHF per kw/h earned: {self.earnings/self.kwh_cunsumed:.4f}')

        


    

    
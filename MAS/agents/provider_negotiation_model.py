import mesa

# the provider is the interface if a customer wants to pay to skip the queue

class NegotiationModelProviderAgent(mesa.Agent):
    def __init__(self, unique_id, model, skip_queue_price, skip_queue_provider_cut, price_per_kwh):
        super().__init__(unique_id, model)
        self.skip_queue_price = skip_queue_price
        self.skip_queue_provider_cut = skip_queue_provider_cut
        self.price_per_kwh = price_per_kwh
        self.earnings = 0
        self.kwh_consumed = 0
        self.customer_swaps_for_payment = 0

    def request_skip_queue(self, customer):
        for Customer in sorted(self.model.charging_station.occupied_spots, key=lambda obj: obj.soc, reverse=True):
            if (Customer.negotiateReleaseSpot()):
                self.earnings += self.skip_queue_provider_cut
                self.model.charging_station.swap_spot(Customer, customer)
                self.model.changes.append(self.model.schedule.time)
                self.customer_swaps_for_payment += 1
                return True
            return False
    
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
    
    #return False
    def attend_auction(self,customer, bid) -> bool:
        return False
    
    def pay_skip_queue(self):
        self.earnings += self.skip_queue_provider_cut
        # The rest of the skip queue price goes to the customer
        return self.skip_queue_provider_cut
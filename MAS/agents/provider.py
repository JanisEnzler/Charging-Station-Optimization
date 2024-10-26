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

    def request_skip_queue():
        pass


    def request_release():
        pass

    
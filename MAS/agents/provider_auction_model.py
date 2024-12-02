import mesa
#import Customer
from MAS.agents.customer import CustomerAgent, CustomerState, CustomerActions
from typing import Optional

class AuctionModelProviderAgent(mesa.Agent):
    def __init__(self, unique_id, model, price_per_kwh):
        super().__init__(unique_id, model)
        self.price_per_kwh = price_per_kwh
        self.earnings = 0
        self.kwh_consumed = 0
        self.customer_swaps_for_payment = 0
        self.current_winning_bid = 0
        self.current_bid_fee = 0
        self.current_provider_cut = 0

    def request_skip_queue(self, customer):
        return False

    #determine the winner of the auction, Optional if no auction took place
    def won_auction(self, waiting_customers: dict) -> Optional[CustomerAgent]:
        try:
            #customer with the highest willingness to pay wins the auction
            winner = max(waiting_customers, key=waiting_customers.get)
            self.current_winning_bid = waiting_customers[winner]
            
            sorted_bids = sorted(waiting_customers.values(), reverse=True)
            num_bidders = len(sorted_bids)
            #auction with only one bidder
            if num_bidders == 1:
                self.current_bid_fee = self.current_winning_bid
                self.current_provider_cut = self.current_bid_fee * 0.1 #10% cut for the provider
            #auction with two or more bidders
            elif num_bidders >= 2:
                second_highest_bid = sorted_bids[1]
                potential_fee = second_highest_bid * 1.1 #second highest bid plus 10% provision
                #second highest bid with the additional provision should not exceed the highest bid
                if potential_fee >= self.current_winning_bid:
                    self.current_bid_fee = self.current_winning_bid
                    self.current_provider_cut = self.current_bid_fee * 0.1
                else:
                    self.current_bid_fee = potential_fee
                    self.current_provider_cut = self.current_bid_fee - second_highest_bid
                
            for current_customer in sorted(self.model.charging_station.occupied_spots, 
                                    key=lambda obj: obj.soc, reverse=True):
                if current_customer.negotiateReleaseSpotAuctionModel():
                    self.earnings += self.current_provider_cut
                    self.model.charging_station.swap_spot(current_customer, winner)
                    self.model.changes.append(self.model.schedule.time)
                    self.customer_swaps_for_payment += 1
                    print(f'Time {self.model.schedule.time}: Customer {winner.unique_id} '
                        f'won the auction with a fee of: {self.current_bid_fee}.')
                    waiting_customers.clear()
                    return winner
                    
            # if no auction took place
            self.current_winning_bid = 0
            self.current_bid_fee = 0
            return None
                
        except Exception as e:
            self.current_winning_bid = 0
            self.current_bid_fee = 0
            print(f'Error during auction: {str(e)}')
            return None



    def attend_auction(self) -> bool:
        # customers that are waiting for a spot
        waiting_customers = {
            customer: customer.willingness_to_pay_extra_per_kwh
            for customer in self.model.schedule.agents
            if isinstance(customer, CustomerAgent) and customer.state == CustomerState.NOT_ARRIVED
        }
        
        #no customers means no auction
        if not waiting_customers:
            if self.model.doPrints:
                print(f'Time {self.model.schedule.time}: No auction took place. No customers are waiting.')
            return False
        
       #auction is taking place
        if self.model.doPrints:
            print(f'Time {self.model.schedule.time}: Auction is taking place with {len(waiting_customers)} customers.')
        
        winner = self.won_auction(waiting_customers)
        return winner is not None

    def pay(self, watt_hours, customer):
        self.kwh_consumed += watt_hours/1000
        self.earnings += watt_hours/1000 * self.dynamic_pricing_rate(customer)
        return watt_hours/1000 * self.price_per_kwh

    def show_stats(self):
        print(f'\nProvider earned: {self.earnings:.2f} CHF')
        print(f'{self.kwh_consumed:.2f} kw/h of electricity was consumed')
        print(f'{self.customer_swaps_for_payment} customers swapped spots for payment')
        print(f'CHF per kw/h earned: {self.earnings/self.kwh_consumed:.4f}')
    
    def dynamic_pricing_rate(self, customer):
        return self.price_per_kwh

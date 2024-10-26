class ChargingStation:
    def __init__(self, charging_spots):
        self.charging_spots = charging_spots
        self.occupied_spots = []
        
#customer_id 
    def occupy_spot(self, customer):
        if len(self.occupied_spots) < self.charging_spots and customer not in self.occupied_spots:
            self.occupied_spots.append(customer)
            return True
        else:
            return False
        
    def release_spot(self, customer):
        if customer in self.occupied_spots:
            self.occupied_spots.remove(customer)
            return True
        else:
            return False
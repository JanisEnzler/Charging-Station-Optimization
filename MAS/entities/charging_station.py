class ChargingStation:
    def __init__(self, charging_spots):
        self.charging_spots = charging_spots
        self.occupied_spots = []
        
#customer_id 
    def occupy_spot(self, customer_id):
        if len(self.occupied_spots) < self.charging_spots and customer_id not in self.occupied_spots:
            self.occupied_spots.append(customer_id)
            return True
        else:
            return False
        
    def release_spot(self, customer_id):
        if customer_id in self.occupied_spots:
            self.occupied_spots.remove(customer_id)
            return True
        else:
            return False
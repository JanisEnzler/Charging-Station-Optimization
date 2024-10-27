class ChargingStation:
    def __init__(self, charging_spots):
        self.charging_spots = charging_spots
        self.occupied_spots = []
        
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
        
    def swap_spot(self, customer1, customer2):
        if customer1 in self.occupied_spots and customer2 not in self.occupied_spots:
            self.occupied_spots.remove(customer1)
            self.occupied_spots.append(customer2)
            return True
        else:
            return False
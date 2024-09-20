#class for price calculation
class PriceCalculation:
    #static method to calculate price
    @staticmethod
    def calculate_price(efficiency, availability, reservation, electricity_cost):
        return (efficiency * availability * reservation * electricity_cost) / 100
    
    calculate_price(90, 95, 98, 0.12) # 0.1026
#class for price calculation
class PriceCalculation:
    #static method to calculate price
    @staticmethod
    def calculate_price(standard_rate, efficiency, availability, reservation, electricity_cost):

        calculated_price = (standard_rate+efficiency * availability * reservation * electricity_cost) / 100
        return calculated_price

print(PriceCalculation.calculate_price(10, 0.9, 0.8, 0.9, 0.12)) # 0.0864
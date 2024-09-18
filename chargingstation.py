#provider class
import time

class Chargingstation:
    #electric vehicle charging station
    def __init__(self, name, price, charging_speed):
        self.name = name
        self.price = price
        self.charging_speed = charging_speed
    

    #charging a car object with a current battery leve to the full capacity
    def charge(self, car):
        if car.battery_level < car.battery_capacity:
            car.battery_level = car.battery_capacity
            return True
    
    #simulates the charging process, with a given time in hours and a car object
    def simulate_charging(self, car, delta_time):
        #charging_speed is the amount of battery_level increase per hour7
        if car.battery_level < car.battery_capacity:
            car.battery_level += self.charging_speed * delta_time * self.calculate_charging_efficiency(car)
            #if battery_level exceeds capacity, set it to capacity
            if car.battery_level > car.battery_capacity:
                car.battery_level = car.battery_capacity
            return True
        return False

    # calculates the charging efficiency, based on battery_level, capacity and charging_speed
    def calculate_charging_efficiency(self, car):
        # Replace with actuall efficiency curve
        efficiency = 1 - 0.3 * (car.battery_level/car.battery_capacity)
        return efficiency



"""displaying the current battery level with real live observation of the car in a linear function
linear function y=m*x+b
@param y = battery_level of car
@param x = time in hours
@param m = efficiency from def calculate_charging_efficiency

def display_current_battery_level(self, car):
        m = self.calculate_charging_efficiency(car)
        b = car.battery_level
        
        for x in range()

        for x in range(0, 1):
            y = m*x+b
            print(f"Time: {x} hours, Battery Level: {y}")
"""

class Car:
    def __init__(self, battery_capacity, battery_level):
        # Battery capacity and level are both in watt-hours
        self.battery_capacity = battery_capacity
        self.battery_level = battery_level

    def calculate_charging_duration(self, target_battery_level, charging_power):
        if target_battery_level > self.battery_capacity:
            raise ValueError("Target battery level exceeds capacity")
        if target_battery_level < self.battery_level:
            raise ValueError("Target battery level is below current level")
        # Efficiency decreases as battery level increases, so we need to calculate the average efficiency
        average_efficiency = (self.efficiency(self.battery_level) + self.efficiency(target_battery_level)) / 2
        # Calculate the time to charge the battery to the target level
        return (target_battery_level - self.battery_level) / (charging_power * average_efficiency)


    def efficiency(self, battery_level):
        # Efficiency decreases as battery level increases
        return 1 - (battery_level / self.battery_capacity)* 0.3
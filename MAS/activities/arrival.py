from MAS.activities.negotiation import Negotiation

class Arrival:
    # The arrival activity has no delta T, because it happens at one instance, and then triggers other, longer activities, based on the state of the environment
    def __init__(self, Time, Customer, ChargingStation):
        self.Time = Time
        self.Customer = Customer
        self.ChargingStation = ChargingStation


    def stateChangeFunction(self):
        if self.ChargingStation.isAvailable:
            self.ChargingStation.charge(self.customer.car)
        else:
            self.Customer.scheduleActivity(Negotiation)
import unittest
import numpy as np
import sys
import os
import matplotlib.pyplot as plt

parent_dir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
sys.path.insert(0, parent_dir)

from MAS.entities.charging_station import ChargingStation
from MAS.agents.customer import CustomerState, CustomerAgent

"""
edge cases:
occupy_spot
- Station full, but customer wants to charge
- charging station can fit as many as defined

- test id so it can't occupy multiple charging spots


- customer needs to first charge to be able to release the spot

- if a spot is released, another customer can use it


"""

class TestChargingStation(unittest.TestCase):
    
    def test_overbooking(self):
        chargingStation = ChargingStation(3, 80, 500, 0.8, 1)
        chargingStation.occupy_spot(2)
        chargingStation.occupy_spot(3)
        self.assertTrue(chargingStation.occupy_spot(1))
        self.assertFalse(chargingStation.occupy_spot(4))


    #test to prevent overcharing and if a customer has already 100% battery_level, Soc=1)

    def test_occupying_same_spot_twice(self):
        chargingStation = ChargingStation(3, 80, 500, 0.8, 1)
        chargingStation.occupy_spot(1)
        self.assertFalse(chargingStation.occupy_spot(1))


    def test_cannot_release_if_not_occupied(self):
        chargingStation = ChargingStation(3, 80, 500, 0.8, 1)
        self.assertFalse(chargingStation.release_spot(1))


    def test_release(self):
        chargingStation = ChargingStation(3, 80, 500, 0.8, 1)
        self.assertEqual(len(chargingStation.occupied_spots),0)
        chargingStation.occupy_spot(1)
        self.assertEqual(len(chargingStation.occupied_spots),1)
        chargingStation.release_spot(1)
        self.assertEqual(len(chargingStation.occupied_spots),0)

    def test_charging(self):
        array = []
        chargingStation = ChargingStation(3, 80, 500, 0.8, 1)
        customer = CustomerAgent(1, None, None, None, 50000, 0, 50000, 0, 0, 0, 0 )
        while not customer.fully_charged:
            chargingStation.charge(customer, (1/60))
            array.append(customer.getSoc())

        print(customer.getSoc())
        plt.plot(array)
        plt.show()
        self.assertTrue(customer.fully_charged)
        



if __name__ == '__main__':
    unittest.main()
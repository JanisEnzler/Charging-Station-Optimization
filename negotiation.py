#negotiation class and receive nash equilibrium

import numpy as np
import random
import math

import customer 
from chargingstation import Chargingstation

class Negotiation:

    def __init__(self, customer, chargingstation):
        self.customer = customer
        self.chargingstation = chargingstation
        
    def negotiate(self):
        print("Negotiation class")
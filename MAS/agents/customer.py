import mesa
import numpy as np
import pandas as pd
import car

class Customer(mesa.Agent):
#customer is equivalent to the agent in the MAS

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)


    def step(self):
        print(f"This is a test {str(self.unique_id)}.")

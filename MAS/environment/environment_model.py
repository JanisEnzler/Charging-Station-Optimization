import mesa

import pandas as pd

#from MAS.agents.customer import CustomerAgent
from MAS.agents.customer import CustomerAgent
from MAS.entities.charging_station import ChargingStation


class Environment_Model(mesa.Model):

    def __init__(self, num_charge_spots):
        super().__init__()

        self.schedule = mesa.time.RandomActivation(self)
        self.charging_station = ChargingStation(num_charge_spots)

        df = pd.read_csv('customers.csv')

        for row in df.iterrows():
            a = CustomerAgent(row[0]+1, self, row[1]['arrival_time_in_minutes'], row[1]['waiting_time_in_minutes'], row[1]['battery_capacity'], row[1]['current_battery_level'], row[1]['target_battery_level'])
            self.schedule.add(a)



    def step(self):
        self.schedule.step()




    """Base class for models in the Mesa ABM library.
basic attributes and methods necessary for initializing and running a simulation model.


    Attributes:
        running: A boolean indicating if the model should continue running.
        schedule: An object to manage the order and execution of agent steps.
        current_id: A counter for assigning unique IDs to agents.

    Properties:
        agents: An AgentSet containing all agents in the model
        agent_types: A list of different agent types present in the model.
        agents_by_type: A dictionary where the keys are agent types and the values are the corresponding AgentSets.

    Methods:
        get_agents_of_type: Returns an AgentSet of agents of the specified type.
            Deprecated: Use agents_by_type[agenttype] instead.
        run_model: Runs the model's simulation until a defined end condition is reached.
        step: Executes a single step of the model's simulation process.
        next_id: Generates and returns the next unique identifier for an agent.
        reset_randomizer: Resets the model's random number generator with a new or existing seed.
        initialize_data_collector: Sets up the data collector for the model, requiring an initialized scheduler and agents.
        register_agent : register an agent with the model
        deregister_agent : remove an agent from the model

    Notes:
        Model.agents returns the AgentSet containing all agents registered with the model. Changing
        the content of the AgentSet directly can result in strange behavior. If you want change the
        composition of this AgentSet, ensure you operate on a copy.

    """
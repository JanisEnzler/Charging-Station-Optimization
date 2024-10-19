import mesa

from MAS.agents.customer import Customer


class Environment_Model(mesa.Model):

    def __init__(self, N):
        super().__init__()
        self.num_agents = N
        self.schedule = mesa.time.RandomActivation(self)

        for i in range(self.num_agents):
            a = Customer(i, self)
            self.schedule.add(a)


    def step(self):
        self.schedule.step()



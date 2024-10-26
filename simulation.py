import mesa

from MAS.environment.environment_model import Environment_Model

model = Environment_Model(1, 100000)
for i in range(1440):
    model.step()



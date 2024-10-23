import mesa

from MAS.environment.environment_model import Environment_Model

model = Environment_Model(10)
for i in range(1440):
    model.step()



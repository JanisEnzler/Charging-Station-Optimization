import mesa
#run the Environment_Model
import seaborn as sns

from MAS.environment.environment_model import Environment_Model

model = Environment_Model(10)
model.step()



import mesa
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

CHARGING_POWER = config.getint('charging_station', 'CHARGING_POWER_IN_WATTS')
NUMBER_OF_CHARGING_STATIONS = config.getint('charging_station', 'NUMBER_OF_CHARGING_STATIONS')
PRICE_PER_KWH_IN_CHF = config.getfloat('charging_station', 'PRICE_PER_KWH_IN_CHF')
SKIP_QUEUE_PRICE_CHF = config.getfloat('charging_station', 'SKIP_QUEUE_PRICE_CHF')
SKIP_QUEUE_PROVIDER_CUT = config.getfloat('charging_station', 'SKIP_QUEUE_PROVIDER_CUT')
NUMBER_OF_DAYS = config.getint('simulation', 'NUMBER_OF_DAYS')



from MAS.environment.environment_model import Environment_Model

model = Environment_Model(NUMBER_OF_CHARGING_STATIONS, CHARGING_POWER, SKIP_QUEUE_PRICE_CHF, SKIP_QUEUE_PROVIDER_CUT, PRICE_PER_KWH_IN_CHF)
for i in range(1440*NUMBER_OF_DAYS):
    model.step()

model.provider.show_stats()



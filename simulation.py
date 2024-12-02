import mesa
import configparser

from ploter import plot_array_as_hist, plot_array, plot_array_as_bar

config = configparser.ConfigParser()
config.read('config.ini')

CHARGING_POWER = config.getint('charging_station', 'CHARGING_POWER_IN_WATTS')
NUMBER_OF_CHARGING_STATIONS = config.getint('charging_station', 'NUMBER_OF_CHARGING_STATIONS')
PRICE_PER_KWH_IN_CHF = config.getfloat('charging_station', 'PRICE_PER_KWH_IN_CHF_HIGH')
SKIP_QUEUE_PRICE_CHF = config.getfloat('charging_station', 'SKIP_QUEUE_PRICE_CHF')
SKIP_QUEUE_PROVIDER_CUT = config.getfloat('charging_station', 'SKIP_QUEUE_PROVIDER_CUT')
NUMBER_OF_DAYS = config.getint('simulation', 'NUMBER_OF_DAYS')
DO_PRINTS = config.getboolean('simulation', 'DO_PRINTS')


from MAS.environment.environment_model import EnvironmentModel

"""
baseline_model = EnvironmentModel(NUMBER_OF_CHARGING_STATIONS, CHARGING_POWER,None,None,PRICE_PER_KWH_IN_CHF,DO_PRINTS, 1)
for i in range(1440*NUMBER_OF_DAYS):
    baseline_model.step()

negotiation_model = EnvironmentModel(NUMBER_OF_CHARGING_STATIONS, CHARGING_POWER, SKIP_QUEUE_PRICE_CHF, SKIP_QUEUE_PROVIDER_CUT, PRICE_PER_KWH_IN_CHF, DO_PRINTS, 2)
for i in range(1440*NUMBER_OF_DAYS):
    negotiation_model.step()


dynamic_pricing_model = EnvironmentModel(NUMBER_OF_CHARGING_STATIONS, CHARGING_POWER, SKIP_QUEUE_PRICE_CHF, SKIP_QUEUE_PROVIDER_CUT, PRICE_PER_KWH_IN_CHF, DO_PRINTS, 3)
for i in range(1440*NUMBER_OF_DAYS):
    dynamic_pricing_model.step()

"""


auction_model = EnvironmentModel(NUMBER_OF_CHARGING_STATIONS, CHARGING_POWER, None, None, PRICE_PER_KWH_IN_CHF, DO_PRINTS, 4)
for i in range(1440*NUMBER_OF_DAYS):
    auction_model.step()


#save the models in csv
#baseline_model.save_to_csv('baseline_outcome.csv')
#negotiation_model.save_to_csv('negotiation_outcome.csv')
#dynamic_pricing_model.save_to_csv('dynamic_pricing_outcome.csv')

auction_model.save_to_csv('auction_outcome.csv')



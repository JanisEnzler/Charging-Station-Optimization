import mesa
import configparser
import threading

from ploter import plot_array_as_hist, plot_array, plot_array_as_bar

config = configparser.ConfigParser()
config.read('config.ini')

CHARGING_AMPERAGE = config.getint('charging_station', 'CHARGING_AMPERAGE')
CHARGING_VOLTAGE = config.getint('charging_station', 'CHARGING_VOLTAGE')
CC_CV_THRESHOLD = config.getfloat('charging_station', 'CC_CV_THRESHOLD')
CHARGING_BETA_VALUE = config.getfloat('charging_station', 'CHARGING_BETA_VALUE')
NUMBER_OF_CHARGING_STATIONS = config.getint('charging_station', 'NUMBER_OF_CHARGING_STATIONS')
PRICE_PER_KWH_IN_CHF = config.getfloat('charging_station', 'PRICE_PER_KWH_IN_CHF_HIGH')
SKIP_QUEUE_PRICE_CHF = config.getfloat('charging_station', 'SKIP_QUEUE_PRICE_CHF')
SKIP_QUEUE_PROVIDER_CUT = config.getfloat('charging_station', 'SKIP_QUEUE_PROVIDER_CUT')
NUMBER_OF_DAYS = config.getint('simulation', 'NUMBER_OF_DAYS')
DO_PRINTS = config.getboolean('simulation', 'DO_PRINTS')



from MAS.environment.environment_model import EnvironmentModel


def print_loading_bar(step, total_steps):
    #Deletet the last loading bar
    print("\b"*100, end="")
    print(f"{step/total_steps*100:.2f}%", end="")

""" baseline_model = EnvironmentModel(NUMBER_OF_CHARGING_STATIONS, CHARGING_AMPERAGE, CHARGING_VOLTAGE, CC_CV_THRESHOLD, CHARGING_BETA_VALUE, None,None,PRICE_PER_KWH_IN_CHF,DO_PRINTS, 1)
for i in range(1440*NUMBER_OF_DAYS):
    baseline_model.step()
    print_loading_bar(i, 1440*NUMBER_OF_DAYS)
baseline_model.save_to_csv('baseline_outcome.csv')

print("\nBaseline model done")


negotiation_model = EnvironmentModel(NUMBER_OF_CHARGING_STATIONS, CHARGING_AMPERAGE, CHARGING_VOLTAGE, CC_CV_THRESHOLD, CHARGING_BETA_VALUE, SKIP_QUEUE_PRICE_CHF, SKIP_QUEUE_PROVIDER_CUT, PRICE_PER_KWH_IN_CHF, DO_PRINTS, 2)
for i in range(1440*NUMBER_OF_DAYS):
    negotiation_model.step()
    print_loading_bar(i, 1440*NUMBER_OF_DAYS)
negotiation_model.save_to_csv('negotiation_outcome.csv')

print("\nNegotiation model done")
"""

dynamic_pricing_model = EnvironmentModel(NUMBER_OF_CHARGING_STATIONS, CHARGING_AMPERAGE, CHARGING_VOLTAGE, CC_CV_THRESHOLD, CHARGING_BETA_VALUE, None, None, PRICE_PER_KWH_IN_CHF, DO_PRINTS, 3)
for i in range(1440*NUMBER_OF_DAYS):
    dynamic_pricing_model.step()
    print_loading_bar(i, 1440*NUMBER_OF_DAYS)
dynamic_pricing_model.save_to_csv('dynamic_pricing_outcome.csv')

print("\nDynamic pricing model done")

"""
auction_model = EnvironmentModel(NUMBER_OF_CHARGING_STATIONS, CHARGING_AMPERAGE, CHARGING_VOLTAGE, CC_CV_THRESHOLD, CHARGING_BETA_VALUE, None, None, PRICE_PER_KWH_IN_CHF, DO_PRINTS, 4)
for i in range(1440*NUMBER_OF_DAYS):
    auction_model.step()
    print_loading_bar(i, 1440*NUMBER_OF_DAYS)
auction_model.save_to_csv('auction_outcome.csv')

print("\nAuction model done")
"""



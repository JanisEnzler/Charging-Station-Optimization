import pandas as pd
import numpy as np

#simple price calculation
price_df = {'Provider': ['MOVE', "Plug'n Roll", 'Evpass', 'eCarUp', 'Tesla'],
                         'Charging_rate': [0.70, 0.83, 0.98, 1.19, 0.40],
                         'Cost_for_every_session': [0, 1.78, 0, 0, 0],
                         'Cost_for_long_session': [18.00, 0, 0, 0, 0],
                         }

print(price_df)
mean_standard_rate = sum(price_df['Charging_rate']) / len(price_df['Charging_rate'])
mean_standard_rate = round(mean_standard_rate, 2)
print(mean_standard_rate)

import pandas as pd
import scipy as sci


data = {
    "U_OCV": [4.1617, 4.0913, 4.0749, 4.0606, 4.0153, 3.9592, 3.9164, 3.8687, 
              3.8163, 3.7735, 3.7317, 3.6892, 3.6396, 3.5677, 3.5208, 3.4712, 
              3.386, 3.288, 3.2037, 3.0747],
    "SOC": [1.0, 0.9503, 0.9007, 0.851, 0.8013, 0.7517, 0.702, 0.6524, 
            0.6027, 0.553, 0.5034, 0.4537, 0.404, 0.3543, 0.3046, 0.255, 
            0.2053, 0.1556, 0.1059, 0.0563]
}

# Erstellen des DataFrames
df = pd.DataFrame(data)
print(df)

# Interpolation der OCV-SOC-Beziehung
def interpolate_data(data):
    interpolation_function = sci.interp1d(data["SOC"], data["U_OCV"], kind='linear', fill_value="extrapolate")
    return interpolation_function

#current soc form the CustmerAgent attribut soc
#class CustomerAgent(mesa.Agent):
#
#    def __init__(self, unique_id, model, arrival_time_in_minutes, waiting_time_in_minutes, battery_capacity, current_battery_level, target_battery_level, soc):
#        super().__init__(unique_id, model)
#        self.state = CustomerState.NOT_ARRIVED
#        self.arrival_time_in_minutes = arrival_time_in_minutes
#        self.waiting_time_in_minutes = waiting_time_in_minutes
#        self.battery_capacity = battery_capacity
#        self.current_battery_level = current_battery_level
#        self.target_battery_level = target_battery_level
#        self.soc = soc
#        #self.ocv = ocv

#currewnt soc from the CustomerAgent attribut soc



# Interpolierte Daten
interpolated_data = interpolate_data(df)
print(interpolated_data(0.5))


"""
# Anpassen des Spaltennamens, falls erforderlich
if 'soc' in customer_data.columns:
    current_soc = customer_data['soc']
elif 'current_battery_level' in customer_data.columns and 'battery_capacity' in customer_data.columns:
    current_soc = customer_data['current_battery_level'] / customer_data['battery_capacity']
else:
    raise KeyError("Die erforderlichen Spalten sind in der CSV-Datei nicht vorhanden.")

# Bestimmen des entsprechenden OCV-Werts für den SOC-Wert
current_ocv = interpolated_data(current_soc)
print(current_ocv)
"""


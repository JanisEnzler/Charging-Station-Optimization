import numpy as np


battery_capacity = 50_000 # 50 kW
ocv = #given from ocv-soc_relationship.py
P = 50_000 # 50 kW given from charging station
soc = #given from ocv-soc_relationship.py
U = #given from ocv-soc_relationship.py
I = P/U #Ampere

#temperature checking optional

#trickle charging left out for now

#while soc is smaller than 100%
while soc < 1.0:
    if ocv < 4.2:
        ocv += 0.01
        I = P/ocv
        print("Constant Current Charging")
    else:
        ocv = 4.2
        ocv *= 0.99
        print("Constant Voltage Charging")
    
    soc += I/battery_capacity /3600
print(soc)


#different appraoch
if I == 4.2 and U < 4.2:
    I = np.ones_like(U)
    print("Constant current charging")
elif U >= 4.2:
    print("Constant voltage charging")
else:
    print("no charging needed")







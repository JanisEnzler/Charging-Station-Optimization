import pandas as pd
import numpy as np
from scipy import interpolate

df = pd.read_csv("ocv-soc_relationship.csv")

x = 0.5

interpolation = interpolate.interp1d(df["SOC"], df["U_ocv"], kind='linear', fill_value="extrapolate")
current_ocv = interpolation(x)

print(f"Der OCV-Wert für SOC = {x} ist: {current_ocv:.1f}")

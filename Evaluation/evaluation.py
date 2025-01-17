import pandas as pd 
#import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt

# CSV-Dateien einlesen
baseline_df = pd.read_csv('baseline_outcome.csv')
negotiation_df = pd.read_csv('negotiation_outcome.csv')
dynamic_df = pd.read_csv('dynamic_pricing_outcome.csv')
auction_df = pd.read_csv('auction_outcome.csv')

def get_metrics(df):
    customers = len(df[df['Action'] == 'CustomerActions.STARTING_TO_CHARGE'])
    payment = df['PaymentToProvider'].sum()
    watts = df['AmountCharged'].sum()
    return customers, payment, watts

# Baseline-Metriken als Referenz
baseline_customers, baseline_payment, baseline_watts = get_metrics(baseline_df)

# Vergleichsmodelle
models = {
    "Negotiation": negotiation_df,
    "Dynamic": dynamic_df,
    "Auction": auction_df
}

# Relative Unterschiede berechnen
results = []
for model_name, df in models.items():
    customers, payment, watts = get_metrics(df)
    
    rel_customers = ((customers - baseline_customers) / baseline_customers) * 100
    rel_payment = ((payment - baseline_payment) / baseline_payment) * 100
    rel_watts = ((watts - baseline_watts) / baseline_watts) * 100
    
    results.append({
        "Model": model_name,
        "Customers (%)": f"{rel_customers:+.2f}%",
        "Payment (%)": f"{rel_payment:+.2f}%",
        "Watts (%)": f"{rel_watts:+.2f}%"
    })

# Ergebnisse als DataFrame
results_df = pd.DataFrame(results)

print("\nRelative Unterschiede zur Baseline:")
print(results_df.to_string(index=False))

print("\nAbsolute Baseline-Werte:")
print(f"Customers: {baseline_customers}")
print(f"Payment: {baseline_payment:.2f}")
print(f"Watts: {baseline_watts:.2f}")
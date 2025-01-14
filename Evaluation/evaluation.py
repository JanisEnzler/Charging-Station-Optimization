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



# Line plots for relative changes
plt.figure(figsize=(12, 6))

for metric in metrics:
    plt.plot(df['Model'], df[metric], marker='o', label=metric)

plt.title("Relative Changes Across Models Compared to Baseline", fontsize=14)
plt.xlabel('Model', fontsize=12)
plt.ylabel('Relative Change (%)', fontsize=12)
plt.axhline(0, color='black', linestyle='--', linewidth=0.8)
plt.legend(title="Metrics", fontsize=10)
plt.grid(True, linestyle='--', linewidth=0.5, alpha=0.7)
plt.tight_layout()
plt.show()


"""
#read the csv data into a pandas dataframe

baseline_model_df = pd.read_csv('baseline_outcome.csv')
baseline_model_df.head()
neogotiation_model_df = pd.read_csv('negotiation_outcome.csv')
neogotiation_model_df.head()
dynamic_model_df = pd.read_csv('dynamic_pricing_outcome.csv')
dynamic_model_df.head()
auction_model_df = pd.read_csv('auction_outcome.csv')
auction_model_df.head()


#amount of customer charging
def print_stats(df, model):
    print(f"\nModel: {model}")
    # Amount of customers that could charge:
    print(f"Amount of customers that charged at the station: {len(df[df['Action'] == 'CustomerActions.STARTING_TO_CHARGE'])}")
    # Total amount payed to provider
    print(f"Total amount payed to provider: {df['PaymentToProvider'].sum()}")
    # Total watts charged
    print(f"Total watts charged: {df['AmountCharged'].sum()}")

print_stats(baseline_model_df, "Baseline Model")
print_stats(neogotiation_model_df, "Negotiation Model")
print_stats(dynamic_model_df, "Dynamic Pricing Model")
print_stats(auction_model_df, "Auction Model")

#Timestamp,Agent,Action,SOC,TotalAmountCharged,PaymentToProvider,PaymentToCustomer



#hypothesis 0 = baseline model
#hypothesis 1 = negotiation model
#hypothesis 2 = dynamic pricing model
#hypothesis 3 = auction model

metrics = ['TotalAmountCharged', 'PaymentToProvider', 'PaymentToCustomer', 'Swaps', 'Auctions']
data[metrics] = data[metrics].apply(pd.to_numeric, errors='coerce')


results = []

for metric in metrics:
    print(f"Metric: {metric}")
    baseline_model_df = baseline_model_df[metric].dropna()
    if agent != 'baseline_agent'_
        models_values = data 
        
"""


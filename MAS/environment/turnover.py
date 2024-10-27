def kw_per_session(battery_capacity, soc, target_battery_level):
    target_soc = (target_battery_level/battery_capacity)
    total_used_kw = battery_capacity * (target_soc - soc)
    return total_used_kw

def calculate_turnover(total_used_kw, standard_rate):
    turnover = total_used_kw * standard_rate
    return turnover

def calculate_costs(total_used_kw, cost_per_kw):
    costs = total_used_kw * cost_per_kw
    return costs

def profit(turnover, total_costs):
    profit = turnover - total_costs
    return profit

standard_rate = 0.82 #calculated mean
cost_per_kw = 0.35 #given from the kanton


#given from customer csv
used_kw = kw_per_session(50, 0.2, 40)
total_costs = calculate_costs(used_kw, cost_per_kw)

turnover = calculate_turnover(used_kw, standard_rate)
print(f"Turnover: {turnover:.2f} CHF")

profit = profit(turnover, total_costs)
print(f"Profit: {profit:.2f} CHF")

#TODO: MAS and turnover after every session

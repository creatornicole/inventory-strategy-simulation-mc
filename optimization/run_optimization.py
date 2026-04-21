import numpy as np
import pandas as pd
from model.customer_satisfaction import get_customer_satisfaction

def find_optimal_waggons(simulation_results, w_options, capacity_per_waggon, lambda_param):
    df = pd.DataFrame(simulation_results)
    optimized_data = []

    v_satisfaction = np.vectorize(get_customer_satisfaction)

    for (day, hour), group in df.groupby(["day", "hour"]):
        revenues_all_runs = group["revenue_cum_arr"].values
        costs_all_runs = group["cost"].values
        demands_all_runs = group["demand"].values

        expected_utilities = []

        for w in w_options:
            total_capacity = w * capacity_per_waggon

            actual_revenues = np.array([
                revs[total_capacity - 1] if len(revs) >= total_capacity
                else (revs[-1] if len(revs) > 0 else 0)
                for revs in revenues_all_runs
            ])

            w_costs = w * costs_all_runs

            passengers_per_waggon = np.minimum(total_capacity, demands_all_runs) / w
            satisfaction_scores = v_satisfaction(passengers_per_waggon)
            dissatisfaction_penalty = lambda_param * (1 - (satisfaction_scores / 100))

            utilies = actual_revenues - w_costs - dissatisfaction_penalty

            expected_utilities.append((w, np.mean(utilies)))
        
        best_w, best_utility = max(expected_utilities, key=lambda x: x[1])

        optimized_data.append({
            "day": day,
            "hour": hour,
            "optimal_w": best_w,
            "expected_utilities": best_utility
        })
    
    return pd.DataFrame(optimized_data)
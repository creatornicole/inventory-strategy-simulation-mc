import numpy as np
import pandas as pd
from model.customer_satisfaction import get_customer_satisfaction
from model.cost import calc_switching_costs

def find_optimal_waggons(simulation_results, w_options, capacity_per_waggon, lambda_param, overflow_costs, cost_up, cost_down):
    df = pd.DataFrame(simulation_results)

    # calculate the average utility for each "w" per hour
    utility_lookup = calc_utility_matrix(df, w_options, capacity_per_waggon, lambda_param, overflow_costs)

    # determine the optimal sequence of waggons (= schedule) for the entire day by accounting for switching costs
    result_df = find_best_switching_path(utility_lookup, w_options, cost_up, cost_down)

    return result_df

def calc_utility_matrix(df_simulations, w_options, capacity_per_waggon, lambda_param, overflow_costs):
    v_satisfaction = np.vectorize(get_customer_satisfaction)
    utility_lookup = {}

    for (day, hour), group in df_simulations.groupby(["day", "hour"]):
        revenues_all_runs = group["revenue_cum_arr"].values
        costs_all_runs = group["cost"].values
        demands_all_runs = group["demand"].values

        hour_utilities = {}

        for w in w_options:
            total_capacity = w * capacity_per_waggon

            actual_revenues = np.array([
                revs[total_capacity - 1] if len(revs) >= total_capacity
                else (revs[-1] if len(revs) > 0 else 0)
                for revs in revenues_all_runs
            ])

            w_costs = w * costs_all_runs

            passengers_in_train = np.minimum(total_capacity, demands_all_runs)
            passengers_per_waggon = passengers_in_train / w
            satisfaction_scores = v_satisfaction(passengers_per_waggon)
            dissatisfaction_penalty = lambda_param * (1 - (satisfaction_scores / 100))

            overflow_count = np.maximum(0, demands_all_runs - total_capacity)
            overflow_penalty = overflow_count * overflow_costs

            hour_utilities[w] = np.mean(actual_revenues - w_costs - dissatisfaction_penalty - overflow_penalty)
        
        utility_lookup[(day, hour)] = hour_utilities

    return utility_lookup

def find_best_switching_path(utility_lookup, w_options, cost_up, cost_down):
    optimized_data = []
    last_w = None

    for day, hour in sorted(utility_lookup.keys()):
        best_w = None
        max_path_utility = -float("inf")

        for w in w_options:
           base_utility = utility_lookup[(day, hour)][w]
           switching_penalty = calc_switching_costs(w, last_w, cost_up, cost_down)

           total_utility = base_utility - switching_penalty

           if total_utility > max_path_utility:
                max_path_utility = total_utility
                best_w = w
        
        optimized_data.append({
            "day": day,
            "hour": hour,
            "optimal_w": best_w,
            "expected_utility": max_path_utility,
            "last_w": last_w
        })

        last_w = best_w

    return pd.DataFrame(optimized_data)





import numpy as np
from model.demand import simulate_passenger_demand
from model.revenue import simulate_revenue
from model.cost import simulate_wagon_cost

def run_simulation(params):

    runs = params["runs"]

    results = []

    for d in range(1, 8):   # Weekdays (Mo-So)
        for h in range(6, 24):  # Hours (06:00-23:00)
            demand_arr = simulate_passenger_demand(d, h, size=runs)

            revenue_cum_arrays = [
                np.cumsum(simulate_revenue(int(n)))
                for n in demand_arr
            ]

            cost_arr = simulate_wagon_cost(size=runs)

            # store all runs
            for i in range(runs):
                results.append({
                    "day": d,
                    "hour": h,
                    "run": i,
                    "demand": demand_arr[i],
                    "revenue_cum_arr": revenue_cum_arrays[i],
                    "cost": cost_arr[i]
                })

    return results
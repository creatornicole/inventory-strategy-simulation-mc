import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from simulation.run_simulation import run_simulation
from optimization.run_optimization import find_optimal_waggons

params = {
    "runs": 100,
    "w_options": [1, 2, 3, 4],
    "capacity_per_waggon": 300,
    "lambda_param": 1000,
    "overflow_costs": 100,
    "cost_up": 300,
    "cost_down": 100
}

raw_data = run_simulation(params)

results = find_optimal_waggons(
    simulation_results=raw_data,
    w_options=params["w_options"],
    capacity_per_waggon=params["capacity_per_waggon"],
    lambda_param=params["lambda_param"],
    overflow_costs=params["overflow_costs"],
    cost_up=params["cost_up"],
    cost_down=params["cost_down"]
)

print(results.head())

df = pd.DataFrame(raw_data)

day = 7

subset = df[df["day"] == day]

for r in subset["run"].unique()[:200]:
    run_data = subset[subset["run"] == r]
    run_data = run_data.sort_values("hour")

    plt.plot(run_data["hour"], run_data["demand"], alpha=0.1)

plt.title(f"Demand trajectories - Day {day}")
plt.xlabel("Hour")
plt.ylabel("Demand")

plt.show()
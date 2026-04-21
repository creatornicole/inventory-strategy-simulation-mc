import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from simulation.run_simulation import run_simulation
from optimization.run_optimization import find_optimal_waggons

params = {
    "runs": 10000,
    "w_options": [1, 2, 3, 4],
    "capacity_per_waggon": 300,
    "lambda_param": 1000 
}

raw_data = run_simulation(params)

results = find_optimal_waggons(
    simulation_results=raw_data,
    w_options=params["w_options"],
    capacity_per_waggon=params["capacity_per_waggon"],
    lambda_param=params["lambda_param"]
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
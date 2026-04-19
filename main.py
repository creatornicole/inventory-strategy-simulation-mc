from simulation.run_simulation import run_simulation
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

params = {
    "runs": 100
}

results = run_simulation(params)

df = pd.DataFrame(results)

day = 1

subset = df[df["day"] == day]

for r in subset["run"].unique()[:200]:
    run_data = subset[subset["run"] == r]
    run_data = run_data.sort_values("hour")

    plt.plot(run_data["hour"], run_data["demand"], alpha=0.1)

plt.title(f"Demand trajectories - Day {day}")
plt.xlabel("Hour")
plt.ylabel("Demand")

plt.show()
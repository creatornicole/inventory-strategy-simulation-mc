import numpy as np

def get_demand(m, params):
    return (
        params["B"]
        + params["A"] * np.sin(2 * np.pi * m / 12)
        + np.random.normal(0, params["sigma"])
    )
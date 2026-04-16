import numpy as np

def get_price(m, params):
    return (
        params["P0"]
        + params["Ap"] * np.sin(2 * np.pi * m / 12)
        + np.random.normal(0, params["sigma_p"])
    )
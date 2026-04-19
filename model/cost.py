import numpy as np

def simulate_wagon_cost(mean=1200, std=300, size=1):
    return np.random.normal(
        loc=mean, 
        scale=std, 
        size=size)
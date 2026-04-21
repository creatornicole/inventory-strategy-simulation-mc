import numpy as np

def simulate_wagon_cost(mean=1200, std=300, size=1):
    return np.random.normal(
        loc=mean, 
        scale=std, 
        size=size)

def calc_switching_costs(current_w, last_w, cost_up=300, cost_down=100):
    if last_w is None or current_w == last_w:
        return 0
    
    diff = current_w - last_w
    if diff > 0:
        return diff * cost_up
    else:
        return abs(diff) * cost_down
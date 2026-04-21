import numpy as np

def simulate_revenue(n):
    # assign ticket type per passenger:
    # True = Deutschlandticket (80%)
    # False = single ticket for whole journey (20%)
    is_subscription = np.random.rand(n) < 0.8

    revenues = np.empty(n)

    U = np.random.normal(8.5, 2, n)
    U = np.maximum(U, 1)
    revenues = np.where(is_subscription, 63 / U, 23.10)

    return revenues
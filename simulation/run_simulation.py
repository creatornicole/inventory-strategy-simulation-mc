import numpy as np
from model.demand import get_demand
from model.price import get_price

def run_simulation(params, strategy):

    runs = params["runs"]

    # accumulators for plotting
    profit_sum = np.zeros(12)
    purchase_sum = np.zeros(12)
    storage_sum = np.zeros(12)
    overflow_sum = np.zeros(12)
    inventory_sum = np.zeros(12)
    service_sum = np.zeros(12)
    lost_sum = np.zeros(12)

    for _ in range(runs):
        inventory = params["initial_stock"]

        for m in range(12):
            
            # fuel is ordered at the beginning of the month based on the chosen strategy
            state = { "inventory": inventory, "month": m + 1}
            order = strategy(state, params)

            # if inventory is not enough, store fuel externally with costs that must be paid upfront for the upcoming month
            inventory = inventory + order
            overflow_cost = max(0, inventory - params["capacity"]) * params["overflow_penalty"]

            # estimate values
            demand = max(0, get_demand(m + 1, params)) # TODO: kann in Minus-Bereich gehen?
            price = max(0, get_price(m + 1, params)) # TODO: kann in Minus-Bereich gehen?

            sales = min(demand, inventory) # maximum of sales is inventory state
            lost = max(0, demand - inventory)

            inventory = inventory - sales

            revenue = sales * params["sell_price"]   
    
            purchase_cost = order * price
            # at the end of the month the storage cost come into play for the last month based on the current storage level
            storage_cost = min(inventory, params["capacity"]) * params["storage_cost"]
            total_cost = purchase_cost + storage_cost + overflow_cost

            profit = revenue - total_cost

            service = sales / demand if demand > 0 else 1

            # accumulate for plotting
            profit_sum[m] += profit
            purchase_sum[m] += purchase_cost
            storage_sum[m] += storage_cost
            overflow_sum[m] += overflow_cost
            inventory_sum[m] += inventory
            service_sum[m] += service
            lost_sum[m] += lost
    
    # return average values
    return {
        "profit": profit_sum / runs,
        "purchase_cost": purchase_sum / runs,
        "storage_cost": storage_sum / runs,
        "overflow_cost": overflow_sum / runs,
        "inventory": inventory_sum / runs,
        "service": service_sum / runs,
        "lost": lost_sum / runs
    }


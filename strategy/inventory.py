def inventory_strategy(state, params):
    if state["inventory"] < params["min_stock"]:
        return params["order_qty"]
    return 0
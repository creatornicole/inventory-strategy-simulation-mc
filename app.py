import streamlit as st
import numpy as np

from simulation.run_simulation import run_simulation
from strategy.static import static_strategy
from strategy.inventory import inventory_strategy
from ui.plots import plot_costs

# -------------------------
# Title
# -------------------------
st.title("Monte Carlo Inventory Simulation")

# -------------------------
# Controls
# -------------------------
strategy_name = st.selectbox(
    "Strategy (Single Mode only)",
    ["Static", "Inventory-Based"]
)

compare = st.checkbox("Compare Strategies (Static vs Inventory-Based)")

runs = st.number_input("Simulation runs", 1000, 20000, 10000)
order_qty = st.number_input("Order quantity", 100, 5000, 1000)
min_stock = st.number_input("Minimum stock", 0, 5000, 500)

# -------------------------
# Parameters
# -------------------------
params = {
    "runs": runs,
    "order_qty": order_qty,
    "min_stock": min_stock,

    # demand model
    "B": 1000,
    "A": 300,
    "sigma": 150,

    # price model
    "P0": 1.2,
    "Ap": 0.1,
    "sigma_p": 0.05,

    # economic parameters
    "sell_price": 1.6,
    "storage_cost": 0.05,
    "overflow_penalty": 0.2,

    # system constraints
    "capacity": 5000,
    "initial_stock": 1000
}

# -------------------------
# Session State Init
# -------------------------
if "results" not in st.session_state:
    st.session_state.results = None
if "results_static" not in st.session_state:
    st.session_state.results_static = None
if "results_inventory" not in st.session_state:
    st.session_state.results_inventory = None

# -------------------------
# Run Simulation
# -------------------------
if st.button("Run Simulation"):

    if compare:
        st.session_state.results_static = run_simulation(params, static_strategy)
        st.session_state.results_inventory = run_simulation(params, inventory_strategy)
        st.session_state.results = None
    else:
        strategy = static_strategy if strategy_name == "Static" else inventory_strategy
        st.session_state.results = run_simulation(params, strategy)
        st.session_state.results_static = None
        st.session_state.results_inventory = None

# -------------------------
# Guards (CRASH PREVENTION)
# -------------------------
if compare:
    if st.session_state.results_static is None or st.session_state.results_inventory is None:
        st.info("👉 Please run the simulation first.")
        st.stop()
else:
    if st.session_state.results is None:
        st.info("👉 Please run the simulation first.")
        st.stop()

# -------------------------
# Tabs
# -------------------------
tabs = st.tabs(["Profit", "Costs", "Inventory", "Service Level", "Lost Demand"])

results = st.session_state.results
results_s = st.session_state.results_static
results_i = st.session_state.results_inventory

# -------------------------
# TAB 1: Profit
# -------------------------
with tabs[0]:
    st.subheader("Profit")

    if compare:
        col1, col2 = st.columns(2)

        col1.subheader("Static")
        col1.line_chart(results_s["profit"])

        col2.subheader("Inventory-Based")
        col2.line_chart(results_i["profit"])
    else:
        st.line_chart(results["profit"])

# -------------------------
# TAB 2: Costs
# -------------------------
with tabs[1]:
    st.subheader("Costs")

    if compare:
        col1, col2 = st.columns(2)

        with col1:
            plot_costs(results_s, "Static")

        with col2:
            plot_costs(results_i, "Inventory-Based")

    else:
        plot_costs(results)

# -------------------------
# TAB 3: Inventory
# -------------------------
with tabs[2]:
    st.subheader("Inventory")

    if compare:
        col1, col2 = st.columns(2)

        col1.subheader("Static")
        col1.line_chart(results_s["inventory"])

        col2.subheader("Inventory-Based")
        col2.line_chart(results_i["inventory"])
    else:
        st.line_chart(results["inventory"])

# -------------------------
# TAB 4: Service Level
# -------------------------
with tabs[3]:
    st.subheader("Service Level")

    if compare:
        col1, col2 = st.columns(2)

        col1.subheader("Static")
        col1.line_chart(results_s["service"])

        col2.subheader("Inventory-Based")
        col2.line_chart(results_i["service"])
    else:
        st.line_chart(results["service"])

# -------------------------
# TAB 5: Lost Demand
# -------------------------
with tabs[4]:
    st.subheader("Lost Demand")

    if compare:
        col1, col2 = st.columns(2)

        col1.subheader("Static")
        col1.line_chart(results_s["lost"])

        col2.subheader("Inventory-Based")
        col2.line_chart(results_i["lost"])
    else:
        st.line_chart(results["lost"])
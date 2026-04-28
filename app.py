import streamlit as st
from simulation.run_simulation import run_simulation
from optimization.run_optimization import find_optimal_waggons
from config.input_config import CONFIG
from config.weekdays import WEEKDAYS
from ui.plots import plot_day_results

# -------------------------
# TITLE
# -------------------------
st.title("Monte Carlo Simulation")

# -------------------------
# INPUTS
# -------------------------
runs = st.number_input(
    CONFIG["runs"]["label"],
    min_value=CONFIG["runs"]["min"],
    max_value=CONFIG["runs"]["max"],
    value=CONFIG["runs"]["default"],
    step=CONFIG["runs"]["step"]
)

w_range = st.slider(
    CONFIG["w_range"]["label"],
    min_value=CONFIG["w_range"]["min"],
    max_value=CONFIG["w_range"]["max"],
    value=CONFIG["w_range"]["default"],
    step=CONFIG["w_range"]["step"]
)

lambda_param = st.number_input(
    CONFIG["lambda_param"]["label"],
    min_value=CONFIG["lambda_param"]["min"],
    max_value=CONFIG["lambda_param"]["max"],
    value=CONFIG["lambda_param"]["default"],
    step=CONFIG["lambda_param"]["step"],
    help=CONFIG["lambda_param"]["help"]
)

overflow_costs = st.number_input(
    CONFIG["overflow_costs"]["label"],
    min_value=CONFIG["overflow_costs"]["min"],
    max_value=CONFIG["overflow_costs"]["max"],
    value=CONFIG["overflow_costs"]["default"],
    step=CONFIG["overflow_costs"]["step"],
    help=CONFIG["overflow_costs"]["help"]
)

cost_up = st.number_input(
    CONFIG["cost_up"]["label"],
    min_value=CONFIG["cost_up"]["min"],
    max_value=CONFIG["cost_up"]["max"],
    value=CONFIG["cost_up"]["default"],
    step=CONFIG["cost_up"]["step"],
    help=CONFIG["cost_up"]["help"]
)

cost_down = st.number_input(
    CONFIG["cost_down"]["label"],
    min_value=CONFIG["cost_down"]["min"],
    max_value=CONFIG["cost_down"]["max"],
    value=CONFIG["cost_down"]["default"],
    step=CONFIG["cost_down"]["step"],
    help=CONFIG["cost_down"]["help"]
)

# -------------------------
# BUILD PARAMS
# -------------------------
params = {
    "runs": runs,
    "w_options": list(range(w_range[0], w_range[1] + 1)),
    "lambda_param": lambda_param,
    "overflow_costs": overflow_costs,
    "cost_up": cost_up,
    "cost_down": cost_down
}

# -------------------------
# RUN BUTTON
# -------------------------
if st.button("Starte Simulation"):
    with st.spinner("Berechne Simulation..."):
        raw_data = run_simulation(params)

    with st.spinner("Optimiere Waggonstrategie..."):
        results = find_optimal_waggons(
            simulation_results=raw_data,
            w_options=params["w_options"],
            capacity_per_waggon=300,
            lambda_param=params["lambda_param"],
            overflow_costs=params["overflow_costs"],
            cost_up=params["cost_up"],
            cost_down=params["cost_down"]
        )

    st.session_state.results = results

# -------------------------
# RESULTS
# -------------------------
if "results" in st.session_state:

    results = st.session_state.results

    days = sorted(results["day"].unique())

    tabs = st.tabs([WEEKDAYS.get(d, f"{d}") for d in days])

    for i, d in enumerate(days):

        with tabs[i]:
            st.subheader(f"Ergebnisse für {WEEKDAYS.get(d, d)}")

            df_day = results[results["day"] == d]

            all_util = results["expected_utility"]
            y_min = all_util.min()
            y_max = all_util.max()

            fig = plot_day_results(df_day, d, y_min, y_max)

            st.pyplot(fig)

            st.dataframe(df_day)
import streamlit as st

def plot_costs(results, title = "Cost Breakdown"):
    st.subheader(title)

    st.area_chart({
        "Purchase": results["purchase_cost"],
        "Storage": results["storage_cost"],
        "Overflow": results["overflow_cost"]
    })
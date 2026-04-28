import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from config.weekdays import WEEKDAYS

def plot_day_results(df_day, day, y_min=None, y_max=None):
    """
    Creates dual-axis plot:
        Bar: optimal_w
        Line: expected_utility
    """

    df_day = df_day.sort_values("hour")

    hours = df_day["hour"].values
    waggons = df_day["optimal_w"].values
    utility = df_day["expected_utility"].values

    fig, ax1 = plt.subplots()

    ax1.grid(True, linestyle="--", alpha=0.4)

    # -------------------------
    # Bar chart: Waggons
    # -------------------------
    ax1.bar(hours, waggons, alpha=0.7, color="#8da0cb")
    
    ax1.set_xlabel("Stunde")
    ax1.set_ylabel("Waggonanzahl")

    ax1.set_yticks(range(int(min(waggons)), int(max(waggons)) + 2))
    ax1.yaxis.set_major_locator(mticker.MaxNLocator(integer=True))
    ax1.xaxis.set_major_locator(mticker.MaxNLocator(integer=True))

    # -------------------------
    # Line chart: Utility
    # -------------------------
    ax2 = ax1.twinx()

    ax2.axhline(0, color="black", linewidth=1, linestyle="--", alpha=0.7)

    ax2.plot(hours, utility, color="#2b8cbe", linewidth=2)

    colors = ["#2ca25f" if u >= 0 else "#de2d26" for u in utility]

    ax2.scatter(
        hours,
        utility,
        c=colors,
        s=40,
        zorder=3
    )
    
    ax2.set_ylabel("Erwarteter Nutzen")

    if y_min is not None and y_max is not None:
        ax2.set_ylim(y_min - 100, y_max + 100)

    # -------------------------
    # Title
    # -------------------------
    plt.title(f"Waggonstrategie - {WEEKDAYS.get(day, day)}")

    fig.tight_layout()

    return fig
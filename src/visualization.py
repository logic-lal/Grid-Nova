
import matplotlib.pyplot as plt
import numpy as np


def plot_energy_summary(solar_energy,wind_energy,total_demand):

    plt.style.use("dark_background")

    fig,ax=plt.subplots(figsize=(10,6))

    labels=["Solar","Wind","Demand"]
    values=[solar_energy,wind_energy,total_demand]
    colors=["#facc15","#22d3ee","#fb7185"]

    bars=ax.bar(labels,values,color=colors,width=0.55)

    ax.set_title("E_SYNC | ENERGY OVERVIEW",fontsize=18,fontweight="bold",pad=20)
    ax.set_ylabel("Energy (kWh)",fontsize=12)

    ax.grid(axis="y",alpha=0.2)
    ax.set_axisbelow(True)

    for bar in bars:
        height=bar.get_height()
        ax.text(
            bar.get_x()+bar.get_width()/2,
            height+0.3,
            f"{height:.2f}",
            ha="center",
            fontsize=11
        )

    plt.tight_layout()
    plt.savefig("outputs/energy_summary.png",dpi=300)
    plt.show()


def plot_weekly_results(days,solar_values,wind_values,generation_values,demand_values,battery_days,battery_values):

    plt.style.use("dark_background")

    fig,axes=plt.subplots(3,1,figsize=(13,14))

    fig.patch.set_facecolor("#0f172a")

    for ax in axes:
        ax.set_facecolor("#111827")
        ax.grid(color="#475569",alpha=0.25,linestyle="--")
        ax.set_axisbelow(True)

        for spine in ax.spines.values():
            spine.set_color("#334155")

    fig.suptitle(
        "E_SYNC | SMART RENEWABLE ENERGY GRID",
        fontsize=21,
        fontweight="bold",
        color="white",
        y=0.99
    )

    # Graph 1: Solar and wind generation

    axes[0].plot(
        days,solar_values,
        color="#facc15",
        marker="o",
        linewidth=2.8,
        markersize=8,
        label="Solar"
    )

    axes[0].fill_between(
        days,solar_values,
        color="#facc15",
        alpha=0.12
    )

    axes[0].plot(
        days,wind_values,
        color="#22d3ee",
        marker="o",
        linewidth=2.8,
        markersize=8,
        label="Wind"
    )

    axes[0].fill_between(
        days,wind_values,
        color="#22d3ee",
        alpha=0.12
    )

    axes[0].set_title("DAILY ENERGY GENERATION",fontsize=10,fontweight="bold",pad=12)
    axes[0].set_ylabel("Energy (kWh)")
    axes[0].set_xlabel("Day",labelpad=8)
    axes[0].set_xticks(days)
    axes[0].legend(loc="upper right",frameon=False)

    # Graph 2: Battery state of charge

    axes[1].plot(
        battery_days,battery_values,
        color="#4ade80",
        marker="o",
        linewidth=3,
        markersize=8,
        label="Battery SOC"
    )

    axes[1].fill_between(
        battery_days,battery_values,
        color="#4ade80",
        alpha=0.15
    )

    axes[1].set_title("BATTERY STATE OF CHARGE",fontsize=14,fontweight="bold",pad=12)
    axes[1].set_ylabel("Battery Energy (kWh)")
    axes[1].set_xlabel("Day",labelpad=8)
    axes[1].set_xlim(0,7)
    axes[1].set_ylim(0,33)
    axes[1].set_xticks(range(8))
    axes[1].legend(loc="lower right",frameon=False)

    # Graph 3: Generation versus demand

    width=0.35

    axes[2].bar(
        np.array(days)-width/2,
        generation_values,
        width=width,
        color="#38bdf8",
        label="Generation"
    )

    axes[2].bar(
        np.array(days)+width/2,
        demand_values,
        width=width,
        color="#fb7185",
        label="Demand"
    )

    axes[2].set_title("GENERATION VS ELECTRICITY DEMAND",fontsize=14,fontweight="bold",pad=12)
    axes[2].set_ylabel("Energy (kWh)")
    axes[2].set_xlabel("Day",labelpad=8)
    axes[2].set_xticks(days)
    axes[2].legend(frameon=False)

   
    fig.subplots_adjust(
        left=0.08,
        right=0.97,
        top=0.93,
        bottom=0.07,
        hspace=0.55
    )

    plt.savefig(
        "outputs/weekly_summary.png",
        dpi=300,
        facecolor=fig.get_facecolor()
    )

    plt.show()

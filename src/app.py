"""
E_Sync

Intelligent Hybrid Renewable Energy Optimization and Simulation System

Run from the project root:
    python -m streamlit run src/app.py
"""

import os
import sys
import html
import math

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import streamlit as st
import matplotlib.pyplot as plt

from energy_sources.solar import calculate_solar_power, calculate_solar_energy
from energy_sources.wind import calculate_wind_power, calculate_wind_energy
from demand import calculate_demand
from battery import manage_battery
from linear_equation import gauss_elimination, gauss_jordan
from root_finding import bisection, false_position, newton_raphson


def daily_generation(irradiance, wind_speed, params):
    solar_power = calculate_solar_power(
        irradiance, params["panel_area"], params["solar_eff"]
    )
    solar_energy = calculate_solar_energy(solar_power, params["solar_hours"])
    wind_power = calculate_wind_power(
        wind_speed, params["blade_radius"], params["wind_eff"]
    )
    wind_energy = calculate_wind_energy(wind_power, params["wind_hours"])
    return solar_power, solar_energy, wind_power, wind_energy


def total_daily_demand(appliances):
    return sum(calculate_demand(power, hours, quantity)
               for _, power, hours, quantity in appliances)


def simulate_day(irradiance, wind_speed, params, demand, initial_soc=None):
    solar_power, solar, wind_power, wind = daily_generation(
        irradiance, wind_speed, params
    )
    generation = solar + wind
    starting_soc = params["initial_soc"] if initial_soc is None else initial_soc
    soc, charged, discharged, unserved = manage_battery(
        starting_soc, generation, demand, params["capacity"]
    )
    delivered = discharged * 0.95
    return {
        "solar_power": solar_power, "solar": solar,
        "wind_power": wind_power, "wind": wind,
        "generation": generation, "demand": demand,
        "soc": soc, "charged": charged, "discharged": discharged,
        "battery_delivered": delivered, "unserved": unserved,
    }


def html_table(headers, rows):
    header = "| " + " | ".join(str(h) for h in headers) + " |"
    separator = "| " + " | ".join(["---"] * len(headers)) + " |"

    table_rows = []
    for row in rows:
        formatted_row = "| " + " | ".join(str(value) for value in row) + " |"
        table_rows.append(formatted_row)

    table = "\n".join([header, separator] + table_rows)
    st.markdown(table)


def sidebar_inputs():
    st.sidebar.header("⚙️ System Configuration")
    st.sidebar.subheader("☀️ Solar System")
    panel_area = st.sidebar.number_input("Panel area (m²)", 1.0, 1000.0, 20.0, 1.0)
    solar_eff = st.sidebar.slider("Solar efficiency", 0.05, 0.50, 0.20, 0.01)
    solar_hours = st.sidebar.slider("Sunshine hours/day", 0.0, 24.0, 5.0, 0.5)

    st.sidebar.subheader("🌬️ Wind System")
    blade_radius = st.sidebar.number_input("Blade radius (m)", 0.5, 50.0, 2.0, 0.5)
    wind_eff = st.sidebar.slider("Wind efficiency", 0.05, 0.59, 0.40, 0.01)
    wind_hours = st.sidebar.slider("Wind operating hours/day", 0.0, 24.0, 24.0, 0.5)

    st.sidebar.subheader("🔋 Battery")
    capacity = st.sidebar.number_input("Battery capacity (kWh)", 1.0, 1000.0, 30.0, 1.0)
    initial_soc = st.sidebar.number_input(
        "Initial battery charge (kWh)", 0.0, float(capacity),
        min(10.0, float(capacity)), 0.5
    )

    st.sidebar.subheader("🏠 Appliance Demand")
    defaults = [
        ("Fridge", 150.0, 24.0, 1),
        ("Fans", 75.0, 8.0, 3),
        ("Lights", 10.0, 6.0, 5),
        ("TV", 100.0, 4.0, 1),
    ]
    appliances = []
    for name, p0, h0, q0 in defaults:
        with st.sidebar.expander(name):
            power = st.number_input(f"{name} power (W)", 0.0, 100000.0, p0, 5.0, key=f"{name}_power")
            hours = st.number_input(f"{name} use (hours/day)", 0.0, 24.0, h0, 0.5, key=f"{name}_hours")
            qty = st.number_input(f"{name} quantity", 0, 1000, q0, 1, key=f"{name}_qty")
        appliances.append((name, power, hours, qty))

    params = {
        "panel_area": panel_area, "solar_eff": solar_eff,
        "solar_hours": solar_hours, "blade_radius": blade_radius,
        "wind_eff": wind_eff, "wind_hours": wind_hours,
        "capacity": capacity, "initial_soc": initial_soc,
    }
    return params, appliances


def plot_daily(result):
    plt.style.use("dark_background")

    fig, ax = plt.subplots(figsize=(10, 6))
    fig.patch.set_facecolor("#0f172a")
    ax.set_facecolor("#111827")

    labels = ["Solar", "Wind", "Demand"]
    values = [result["solar"], result["wind"], result["demand"]]
    colors = ["#facc15", "#22d3ee", "#fb7185"]

    bars = ax.bar(labels, values, color=colors, width=0.55)
    ax.set_title("E_SYNC | ENERGY OVERVIEW", fontsize=18, fontweight="bold", pad=20, color="white")
    ax.set_ylabel("Energy (kWh)", fontsize=12, color="white")
    ax.grid(axis="y", color="#475569", alpha=0.25, linestyle="--")
    ax.set_axisbelow(True)

    for spine in ax.spines.values():
        spine.set_color("#334155")

    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, height + 0.3, f"{height:.2f}",
                ha="center", fontsize=11, color="white")

    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)


def daily_tab(params, demand):
    st.subheader("☀️ Daily Simulation")

    c1, c2 = st.columns(2)
    irradiance = c1.slider("Solar irradiance (W/m²)", 0, 1500, 800, 10)
    wind_speed = c2.slider("Wind speed (m/s)", 0.0, 40.0, 8.0, 0.5)
    result = simulate_day(irradiance, wind_speed, params, demand)

    st.markdown("#### Generation")
    cols = st.columns(4)
    cols[0].metric("Solar energy", f'{result["solar"]:.2f} kWh')
    cols[1].metric("Wind energy", f'{result["wind"]:.2f} kWh')
    cols[2].metric("Total generation", f'{result["generation"]:.2f} kWh')
    cols[3].metric("Daily demand", f'{demand:.2f} kWh')

    st.markdown("#### Battery & Energy Balance")
    cols = st.columns(4)
    cols[0].metric("Battery remaining", f'{result["soc"]:.2f} kWh')
    cols[1].metric("Energy stored", f'{result["charged"]:.2f} kWh')
    cols[2].metric("Battery delivered", f'{result["battery_delivered"]:.2f} kWh')
    cols[3].metric("Unserved demand", f'{result["unserved"]:.2f} kWh')

    if result["generation"] >= demand:
        st.success(f"Renewable generation covers demand. Surplus before battery charging: {result['generation']-demand:.2f} kWh.")
    else:
        st.warning(f"Renewable generation is below demand by {demand-result['generation']:.2f} kWh before battery support.")
    plot_daily(result)


def weekly_tab(params, demand):
    st.subheader("📅 Seven-Day Simulation")

    defaults = [(800, 8.0), (300, 4.0), (200, 3.0), (900, 10.0),
                (400, 5.0), (150, 2.0), (700, 7.0)]
    rows = []
    daily_results = []
    soc = params["initial_soc"]

    for day, (irr0, wind0) in enumerate(defaults, 1):
        with st.expander(f"Day {day} input", expanded=(day == 1)):
            a, b = st.columns(2)
            irr = a.number_input(f"Solar irradiance (W/m²) — Day {day}", 0, 1500, irr0, 10, key=f"week_irr_{day}")
            wind = b.number_input(f"Wind speed (m/s) — Day {day}", 0.0, 40.0, wind0, 0.5, key=f"week_wind_{day}")

        result = simulate_day(irr, wind, params, demand, soc)
        soc = result["soc"]
        daily_results.append(result)
        rows.append([
            day, f'{result["solar"]:.2f}', f'{result["wind"]:.2f}',
            f'{result["generation"]:.2f}', f'{demand:.2f}',
            f'{result["battery_delivered"]:.2f}', f'{soc:.2f}',
            f'{result["unserved"]:.2f}'
        ])

    st.markdown("#### Weekly Results")
    html_table(
        ["Day", "Solar (kWh)", "Wind (kWh)", "Generation (kWh)",
         "Demand (kWh)", "Battery delivered (kWh)", "Battery SoC (kWh)",
         "Unserved (kWh)"], rows
    )

    total_gen = sum(r["generation"] for r in daily_results)
    total_demand = sum(r["demand"] for r in daily_results)
    total_unserved = sum(r["unserved"] for r in daily_results)
    m = st.columns(4)
    m[0].metric("Weekly generation", f"{total_gen:.2f} kWh")
    m[1].metric("Weekly demand", f"{total_demand:.2f} kWh")
    m[2].metric("Final battery", f"{soc:.2f} kWh")
    m[3].metric("Unserved demand", f"{total_unserved:.2f} kWh")

    plt.style.use("dark_background")
    days = list(range(1, 8))
    solar_values = [r["solar"] for r in daily_results]
    wind_values = [r["wind"] for r in daily_results]
    generation_values = [r["generation"] for r in daily_results]
    demand_values = [r["demand"] for r in daily_results]

    fig, axes = plt.subplots(1, 3, figsize=(20, 6))
    fig.patch.set_facecolor("#0f172a")

    ax = axes[0]
    ax.set_facecolor("#111827")
    ax.plot(days, solar_values, color="#facc15", marker="o", linewidth=2.8, markersize=8, label="Solar")
    ax.plot(days, wind_values, color="#22d3ee", marker="o", linewidth=2.8, markersize=8, label="Wind")
    ax.fill_between(days, solar_values, color="#facc15", alpha=0.12)
    ax.fill_between(days, wind_values, color="#22d3ee", alpha=0.12)
    ax.set_title("DAILY ENERGY GENERATION", fontsize=12, fontweight="bold", color="white")
    ax.set_xlabel("Day")
    ax.set_ylabel("Energy (kWh)")
    ax.set_xticks(days)
    ax.grid(True, color="#475569", alpha=0.25, linestyle="--")
    ax.legend()

    ax = axes[1]
    ax.set_facecolor("#111827")
    battery_days = list(range(8))
    battery_values = [params["initial_soc"]] + [r["soc"] for r in daily_results]
    ax.plot(battery_days, battery_values, color="#4ade80", marker="o", linewidth=3, markersize=8, label="Battery SoC")
    ax.fill_between(battery_days, battery_values, color="#4ade80", alpha=0.15)
    ax.set_title("BATTERY STATE OF CHARGE", fontsize=12, fontweight="bold", color="white")
    ax.set_xlabel("Day")
    ax.set_ylabel("Battery SoC (kWh)")
    ax.set_xticks(battery_days)
    ax.set_xlim(0, 7)
    ax.set_ylim(0, max(float(params["capacity"]) * 1.1, 1))
    ax.grid(True, color="#475569", alpha=0.25, linestyle="--")
    ax.legend()

    ax = axes[2]
    ax.set_facecolor("#111827")
    width = 0.35
    generation_positions = [day - width / 2 for day in days]
    demand_positions = [day + width / 2 for day in days]
    ax.bar(generation_positions, generation_values, width=width, color="#38bdf8", label="Generation")
    ax.bar(demand_positions, demand_values, width=width, color="#fb7185", label="Demand")
    ax.set_title("GENERATION VS ELECTRICITY DEMAND", fontsize=12, fontweight="bold", color="white")
    ax.set_xlabel("Day")
    ax.set_ylabel("Energy (kWh)")
    ax.set_xticks(days)
    ax.grid(axis="y", color="#475569", alpha=0.25, linestyle="--")
    ax.set_axisbelow(True)
    ax.legend()

    for ax in axes:
        for spine in ax.spines.values():
            spine.set_color("#334155")
        ax.tick_params(colors="white")
        ax.xaxis.label.set_color("white")
        ax.yaxis.label.set_color("white")

    fig.suptitle("E_SYNC | SMART RENEWABLE ENERGY GRID", fontsize=17, fontweight="bold", color="white")
    fig.tight_layout(rect=[0, 0, 1, 0.93])
    st.pyplot(fig)
    plt.close(fig)

    st.session_state["weekly_results"] = daily_results


def solve_root_methods(target_energy, params, tolerance):
    """Find wind speed whose calculated daily wind energy equals target_energy using root_finding.py."""
    def f(speed):
        power = calculate_wind_power(speed, params["blade_radius"], params["wind_eff"])
        return calculate_wind_energy(power, params["wind_hours"]) - target_energy

    def derivative(speed):
        constant = (0.5 * 1.225 * math.pi * params["blade_radius"]**2
                    * params["wind_eff"] * params["wind_hours"]) / 1000
        return 3 * constant * speed**2

    a, b = 0.0, 40.0
    if f(a) * f(b) > 0:
        return None, "Target is outside the wind-energy range for speeds 0–40 m/s."

    results = {}

    # 1. Bisection Method (imported from root_finding.py)
    root1, it1 = bisection(f, a, b, tolerance)
    if root1 is not None:
        results["Bisection"] = (root1, it1, abs(f(root1)))

    # 2. False Position Method (imported from root_finding.py)
    root2, it2 = false_position(f, a, b, tolerance)
    if root2 is not None:
        results["False Position"] = (root2, it2, abs(f(root2)))

    # 3. Newton-Raphson Method (imported from root_finding.py)
    root3, it3 = newton_raphson(f, derivative, 8.0, tolerance)
    if root3 is not None:
        results["Newton-Raphson"] = (root3, it3, abs(f(root3)))

    if not results:
        return None, "Methods failed to converge."

    return results, None


def numerical_methods_tab(params, demand):
    st.subheader("🧮 Numerical Methods Lab")
    st.write("Use root-finding methods to estimate the wind speed needed to reach a selected daily wind-energy target.")

    target = st.number_input("Target wind energy (kWh/day)", min_value=0.0, max_value=100000.0, value=20.0, step=1.0)
    tolerance = st.select_slider("Tolerance", options=[0.1, 0.01, 0.001, 0.0001, 0.00001], value=0.0001)

    if st.button("Calculate required wind speed", type="primary"):
        results, error = solve_root_methods(target, params, tolerance)
        if error:
            st.warning(error)
        else:
            html_table(["Method", "Estimated wind speed (m/s)", "Iterations", "Residual (kWh)"], [
                [name, f"{value[0]:.6f}", value[1], f"{value[2]:.8f}"]
                for name, value in results.items()
            ])
            st.caption("Residual = |calculated wind energy − target wind energy|. Results are numerical approximations.")

    st.divider()
    st.write("**Euler and Modified Euler: simplified battery state prediction**")
    st.caption("This teaching model assumes a constant net-energy rate over the selected period and limits the predicted charge to the battery's physical range.")

    start_soc = st.number_input("Starting SoC (kWh)", 0.0, float(params["capacity"]), min(float(params["initial_soc"]), float(params["capacity"])), 0.5)
    net_rate = st.number_input("Net battery energy rate (kWh/hour; + charge, − discharge)", -100.0, 100.0, 0.5, 0.1)
    duration = st.number_input("Prediction duration (hours)", 0.5, 24.0, 4.0, 0.5)
    step = st.select_slider("Time step (hours)", options=[0.1, 0.25, 0.5, 1.0], value=0.5)
    cap = float(params["capacity"])

    def rate(_t, soc):
        if net_rate >= 0:
            return net_rate * max(0.0, 1.0 - soc/cap)
        return net_rate * max(0.0, soc/cap)

    def integrate(method):
        t, y = 0.0, float(start_soc)
        points = [(t, y)]
        while t < duration - 1e-12:
            h = min(step, duration-t)
            k1 = rate(t, y)
            if method == "Euler":
                y_next = y + h*k1
            else:
                predictor = max(0.0, min(cap, y+h*k1))
                k2 = rate(t+h, predictor)
                y_next = y + (h/2)*(k1+k2)
            y = max(0.0, min(cap, y_next))
            t += h
            points.append((t, y))
        return points

    euler = integrate("Euler")
    modified = integrate("Modified Euler")
    c1, c2 = st.columns(2)
    c1.metric("Euler predicted SoC", f"{euler[-1][1]:.3f} kWh")
    c2.metric("Modified Euler predicted SoC", f"{modified[-1][1]:.3f} kWh")

    fig, ax = plt.subplots()
    ax.plot([p[0] for p in euler], [p[1] for p in euler], marker="o", label="Euler")
    ax.plot([p[0] for p in modified], [p[1] for p in modified], marker="s", label="Modified Euler")
    ax.set(xlabel="Time (hours)", ylabel="Battery SoC (kWh)", title="Numerical Battery SoC Prediction")
    ax.set_ylim(0, cap*1.05)
    ax.grid(True, alpha=0.25)
    ax.legend()
    st.pyplot(fig)
    plt.close(fig)


def allocation_tab():
    st.subheader("Linear System Solver — Gauss Methods")
    st.info("Enter a 3×3 linear system and its right-hand-side values. Both methods solve the same system independently.")
    st.latex(r"\mathbf{A}\mathbf{x}=\mathbf{b}")

    defaults = [[2.0, 1.0, -1.0], [-3.0, -1.0, 2.0], [-2.0, 1.0, 2.0]]
    rhs_defaults = [8.0, -11.0, -3.0]
    matrix, rhs = [], []
    for i in range(3):
        cols = st.columns(4)
        row = [cols[j].number_input(f"a{i+1}{j+1}", -1000.0, 1000.0, defaults[i][j], 0.5, key=f"linear_a_{i}_{j}") for j in range(3)]
        matrix.append(row)
        rhs.append(cols[3].number_input(f"b{i+1}", -10000.0, 10000.0, rhs_defaults[i], 0.5, key=f"linear_b_{i}"))

    augmented = [matrix[i] + [rhs[i]] for i in range(3)]
    st.write("Augmented matrix [A | b]")
    html_table(["x", "y", "z", "RHS"], [[f"{v:.4f}" for v in row] for row in augmented])

    if st.button("Solve using Gauss methods", type="primary"):
        outcomes = []
        for label, solver in [("Gauss Elimination", gauss_elimination), ("Gauss-Jordan", gauss_jordan)]:
            try:
                answer = solver([row[:] for row in augmented])
                if answer is None:
                    st.warning(f"{label}: no unique solution (singular matrix).")
                else:
                    outcomes.append([label, *(f"{v:.6f}" for v in answer)])
            except (ValueError, ZeroDivisionError, IndexError, TypeError) as exc:
                st.error(f"{label} failed: {exc}")
        if outcomes:
            html_table(["Method", "x", "y", "z"], outcomes)


def main():
    st.set_page_config(page_title="va", page_icon="⚡", layout="wide")
    st.title("⚡ E_Sync")
    st.subheader("Intelligent Hybrid Renewable Energy Optimization and Simulation System")
    st.caption("Explore solar and wind generation, household demand, battery storage, and numerical methods through interactive simulations.")

    params, appliances = sidebar_inputs()
    demand = total_daily_demand(appliances)
    st.sidebar.metric("Total daily demand", f"{demand:.2f} kWh")

    daily, weekly, numerical, linear = st.tabs([
        "☀️ Daily Simulation", "📅 Weekly Simulation",
        "🧮 Numerical Methods", "📐 Linear System Solver"
    ])
    with daily:
        daily_tab(params, demand)
    with weekly:
        weekly_tab(params, demand)
    with numerical:
        numerical_methods_tab(params, demand)
    with linear:
        allocation_tab()

    st.divider()
    st.caption("E_Sync | Educational simulation — results depend on the simplified physical and battery models used in this project.")


if __name__ == "__main__":
    main()
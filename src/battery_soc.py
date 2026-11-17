
import math
import os
import matplotlib.pyplot as plt


# Project settings
solar_total=16.0
wind_total=37.83
demand_total=6.10

initial_soc=10
capacity=30

charge_efficiency=0.95
discharge_efficiency=0.95

simulation_hours=24
h=0.25


# Generate hourly solar power profile
solar_profile=[]

for t in range(25):

    if 6<=t<=18:
        power=math.sin(math.pi*(t-6)/12)
    else:
        power=0

    solar_profile.append(power)


# Generate hourly wind power profile
wind_profile=[]

for t in range(25):

    if 6<=t<=20:
        power=0.2+math.sin(math.pi*(t-6)/14)
    else:
        power=0.02

    wind_profile.append(power)


# Generate hourly demand profile
demand_profile=[]

for t in range(25):

    power=0.15

    if 6<=t<=9:
        power+=0.15

    if 18<=t<=22:
        power+=0.25

    demand_profile.append(power)


# Calculate daily energy using trapezoidal integration
def calculate_energy(profile):

    total=0

    for i in range(len(profile)-1):
        total+=(profile[i]+profile[i+1])/2

    return total


# Scale profiles to match project energy values
def scale_profile(profile,target):

    total=calculate_energy(profile)

    return [value*target/total for value in profile]


solar_profile=scale_profile(solar_profile,solar_total)
wind_profile=scale_profile(wind_profile,wind_total)
demand_profile=scale_profile(demand_profile,demand_total)


# Find power at any time using linear interpolation
def get_power(profile,t):

    if t<=0:
        return profile[0]

    if t>=24:
        return profile[24]

    index=int(t)
    fraction=t-index

    return profile[index]+fraction*(profile[index+1]-profile[index])


# Battery differential equation
def battery_rate(t,soc):

    solar=get_power(solar_profile,t)
    wind=get_power(wind_profile,t)
    demand=get_power(demand_profile,t)

    generation=solar+wind

    if generation>demand:

        if soc>=capacity:
            return 0

        return (generation-demand)*charge_efficiency

    elif generation<demand:

        if soc<=0:
            return 0

        return -(demand-generation)/discharge_efficiency

    return 0


# Euler Method
def euler_method(f,t0,y0,h,t_end):

    t=t0
    y=y0

    results=[(t,y)]

    while t<t_end-1e-9:

        step=min(h,t_end-t)

        slope=f(t,y)

        y=y+step*slope

        y=max(0,min(y,capacity))

        t=t+step

        results.append((t,y))

    return results


# Modified Euler Method
def modified_euler(f,t0,y0,h,t_end):

    t=t0
    y=y0

    results=[(t,y)]

    while t<t_end-1e-9:

        step=min(h,t_end-t)

        k1=f(t,y)

        predicted_y=y+step*k1
        predicted_y=max(0,min(predicted_y,capacity))

        k2=f(t+step,predicted_y)

        y=y+(step/2)*(k1+k2)

        y=max(0,min(y,capacity))

        t=t+step

        results.append((t,y))

    return results


# Run both numerical methods
euler_results=euler_method(
    battery_rate,0,initial_soc,h,simulation_hours
)

modified_results=modified_euler(
    battery_rate,0,initial_soc,h,simulation_hours
)


# Extract results
time_values=[item[0] for item in euler_results]

euler_soc=[item[1] for item in euler_results]

modified_soc=[item[1] for item in modified_results]


# Compare numerical methods
differences=[]

for i in range(len(euler_results)):

    difference=abs(
        euler_results[i][1]-modified_results[i][1]
    )

    differences.append(difference)


max_difference=max(differences)

final_difference=abs(
    euler_results[-1][1]-modified_results[-1][1]
)


# Display project information
print("========== HOURLY BATTERY SOC ANALYSIS ==========")

print("Total Solar Energy:",round(calculate_energy(solar_profile),2),"kWh")
print("Total Wind Energy:",round(calculate_energy(wind_profile),2),"kWh")
print("Total Demand:",round(calculate_energy(demand_profile),2),"kWh")


print("\nEULER METHOD")
print("Final Battery SOC:",round(euler_results[-1][1],2),"kWh")


print("\nMODIFIED EULER METHOD")
print("Final Battery SOC:",round(modified_results[-1][1],2),"kWh")


# Display results at two-hour intervals
print("\nTIME | EULER SOC | MODIFIED EULER SOC")

for i in range(0,len(euler_results),8):

    t=euler_results[i][0]
    euler_value=euler_results[i][1]
    modified_value=modified_results[i][1]

    print(
        round(t,2),"|",
        round(euler_value,2),"|",
        round(modified_value,2)
    )


# Display numerical comparison
print("\n========== METHOD COMPARISON ==========")

print("Euler Final SOC:",round(euler_results[-1][1],4),"kWh")
print("Modified Euler Final SOC:",round(modified_results[-1][1],4),"kWh")
print("Maximum Difference:",round(max_difference,6),"kWh")
print("Final Difference:",round(final_difference,6),"kWh")


# Create output folder if it does not exist
os.makedirs("outputs",exist_ok=True)


# Create advanced battery SOC comparison graph
fig,(ax1,ax2)=plt.subplots(
    2,1,
    figsize=(13,9),
    sharex=True,
    gridspec_kw={"height_ratios":[3,1]}
)

fig.patch.set_facecolor("#101820")

for ax in (ax1,ax2):

    ax.set_facecolor("#17232f")

    ax.tick_params(colors="white")

    ax.xaxis.label.set_color("white")
    ax.yaxis.label.set_color("white")

    for spine in ax.spines.values():
        spine.set_color("#526575")

    ax.grid(
        color="#526575",
        alpha=0.3,
        linestyle="--"
    )


# Main SOC graph
ax1.plot(
    time_values,euler_soc,
    color="#00d4ff",
    linewidth=2.8,
    label="Euler Method"
)

ax1.plot(
    time_values,modified_soc,
    color="#ff9f43",
    linewidth=2.8,
    label="Modified Euler Method"
)

ax1.fill_between(
    time_values,euler_soc,modified_soc,
    color="#a78bfa",
    alpha=0.35,
    label="Method Difference"
)

ax1.axhline(
    y=capacity,
    color="#ff4d6d",
    linestyle="--",
    linewidth=2,
    label="Maximum Battery Capacity"
)

ax1.axhline(
    y=initial_soc,
    color="#2ecc71",
    linestyle=":",
    alpha=0.8,
    label="Initial SOC"
)

ax1.set_title(
    "E_SYNC | BATTERY PERFORMANCE ANALYSIS",
    fontsize=17,
    fontweight="bold",
    color="white",
    pad=18
)

ax1.set_ylabel("Battery SOC (kWh)",fontsize=12)

ax1.set_xlim(0,24)
ax1.set_ylim(0,capacity+5)

ax1.legend(
    facecolor="#243447",
    edgecolor="#526575",
    labelcolor="white",
    loc="lower right"
)


# Numerical difference graph
ax2.plot(
    time_values,differences,
    color="#c084fc",
    linewidth=2.3,
    label="Absolute Difference"
)

ax2.fill_between(
    time_values,differences,
    color="#c084fc",
    alpha=0.25
)

max_index=differences.index(max_difference)

ax2.scatter(
    time_values[max_index],
    max_difference,
    color="#ff4d6d",
    s=65,
    zorder=5,
    label="Maximum Difference"
)

ax2.set_xlabel("Time (Hours)",fontsize=12)
ax2.set_ylabel("Difference (kWh)",fontsize=11)

ax2.legend(
    facecolor="#243447",
    edgecolor="#526575",
    labelcolor="white"
)


# Overall title
fig.suptitle(
    "Euler vs Modified Euler",
    fontsize=11,
    color="#aab8c5",
    y=0.96
)
ax1.set_xlim(0,24)
ax1.set_ylim(0,35)

ax2.set_xlim(0,24)
ax2.set_ylim(bottom=0)
plt.tight_layout(rect=[0,0,1,0.95])


# Save graph
plt.savefig(
    "outputs/battery_soc_comparison.png",
    dpi=300,
    facecolor=fig.get_facecolor(),
    bbox_inches="tight"
)

plt.show()

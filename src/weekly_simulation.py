
from energy_sources.solar import calculate_solar_power,calculate_solar_energy
from energy_sources.wind import calculate_wind_power,calculate_wind_energy
from demand import calculate_demand
from battery import manage_battery
from visualization import plot_weekly_results


def run_weekly_simulation(show_output=True,show_plot=True):

    irradiance_values=[800,300,200,900,400,150,700]
    wind_speed_values=[8,4,3,10,5,2,7]

    solar_hours=5
    wind_hours=24

    panel_area=20
    solar_efficiency=0.20

    blade_radius=2
    wind_efficiency=0.40

    capacity=30
    soc=10

    fridge=calculate_demand(150,24,1)
    fans=calculate_demand(75,8,3)
    lights=calculate_demand(10,6,5)
    tv=calculate_demand(100,4,1)

    daily_demand=fridge+fans+lights+tv

    total_generation_week=0
    total_demand_week=0
    total_unserved_week=0

    days=[]
    solar_values=[]
    wind_values=[]
    generation_values=[]
    demand_values=[]

    battery_days=[0]
    battery_values=[soc]

    daily_results=[]

    if show_output:
        print("========== E_SYNC 7 DAY SIMULATION ==========")
        print("Day | Solar | Wind | Generation | Demand | Battery | Unserved")

    for day in range(7):

        solar_power=calculate_solar_power(
            irradiance_values[day],panel_area,solar_efficiency
        )

        solar_energy=calculate_solar_energy(solar_power,solar_hours)

        wind_power=calculate_wind_power(
            wind_speed_values[day],blade_radius,wind_efficiency
        )

        wind_energy=calculate_wind_energy(wind_power,wind_hours)

        total_generation=solar_energy+wind_energy

        soc,charged,discharged,unserved=manage_battery(
            soc,total_generation,daily_demand,capacity
        )

        battery_delivered=max(0,daily_demand-total_generation)-unserved

        daily_results.append({
            "day":day+1,
            "solar":solar_energy,
            "wind":wind_energy,
            "generation":total_generation,
            "demand":daily_demand,
            "battery_delivered":battery_delivered,
            "battery_soc":soc,
            "unserved":unserved
        })

        days.append(day+1)
        solar_values.append(solar_energy)
        wind_values.append(wind_energy)
        generation_values.append(total_generation)
        demand_values.append(daily_demand)

        battery_days.append(day+1)
        battery_values.append(soc)

        total_generation_week+=total_generation
        total_demand_week+=daily_demand
        total_unserved_week+=unserved

        if show_output:
            print(
                day+1,
                "|",round(solar_energy,2),
                "|",round(wind_energy,2),
                "|",round(total_generation,2),
                "|",round(daily_demand,2),
                "|",round(soc,2),
                "|",round(unserved,2)
            )

    if show_output:
        print("\n========== WEEKLY SUMMARY ==========")

        print("Total Generation:",round(total_generation_week,2),"kWh")
        print("Total Demand:",round(total_demand_week,2),"kWh")
        print("Final Battery:",round(soc,2),"kWh")
        print("Total Unserved Demand:",round(total_unserved_week,2),"kWh")

    if show_plot:
        plot_weekly_results(
            days,solar_values,wind_values,
            generation_values,demand_values,
            battery_days,battery_values
        )

    return daily_results


if __name__=="__main__":
    run_weekly_simulation()

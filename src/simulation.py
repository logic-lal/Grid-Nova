
from energy_sources.solar import calculate_solar_power
from energy_sources.solar import calculate_solar_energy
from energy_sources.wind import calculate_wind_power
from energy_sources.wind import calculate_wind_energy
from demand import calculate_demand
from battery import manage_battery
from visualization import plot_energy_summary


def run_simulation():

    irradiance=800
    panel_area=20
    solar_efficiency=0.20

    wind_speed=8
    blade_radius=2
    wind_efficiency=0.40

    solar_hours=5
    wind_hours=24

    solar_power=calculate_solar_power(irradiance,panel_area,solar_efficiency)
    solar_energy=calculate_solar_energy(solar_power,solar_hours)

    wind_power=calculate_wind_power(wind_speed,blade_radius,wind_efficiency)
    wind_energy=calculate_wind_energy(wind_power,wind_hours)

    total_generation=solar_energy+wind_energy

    fridge=calculate_demand(150,24,1)
    fans=calculate_demand(75,8,3)
    lights=calculate_demand(10,6,5)
    tv=calculate_demand(100,4,1)

    total_demand=fridge+fans+lights+tv

    capacity=30
    soc=10

    soc,charged,discharged,unserved=manage_battery(
        soc,total_generation,total_demand,capacity
    )

    print("========== E_SYNC GRID SIMULATION ==========")

    print("\nSOLAR GENERATION")
    print("Solar Power:",round(solar_power,2),"kW")
    print("Solar Energy:",round(solar_energy,2),"kWh")

    print("\nWIND GENERATION")
    print("Wind Power:",round(wind_power,2),"kW")
    print("Wind Energy:",round(wind_energy,2),"kWh")

    print("\nENERGY BALANCE")
    print("Total Generation:",round(total_generation,2),"kWh")
    print("Total Demand:",round(total_demand,2),"kWh")
    print("Energy Balance:",round(total_generation-total_demand,2),"kWh")

    print("\nBATTERY STATUS")
    print("Battery Capacity:",capacity,"kWh")
    print("Initial Battery:",10,"kWh")
    print("Energy Stored:",round(charged,2),"kWh")
    print("Energy Discharged:",round(discharged,2),"kWh")
    print("Remaining Battery:",round(soc,2),"kWh")
    print("Unserved Demand:",round(unserved,2),"kWh")
    plot_energy_summary(solar_energy,wind_energy,total_demand)
    
    



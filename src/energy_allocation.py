
from linear_equation import gauss_elimination,gauss_jordan
from weekly_simulation import run_weekly_simulation


def run_energy_allocation():

    weekly_data=run_weekly_simulation(
        show_output=False,
        show_plot=False
    )

    print("========== ENERGY ALLOCATION SYSTEM ==========")
    print("\nAvailable simulation days: 1-7")

    try:
        day_number=int(input("\nSelect a day (1-7): "))

        if day_number<1 or day_number>7:
            print("Invalid day. Please select between 1 and 7.")
            return

    except ValueError:
        print("Invalid input. Please enter a number.")
        return

    day_data=weekly_data[day_number-1]

    solar=day_data["solar"]
    wind=day_data["wind"]
    battery=day_data["battery_delivered"]
    demand=day_data["demand"]

    renewable_generation=solar+wind
    total_available=renewable_generation+battery
    renewable_used=min(renewable_generation,demand)
    total_supplied=renewable_used+battery

    surplus=max(0,renewable_generation-demand)
    shortage=max(0,demand-renewable_generation)

    coefficients=[
        [0.7,0.2,0.1],
        [0.3,0.5,0.4],
        [0.0,0.3,0.5]
    ]

    A=[]
    B=[]

    for row in coefficients:
        total=row[0]*solar+row[1]*wind+row[2]*battery
        A.append(row+[total])
        B.append(row+[total])

    def display_value(value):
        value=round(value,2)
        if abs(value)<0.005:
            return 0.0
        return value

    print("\n========== DAY",day_number,"ENERGY BREAKDOWN ==========")

    print("\nENERGY GENERATION")
    print("Solar Generation:",display_value(solar),"kWh")
    print("Wind Generation:",display_value(wind),"kWh")
    print("Total Renewable Generation:",display_value(renewable_generation),"kWh")

    print("\nBATTERY")
    print("Battery Energy Delivered:",display_value(battery),"kWh")

    print("\nENERGY BALANCE")
    print("Total Energy Available:",display_value(total_available),"kWh")
    print("Energy Supplied to Demand:",display_value(total_supplied),"kWh")
    print("Daily Demand:",display_value(demand),"kWh")
    print("Renewable Surplus Before Battery Charging:",display_value(surplus),"kWh")
    print("Generation Shortage Before Battery Support:",display_value(shortage),"kWh")

    print("\n========== GAUSS ELIMINATION ==========")

    result1=gauss_elimination(A)

    if result1 is not None:
        print("Solar Contribution:",display_value(result1[0]),"kWh")
        print("Wind Contribution:",display_value(result1[1]),"kWh")
        print("Battery Contribution:",display_value(result1[2]),"kWh")
        print("Reconstructed Total:",display_value(sum(result1)),"kWh")

    print("\n========== GAUSS-JORDAN METHOD ==========")

    result2=gauss_jordan(B)

    if result2 is not None:
        print("Solar Contribution:",display_value(result2[0]),"kWh")
        print("Wind Contribution:",display_value(result2[1]),"kWh")
        print("Battery Contribution:",display_value(result2[2]),"kWh")
        print("Reconstructed Total:",display_value(sum(result2)),"kWh")


if __name__=="__main__":
    run_energy_allocation()


import math

def calculate_wind_power(wind_speed,blade_radius,efficiency):

    air_density=1.225
    area=math.pi*blade_radius**2

    power=(0.5*air_density*area*wind_speed**3*efficiency)/1000

    return power


def calculate_wind_energy(power,hours):

    energy=power*hours

    return energy

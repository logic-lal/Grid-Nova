def calculate_solar_power(irradiace,area,efficiency):
    power=(irradiace*area*efficiency)/1000
    return power

def calculate_solar_energy(power,hours):
    energy=power*hours
    return energy

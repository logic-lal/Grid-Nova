
import math


# Project settings
solar_energy=16.0
demand=6.1

initial_soc=10
capacity=30

charge_efficiency=0.95

blade_radius=2
wind_efficiency=0.40
air_density=1.225
hours=24


required_wind_energy=(capacity-initial_soc)/charge_efficiency-(solar_energy-demand)


# Calculation of wind energy
def wind_energy(speed):

    area=math.pi*blade_radius**2

    power=(0.5*air_density*area*speed**3*wind_efficiency)/1000

    return power*hours


# Root equation that we need to solve

def f(speed):

    return wind_energy(speed)-required_wind_energy


# Derivative of root equation
def derivative(speed):

    area=math.pi*blade_radius**2

    constant=(0.5*air_density*area*wind_efficiency*hours)/1000

    return 3*constant*speed**2


# Bisection Method
def bisection(a,b,e):

    if f(a)*f(b)>=0:
        return None,0

    iteration=0

    while iteration<100:

        c=(a+b)/2

        iteration+=1

        if abs(f(c))<e:
            return c,iteration

        if f(a)*f(c)<0:
            b=c
        else:
            a=c

    return c,iteration


# False Position Method
def false_position(a,b,e):

    if f(a)*f(b)>=0:
        return None,0

    iteration=0

    while iteration<100:

        c=(a*f(b)-b*f(a))/(f(b)-f(a))

        iteration+=1

        if abs(f(c))<e:
            return c,iteration

        if f(a)*f(c)<0:
            b=c
        else:
            a=c

    return c,iteration


# Newton-Raphson Method
def newton_raphson(x,e):

    iteration=0

    while iteration<100:

        if abs(derivative(x))<1e-12:
            return None,iteration

        new_x=x-f(x)/derivative(x)

        iteration+=1

        if abs(new_x-x)<e:
            return new_x,iteration

        x=new_x

    return x,iteration


# Run all three methods
root1,iterations1=bisection(0,10,0.000001)

root2,iterations2=false_position(0,10,0.000001)

root3,iterations3=newton_raphson(6,0.000001)


# Display project information
print("========== RENEWABLE ENERGY ROOT ANALYSIS ==========")

print("Solar Energy:",solar_energy,"kWh")
print("Daily Demand:",demand,"kWh")
print("Initial Battery SOC:",initial_soc,"kWh")
print("Battery Capacity:",capacity,"kWh")
print("Required Wind Energy:",round(required_wind_energy,4),"kWh")


# Display results
results=[
    ("Bisection",root1,iterations1),
    ("False Position",root2,iterations2),
    ("Newton-Raphson",root3,iterations3)
]

print("\n========== METHOD COMPARISON ==========")

for method,root,iterations in results:

    if root is not None:

        error=abs(f(root))

        print("\nMethod:",method)
        print("Required Wind Speed:",round(root,6),"m/s")
        print("Wind Energy:",round(wind_energy(root),4),"kWh")
        print("Residual:",round(error,8))
        print("Iterations:",iterations)


# Select the method with the smallest residual
valid_results=[
    (method,root,abs(f(root)))
    for method,root,iterations in results
    if root is not None
]

best=min(valid_results,key=lambda item:item[2])

print("\n========== BEST RESULT ==========")
print("Best Method:",best[0])
print("Required Wind Speed:",round(best[1],6),"m/s")
print("Residual:",round(best[2],8))

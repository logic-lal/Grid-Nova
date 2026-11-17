
def manage_battery(soc,generation,demand,capacity):

    charge_efficiency=0.95
    discharge_efficiency=0.95

    surplus=generation-demand
    shortage=demand-generation

    charged=0
    discharged=0
    unserved=0

    if surplus>0:

        available_space=capacity-soc

        charge_input=min(surplus,available_space/charge_efficiency)

        charged=charge_input*charge_efficiency

        soc=soc+charged

    elif shortage>0:

        required_energy=shortage/discharge_efficiency

        discharged=min(soc,required_energy)

        delivered_energy=discharged*discharge_efficiency

        soc=soc-discharged

        unserved=shortage-delivered_energy

    return soc,charged,discharged,unserved

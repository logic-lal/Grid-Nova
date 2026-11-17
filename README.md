<<<<<<< HEAD
# GridNova
## Intelligent Hybrid Renewable Energy Optimization and Simulation System

GridNova is an educational hybrid renewable-energy simulator. It models solar and wind energy generation, household electricity demand, battery charging/discharging, seven-day energy behaviour, and selected numerical methods.

## Features
- Solar generation from irradiance, panel area, efficiency, and sunshine duration.
- Wind generation from wind speed, turbine blade radius, and efficiency.
- Household appliance energy-demand calculation.
- Battery charge/discharge model with 95% charge and discharge efficiency.
- Daily and seven-day interactive simulations with charts.
- Bisection, False Position, and Newton-Raphson methods for estimating a wind speed that reaches a target daily wind-energy value.
- Euler and Modified Euler methods for a simplified battery state-of-charge prediction model.
- A user-editable 3-variable linear system solved using Gauss Elimination and Gauss-Jordan methods.

## Requirements
- Python 3.10 or newer
- Packages listed in `requirements.txt`

## Setup (Windows PowerShell)
```powershell
py -3.13 -m venv .venv
.venv\\Scripts\\Activate.ps1
python -m pip install -r requirements.txt
```

If PowerShell blocks environment activation, use Git Bash:
```bash
source .venv/Scripts/activate
```

## Run the Streamlit dashboard
Run from the project root (the folder containing `src`):
```bash
python -m streamlit run src/app.py
```

## Run the original terminal simulation
```bash
python src/main.py
```

## Project structure
- `src/app.py`: interactive GridNova dashboard
- `src/energy_sources/solar.py`: solar energy calculations
- `src/energy_sources/wind.py`: wind energy calculations
- `src/demand.py`: appliance demand calculation
- `src/battery.py`: battery charging/discharging
- `src/linear_equation.py`: Gauss Elimination and Gauss-Jordan methods
- `src/numerical_methods.py`: standalone Bisection, False Position, and Newton-Raphson examples
- `src/differential_equation.py`: standalone Euler and Modified Euler examples
- `src/weekly_simulation.py`: seven-day terminal simulation

## Model assumptions and limitations
- The solar and wind calculations use simplified idealized input-based models.
- Battery charging and discharging efficiencies are fixed at 95%.
- The Euler/Modified Euler dashboard demonstration uses a simplified bounded battery-rate model for teaching purposes; it is not a validated battery electrochemical model.
- The linear-system tab is a numerical-method demonstration. Its solution is not, by itself, an optimized real-world energy dispatch schedule.
- Results are simulations, not forecasts or engineering design guarantees.
=======
# Grid-Nova
>>>>>>> 658409cf47191aecee906b3aa81ff39cadc3b34a

# CloudSense AI

A beginner-friendly demonstration of AI-driven cloud resource optimization and predictive auto-scaling.

## What it demonstrates
- Synthetic workload generation (low, normal, spike).
- Random Forest Regression predicts next-interval CPU utilization.
- A policy engine recommends scale up, scale down, or maintain.
- A dashboard displays metrics, decisions, history, and an illustrative cost estimate.

## Important research and billing notes
- The first version uses simulated workload and a simulated instance count. It does not launch, stop, or resize AWS resources.
- The cost figure is an illustrative model ($0.01 per simulated instance-hour), not an AWS price quote.
- The ML training data is synthetic. Do not present its test metrics as real-world AWS performance.
- Before AWS deployment, check the account's Free Tier credits, instance eligibility, region pricing, EBS, public IPv4, and data transfer charges.

## Run on Windows PowerShell
```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
python app.py
```
Open http://127.0.0.1:5000

If PowerShell blocks activation, use:
```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

## Demo procedure
1. Select `Low demand`, click `Run next interval` a few times.
2. Select `Normal demand` and run several intervals.
3. Select `Traffic spike` and run several intervals.
4. Observe predicted CPU and scaling recommendations.
5. Click `Reset demo` to restart.

## Project structure
- `app.py`: Flask routes and application state.
- `simulator.py`: workload generation.
- `ml_model.py`: Random Forest training and prediction.
- `scaling.py`: scaling policy.
- `templates/index.html`: dashboard layout.
- `static/style.css`: styling.
- `static/app.js`: dashboard interactions and charts.

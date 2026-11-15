# Inverted Cart Python Scripts

This folder contains the Python calculations for the inverted-cart model.

## Requirements

- Python 3.10+
- `numpy`, `scipy`, `matplotlib`

## Setup

From PowerShell, create and activate a virtual environment:

```powershell
cd D:\Programing\Github\inverted_cart\python
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Run the scripts

**1st report**
```powershell
python buildStateSpace.py
python computeEquilibriumTorque.py
```

**2nd report**

Nonlinear sims

```powershell
python simulateClosedLoop.py
python simulateFall.py
```
other
```
findEquilibriumAngle.ipynb
simulatePendulum.ipynb
```



## Exit the virtual environment

```powershell
deactivate
```


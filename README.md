
# CorroScope

CorroScope is a Streamlit research companion for corrosion studies. It provides selected scientific calculations and simple tools for organizing experimental measurements.

## Features

- Specimen mass-loss calculation.
- Weight-loss corrosion rate in mm/year.
- Electrochemical corrosion-rate estimation.
- Corrosion-inhibition efficiency.
- Experiment records with CSV import and export.
- Literature notes with keyword search.
- Automated tests for the scientific calculation functions.

## Installation

Python 3.10 or newer is recommended.

Create and activate a virtual environment:

```bash
python -m venv .venv
```

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Launch the application:

```bash
python -m streamlit run app.py
```

Run tests:

```bash
python -m pytest -q
```

## Scientific equations

### Weight-loss corrosion rate

CR (mm/year) = 87.6 × W / (density × area × time)

- W: mass loss in milligrams.
- Density: g/cm³.
- Area: exposed area in cm².
- Time: exposure duration in hours.

### Electrochemical corrosion rate

CR (mm/year) = 0.00327 × Icorr × EW / density

- Icorr: corrosion current density in µA/cm².
- EW: equivalent weight in g/equivalent.
- Density: g/cm³.

### Inhibition efficiency

IE (%) = [(CR_blank - CR_inhibited) / CR_blank] × 100

Use compatible corrosion-rate measurements and appropriate material-specific assumptions.

## Data handling

Records and literature notes are stored in the active Streamlit session in this version. Export important data to CSV before ending the session. No persistent database or user-account system is included.

## Disclaimer

CorroScope supports calculations and record keeping. Verify units, formulas, experimental assumptions, and outputs against your laboratory protocol and relevant standards before reporting results.

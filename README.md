# SCI Federated Learning Experiments

This repository contains the experimental framework used to evaluate the environmental sustainability of Centralized Learning and Federated Learning scenarios using:

- CIFAR-10
- PyTorch
- Flower
- CodeCarbon
- Boavizta

The experiments generate environmental and sustainability data that will be used to calculate Software Carbon Intensity (SCI).

---

# Requirements

## Python

This project was developed using:

```text
Python 3.11+
```

Check your version:

```bash
python --version
```

---

# Installation

## 1. Clone the repository

```bash
git clone https://github.com/rutpal/tfm-sci-federated-learning.git

cd tfm-sci-federated-learning
```

---

## 2. Create a virtual environment

### Linux / macOS

```bash
python3 -m venv venv

source venv/bin/activate
```

### Windows

```cmd
python -m venv venv

venv\Scripts\activate
```

---

## 3. Install dependencies

```bash
pip install --upgrade pip

pip install -r requirements.txt
```

---

# Running the experiments

The full experimental pipeline can be executed using:

```bash
python run_probe.py
```

You will be asked for:

```text
Device category
Device purchase year
```

Example:

```text
Device category: laptop

Device purchase year: 2023
```

---

## Command-line execution

The experiment can also be launched directly using arguments:

```bash
python run_probe.py \
    --device-category laptop \
    --device-year 2023
```

Available device categories:

```text
laptop
desktop
smartphone
tablet
server
```

---

# Experiments executed

The framework automatically executes:

1. Centralized Learning
2. Federated Learning (3 clients)
3. Federated Learning (5 clients)
4. Federated Learning (7 clients)

---

# Generated files

Results are stored under:

```text
probes/
```

Example:

```text
env_<probe_id>_centralized.csv

cc_<probe_id>_centralized.csv

env_<probe_id>_FL_3.csv

cc_<probe_id>_FL_3_1.csv
cc_<probe_id>_FL_3_2.csv
cc_<probe_id>_FL_3_3.csv

env_<probe_id>_FL_5.csv

...

env_<probe_id>_FL_7.csv

...
```

Where:

```text
env = Experimental context and results

cc = CodeCarbon measurements
```

---

# Automatic upload

At the end of the execution:

1. All generated CSV files are compressed into:

```text
<probe_id>.zip
```

2. The ZIP file is automatically uploaded to the project collection endpoint.

3. A confirmation message is displayed when the upload succeeds.

---

# Output data

The collected data includes:

## Experimental metadata

```text
Device category
Device purchase year
Scenario
Training configuration
Number of clients
Number of rounds
Training samples
```

## Machine learning metrics

```text
Accuracy
Training duration
```

## Sustainability metrics

```text
Energy consumption (kWh)
Carbon emissions (kgCO2eq)
```

## CodeCarbon telemetry

```text
CPU information
RAM information
Location
Carbon intensity
Electricity consumption
Operational emissions
```

---

# Troubleshooting

## Module not found

Make sure the virtual environment is activated:

### Linux / macOS

```bash
source venv/bin/activate
```

### Windows

```cmd
venv\Scripts\activate
```

Then reinstall dependencies:

```bash
pip install -r requirements.txt
```

---

## Upload errors

If the automatic upload fails:

1. Keep the generated ZIP file.
2. Contact the project maintainer.
3. Provide the Probe ID shown at the end of the execution.

---

# License

This repository is distributed for academic and research purposes only.
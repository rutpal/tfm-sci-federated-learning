# SCI Federated Learning Experiments

This repository contains the experimental framework used in a research project conducted by the [SEC Research Group at UNIR](https://investigacion.unir.net/grupos/35512/detalle) (Universidad Internacional de La Rioja). The project investigates the environmental sustainability of Artificial Intelligence training workloads.

The objective is to compare Centralized Learning vs Federated Learning in terms of CO2e emissions using the Software Carbon Intensity (SCI) framework and embodied carbon estimations obtained from Boavizta.

The framework automatically:

- Trains machine learning models.
- Measures energy consumption and emissions using CodeCarbon.
- Collects hardware and execution metadata.
- Uploads results automatically for research purposes.

---

# Why participate?

The goal of this study is to understand how training strategies and hardware choices affect the sustainability of AI systems. The more variety of devices and locations involved, the more valuable the dataset becomes. Particularly interesting are executions from:

- Different countries and regions, as electricity carbon intensity varies across locations and directly affects operational emissions.
- Different hardware generations (Laptops, Desktops, Servers, Cloud environments).
- Both new and old devices, since embodied carbon plays an important role in the sustainability assessment.

---

# Requirements

## Python

This project was developed and tested using:

```text
Python 3.11+
```

Verify your installation:

```bash
python --version
```

---

# Installation

## 1. Get the repository

### Option A: Clone the repository with Git

```bash
git clone https://github.com/rutpal/tfm-sci-federated-learning.git

cd tfm-sci-federated-learning
```

### Option B: Download as ZIP

Download the repository as a ZIP file from:

https://github.com/rutpal/tfm-sci-federated-learning

Then extract the ZIP file and navigate to the project directory:

```bash
cd tfm-sci-federated-learning-main
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

Execute:

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

The experiment can also be started directly:

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

# Experiments executed automatically

The framework runs the following scenarios:

1. Centralized Learning
2. Federated Learning (3 clients)
3. Federated Learning (5 clients)
4. Federated Learning (7 clients)

No additional interaction is required.

---

# Data collected

The experiment collects:

## Experimental metadata

```text
Device category
Device purchase year
Training configuration
Number of clients
Number of rounds
Dataset size
```

## Machine learning metrics

```text
Accuracy
Training duration
```

## Sustainability metrics

```text
Energy consumption
Operational emissions
```

## Hardware metadata

```text
CPU information
RAM information
Hardware characteristics
```

## Geographic metadata

```text
Country
Region
Carbon intensity used by CodeCarbon
```

---

# Generated files

The framework creates several CSV files under:

```text
probes/
```

Examples:

```text
env_<probe_id>_centralized.csv

cc_<probe_id>_centralized.csv

env_<probe_id>_FL_3.csv

cc_<probe_id>_FL_3_1.csv
cc_<probe_id>_FL_3_2.csv
cc_<probe_id>_FL_3_3.csv

env_<probe_id>_FL_5.csv

env_<probe_id>_FL_7.csv
```

Where:

```text
env = Experimental metadata and aggregated results

cc = Raw CodeCarbon measurements
```

---

# Automatic upload

At the end of the execution:

1. All generated CSV files are compressed into:

```text
<probe_id>.zip
```

2. The ZIP file is uploaded automatically to the data collection endpoint.

3. A confirmation message is displayed.

No manual submission is required.

---

# Privacy

The framework does not collect:

- Personal files
- Documents
- Browsing history
- Passwords
- User credentials

Only technical and experimental information required for the study is collected.

---

# Expected duration

Typical execution times:

| Device | Estimated duration |
|----------|----------|
| Modern Laptop/Desktop | 10-15 min |
| Older Laptop/Desktop | 15-25 min |
| Cloud/Server Environment | Variable |

---

# Troubleshooting

## Module not found

Verify that the virtual environment is active:

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

## Upload error

If the automatic upload fails:

1. Keep the generated ZIP file.
2. Note the Probe ID displayed at the end.
3. Contact the repository owner.

---

# Research context

This framework is part of a Master's Thesis focused on:

- Sustainable Artificial Intelligence
- Federated Learning
- Software Carbon Intensity (SCI)
- Embodied Carbon
- Environmental impact of machine learning systems

Every execution contributes to building a larger dataset that will support the analysis and conclusions of the study.

Thank you for participating.

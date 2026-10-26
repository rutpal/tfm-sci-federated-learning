# SCI Federated Learning Experiments

This repository contains the experimental framework used in a Master's Thesis research project focused on the environmental sustainability of Artificial Intelligence training workloads.

The objective is to compare:

- Centralized Learning
- Federated Learning

using the Software Carbon Intensity (SCI) framework and embodied carbon estimations obtained from Boavizta.

The framework automatically:

- Trains machine learning models
- Measures energy consumption and emissions using CodeCarbon
- Collects hardware and execution metadata
- Uploads results automatically for research purposes

---

# Why participate?

The goal of this study is to understand how training strategies and hardware choices affect the sustainability of AI systems. The more variety of devices and locations involved, the more valuable the dataset becomes.

Particularly interesting are executions from:

- Different countries and regions, as regional electricity carbon intensity influences the environmental impact of training
- Different hardware generations (Laptops, Desktops, Servers and Cloud environments)
- Both new and old devices, allowing the study to account for embodied carbon alongside operational emissions

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

Extract the ZIP file and open the project directory.

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

From the project root directory:

```bash
pip install --upgrade pip

pip install -r requirements.txt
```

---

# Running the experiments

Move to the `src` directory:

```bash
cd src
```

Then execute:

```bash
python run_probe.py
```

> **Note:** The first execution may take longer because the CIFAR-10 dataset will be downloaded automatically.

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

From the `src` directory:

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
| Modern Laptop/Desktop | 10–15 min |
| Older Laptop/Desktop | 15–25 min |
| Cloud/Server Environment | Variable |

---

# Troubleshooting

## Module not found

Verify that the virtual environment is active.

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

---

# License

This repository is distributed for academic and research purposes only.

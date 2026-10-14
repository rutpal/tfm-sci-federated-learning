# probe.py

from pathlib import Path
import pandas as pd
import time
from pathlib import Path
import zipfile
import base64
import requests


def build_env(
    probe_id,
    scenario,
    dataset,
    model,
    device_category,
    device_year,
    epochs,
    batch_size,
    learning_rate,
    training_samples,
    accuracy,
    energy_total_kwh,
    emissions_total_kg,
    training_time_total_s,
    num_clients=1,
    num_rounds=1
):
    """
    Construye la estructura común env utilizada
    por los escenarios centralizado y federado.
    """

    env = {

        # ==================================================
        # Identificación
        # ==================================================

        "probe_id": probe_id,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),

        # ==================================================
        # Dispositivo
        # ==================================================

        "device_category": device_category,
        "device_year": device_year,

        # ==================================================
        # Escenario experimental
        # ==================================================

        "scenario": scenario,
        "dataset": dataset,
        "model": model,

        # ==================================================
        # Topología FL
        # ==================================================

        "num_clients": num_clients,
        "num_rounds": num_rounds,

        # ==================================================
        # Configuración de entrenamiento
        # ==================================================

        "epochs": epochs,
        "batch_size": batch_size,
        "learning_rate": learning_rate,

        # ==================================================
        # Tamaño del trabajo
        # ==================================================

        "training_samples": training_samples,

        # ==================================================
        # Resultados
        # ==================================================

        "accuracy": accuracy,
        "energy_total_kwh": energy_total_kwh,
        "emissions_total_kg": emissions_total_kg,
        "training_time_total_s": training_time_total_s
    }

    return env


def save_env(
    env,
    probes_dir
):
    """
    Guarda el fichero env_<probe_id>_<scenario>.csv
    """

    Path(probes_dir).mkdir(
        parents=True,
        exist_ok=True
    )

    probe_id = env["probe_id"]
    scenario = env["scenario"]

    env_file = (
        Path(probes_dir)
        / f"env_{probe_id}_{scenario}.csv"
    )

    pd.DataFrame([env]).to_csv(
        env_file,
        index=False
    )

    return env_file

def create_probe_zip(
    probe_id,
    probes_dir
):

    zip_path = (
        Path(probes_dir)
        / f"{probe_id}.zip"
    )

    with zipfile.ZipFile(
        zip_path,
        "w",
        zipfile.ZIP_DEFLATED
    ) as zipf:

        for csv_file in Path(probes_dir).glob(
            f"*{probe_id}*.csv"
        ):
            zipf.write(
                csv_file,
                arcname=csv_file.name
            )

    return zip_path
    
def upload_probe_zip(
    zip_path,
    endpoint_url
):

    with open(zip_path, "rb") as f:

        encoded_file = (
            base64
            .b64encode(f.read())
            .decode()
        )

    response = requests.post(
        endpoint_url,
        data={
            "filename": zip_path.name,
            "file": encoded_file
        }
    )

    response.raise_for_status()

    return response.json()
import logging

import config
from pathlib import Path
from codecarbon import EmissionsTracker

def run_training_with_codecarbon(
    train_function,
    probe_id,
    scenario,
    client_id=None
):

    Path(config.PROBES_DIR).mkdir(
        parents=True,
        exist_ok=True
    )

    if client_id is None:

        output_file = (
            f"cc_{probe_id}_{scenario}.csv"
        )

    else:

        output_file = (
            f"cc_{probe_id}_{scenario}_{client_id}.csv"
        )
    

    logging.getLogger("codecarbon").setLevel(logging.ERROR)

    tracker = EmissionsTracker(
        output_dir=config.PROBES_DIR,
        output_file=output_file
    )

    tracker.start()

    tracker.start_task("training")

    train_function()

    training_data = tracker.stop_task()

    tracker.stop()

    # Eliminar archivos de emisiones base
    for file in Path(config.PROBES_DIR).glob(
        "emissions_base*.csv"
    ):
        file.unlink()

    return {
        "client_id": client_id,
        "energy_total_kwh":
            training_data.energy_consumed,
        "emissions_total_kg":
            training_data.emissions,
        "training_time_total_s":
            training_data.duration
    }
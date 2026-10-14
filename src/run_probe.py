# run_probe.py

import argparse
import config
from probe import (create_probe_zip, upload_probe_zip)

from environment import get_probe_context

from Centralized_training import (
    run_centralized_experiment
)

from Federated_training import (
    run_federated_experiment
)

def parse_args():

    parser = argparse.ArgumentParser(
        description=(
            "SCI Federated vs Centralized Learning Probe"
        )
    )

    parser.add_argument(
        "--device-category",
        choices=[
            "laptop",
            "desktop",
            "smartphone",
            "tablet",
            "server"
        ],
        help="Device category"
    )

    parser.add_argument(
        "--device-year",
        type=int,
        help="Device purchase year"
    )

    return parser.parse_args()


def main():

    args = parse_args()

    if (
        args.device_category is not None
        and
        args.device_year is not None
    ):

        context = get_probe_context(
            device_category=args.device_category,
            device_year=args.device_year
        )

    else:

        context = get_probe_context()

    probe_id = context["probe_id"]
    device_category = context["device_category"]
    device_year = context["device_year"]

    print(
        f"\nProbe ID: {probe_id}\n"
    )

    print(
        "\n[1/4] Running Centralized..."
    )

    run_centralized_experiment(
        probe_id=probe_id,
        device_category=device_category,
        device_year=device_year
    )

    print(
        "\n[2/4] Running FL-3..."
    )

    run_federated_experiment(
        probe_id=probe_id,
        device_category=device_category,
        device_year=device_year,
        num_clients=3
    )

    print(
        "\n[3/4] Running FL-5..."
    )

    run_federated_experiment(
        probe_id=probe_id,
        device_category=device_category,
        device_year=device_year,
        num_clients=5
    )

    print(
        "\n[4/4] Running FL-7..."
    )

    run_federated_experiment(
        probe_id=probe_id,
        device_category=device_category,
        device_year=device_year,
        num_clients=7
    )

    print(
        "\nExperiment completed successfully."
    )

    print(
        f"\nProbe ID: {probe_id}"
    )

    # ==========================================
    # Comprimir resultados
    # ==========================================

    zip_file = create_probe_zip(
        probe_id,
        config.PROBES_DIR
    )

    print(
        f"\nResults saved to: {zip_file}"
    )

    # ==========================================
    # Subir resultados
    # ==========================================

    print(
        "\nUploading results..."
    )

    response = upload_probe_zip(
        zip_file,
        config.ENDPOINT_URL
    )

    if response.get("status") == "ok":

        print(
            "\n================================="
        )

        print(
            "Probe completed successfully."
        )

        print(
            f"Probe ID: {probe_id}"
        )

        print(
            f"Uploaded file: {zip_file.name}"
        )

        print(
            "Results successfully sent."
        )

        print(
            "================================="
        )

    else:

        print(
            "\nUpload failed."
        )

        print(response)

if __name__ == "__main__":
    main()
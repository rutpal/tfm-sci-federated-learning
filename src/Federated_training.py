import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from torch.utils.data import random_split

import config
from dataset import load_cifar10
from model import SimpleCNN
from training import (
    train_model,
    evaluate_model,
    create_optimizer
)
from monitoring import run_training_with_codecarbon
from probe import (
    build_env,
    save_env
)

def dataloader_federated  (train_dataset, test_dataset, num_clients):

#
# ==================================================
# Partición FL-#
# ==================================================

    client_size = len(train_dataset) // num_clients

    lengths = [client_size] * num_clients

    lengths[-1] += (
        len(train_dataset) - sum(lengths)
    )

    client_datasets = random_split(
        train_dataset,
        lengths
    )


# ==================================================
# DataLoaders de clientes
# ==================================================

    client_loaders = [
        DataLoader(
            ds,
            batch_size=config.BATCH_SIZE,
            shuffle=True
        )
        for ds in client_datasets
    ]

# ==================================================
# Test loader global
# ==================================================

    test_loader = DataLoader(
        test_dataset,
        batch_size=config.BATCH_SIZE,
        shuffle=False
    )

    return client_loaders, test_loader


# 8. Cliente Flower

import flwr as fl

class FlowerClient(fl.client.NumPyClient):

    def __init__(
        self,
        model,
        train_loader,
        test_loader,
        probe_id,
        client_id,
        scenario
    ):
        self.model = model
        self.train_loader = train_loader
        self.test_loader = test_loader
        self.probe_id = probe_id
        self.client_id = client_id
        self.scenario = scenario

    def get_parameters(
        self,
        flower_config
    ):
        return [
            val.detach().numpy()
            for _, val in self.model.state_dict().items()
        ]

    def set_parameters(
        self,
        parameters
    ):

        params_dict = zip(
            self.model.state_dict().keys(),
            parameters
        )

        state_dict = {
            k: torch.tensor(v)
            for k, v in params_dict
        }

        self.model.load_state_dict(
            state_dict,
            strict=True
        )

    def fit(
        self,
        parameters,
        flower_config
    ):

        self.set_parameters(parameters)

        local_criterion = nn.CrossEntropyLoss()

        local_optimizer = create_optimizer(
            self.model,
            config.LEARNING_RATE
        )

        cc_metrics = run_training_with_codecarbon(
            train_function=lambda: train_model(
                self.model,
                self.train_loader,
                local_optimizer,
                local_criterion,
                config.EPOCHS
            ),
            probe_id=self.probe_id,
            scenario=self.scenario,
            client_id=self.client_id
        )

        return (
            self.get_parameters(flower_config),
            len(self.train_loader.dataset),
            cc_metrics
        )

    def evaluate(
        self,
        parameters,
        flower_config
    ):

        self.set_parameters(parameters)

        accuracy = evaluate_model(
            self.model,
            self.test_loader
        )

        return (
            0.0,
            len(self.test_loader.dataset),
            {
                "accuracy": accuracy
            }
        )


# 7. Función FedAvg

import numpy as np

def fedavg(client_parameters):

    aggregated_parameters = []

    for layer_weights in zip(*client_parameters):

        aggregated_layer = np.mean(
            layer_weights,
            axis=0
        )

        aggregated_parameters.append(
            aggregated_layer
        )

    return aggregated_parameters


# 8. Inicialización del Entorno Federado

def initialize_federated_environment(
        probe_id,
        num_clients, 
        scenario,
        client_loaders, 
        test_loader
):

    # Modelo global inicial
    global_model = SimpleCNN()

    global_parameters = [
        val.detach().numpy()
        for _, val in global_model.state_dict().items()
    ]

    # Clientes
    clients = []

    for i in range(num_clients):

        clients.append(
            FlowerClient(
                model=SimpleCNN(),
                train_loader=client_loaders[i],
                test_loader=test_loader,
                probe_id=probe_id,
                client_id=i + 1,
                scenario=scenario
            )
        )

    return (
        #global_model,
        global_parameters,
        clients
    )

# 9. Ejecución del entrenamiento generado


def run_federated_training(
    clients,
    global_parameters
):

    client_metrics = []

    for round_num in range(config.NUM_ROUNDS):

        round_parameters = []

        round_metrics = []

        print(
            f"\n===== ROUND {round_num + 1} ====="
        )

        for client_id, client in enumerate(clients):

            updated_parameters, num_examples, metrics = client.fit(
                global_parameters,
                {}
            )

            metrics["round"] = round_num + 1
            metrics["client_id"] = client_id + 1

            round_metrics.append(
                metrics
            )

            round_parameters.append(
                updated_parameters
            )

        global_parameters = fedavg(
            round_parameters
        )

        client_metrics.extend(
            round_metrics
        )

    return (
        global_parameters,
        client_metrics
    )


# 10. Construcción del modelo global

def build_global_model(
    global_parameters
):

    global_model = SimpleCNN()

    params_dict = zip(
        global_model.state_dict().keys(),
        global_parameters
    )

    state_dict = {
        k: torch.tensor(v)
        for k, v in params_dict
    }

    global_model.load_state_dict(
        state_dict,
        strict=True
    )

    return global_model


# 11. Ejecución del experimento federado
def run_federated_experiment(
    probe_id,
    device_category,
    device_year,
    num_clients
):

    scenario = f"FL_{num_clients}"

    train_dataset, test_dataset = load_cifar10()

    client_loaders, test_loader = dataloader_federated(
        train_dataset,
        test_dataset,
        num_clients
    )

    # ==================================================
    # Inicialización
    # ==================================================

    #global_model, global_parameters, clients = (
    global_parameters, clients = (        
        initialize_federated_environment(
            probe_id,
            num_clients,
            scenario,
            client_loaders,
            test_loader
        )
    )

    # ==================================================
    # Entrenamiento federado
    # ==================================================

    global_parameters, client_metrics = (
        run_federated_training(
            clients,
            global_parameters
        )
    )

    # ==================================================
    # Construcción del modelo global
    # ==================================================

    global_model = build_global_model(
        global_parameters
    )

    # ==================================================
    # Captura de datos final
    # ==================================================

    global_accuracy = evaluate_model(
        global_model,
        test_loader
    )

    energy_total_kwh = sum(
        m["energy_total_kwh"]
        for m in client_metrics
    )

    emissions_total_kg = sum(
        m["emissions_total_kg"]
        for m in client_metrics
    )

    training_time_total_s = sum(
        m["training_time_total_s"]
        for m in client_metrics
    )

    env = build_env(
        probe_id=probe_id,
        scenario=scenario,
        dataset=config.DATASET,
        model=config.MODEL_NAME,
        device_category=device_category,
        device_year=device_year,
        epochs=config.EPOCHS,
        batch_size=config.BATCH_SIZE,
        learning_rate=config.LEARNING_RATE,
        training_samples=len(train_dataset),
        accuracy=global_accuracy,
        energy_total_kwh=energy_total_kwh,
        emissions_total_kg=emissions_total_kg,
        training_time_total_s=training_time_total_s,
        num_clients=num_clients,
        num_rounds=config.NUM_ROUNDS
    )

    save_env(
        env,
        config.PROBES_DIR

    )
    print(f"Scenario: {scenario}")
    print(f"Rounds: {config.NUM_ROUNDS}")

    print(f"    Global accuracy: {global_accuracy:.4f}")

    print(f"    Energy total: {energy_total_kwh:.6f}")

    print(f"    Emissions total: {emissions_total_kg:.8f}")

    print(f"Training time total: {training_time_total_s:.2f}")

    return env
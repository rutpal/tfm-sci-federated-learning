import torch
from torch.utils.data import DataLoader
import torch.nn as nn

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
 
# 1. Carga del Dataset y DataLoader

# ==================================================
# DataLoader
# ==================================================

def dataloader_centralized (train_dataset, test_dataset, batch_size):
    
    train_loader = DataLoader(
        train_dataset,
        batch_size=batch_size,
        shuffle=True
    )

    test_loader = DataLoader(
        test_dataset,
        batch_size=batch_size,
        shuffle=False
    )

    return train_loader, test_loader

# 8. Función de ejecución del experimento
# y captura de datos del probe (code carbon (cc) y entorno (env))

 


def run_centralized_experiment(
    probe_id,
    device_category,
    device_year
):

    scenario = "centralized"
    
    train_dataset, test_dataset = load_cifar10()

    train_loader, test_loader = dataloader_centralized(
        train_dataset,
        test_dataset,
        config.BATCH_SIZE
    )

    model = SimpleCNN()

    optimizer = create_optimizer(
        model,
        config.LEARNING_RATE
    )

    criterion = nn.CrossEntropyLoss()

    cc_metrics = run_training_with_codecarbon(
        train_function=lambda: train_model(
            model,
            train_loader,
            optimizer,
            criterion,
            config.EPOCHS
        ),
        probe_id=probe_id,
        scenario=scenario, 
        client_id=None
    )
    
    accuracy = evaluate_model(
        model,
        test_loader
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
        training_samples=len(train_loader.dataset),
        accuracy=accuracy,
        energy_total_kwh=cc_metrics["energy_total_kwh"],
        emissions_total_kg=cc_metrics["emissions_total_kg"],
        training_time_total_s=cc_metrics["training_time_total_s"],
        num_clients=1,
        num_rounds=config.NUM_ROUNDS
    )
    
    save_env(
    env,
    config.PROBES_DIR
    )
    print(f"Scenario: {scenario}")
    print(f"Rounds: {config.NUM_ROUNDS}")

    print(f"    Global accuracy: {accuracy:.4f}")

    print(f"    Energy total: {cc_metrics['energy_total_kwh']:.6f}")

    print(f"    Emissions total: {cc_metrics['emissions_total_kg']:.8f}")

    print(f"Training time total: {cc_metrics['training_time_total_s']:.2f}")

    return env
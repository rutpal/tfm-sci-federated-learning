import torch
import torch.nn as nn
import torch.optim as optim


# 4. Función de pérdida y optimización
def create_optimizer(model, learning_rate):

    optimizer = optim.Adam(
        model.parameters(),
        lr=learning_rate
    )

    return optimizer

# 5. Función de entrenamiento

def train_model(
    model,
    train_loader,
    optimizer,
    criterion,
    epochs
):

    model.train()

    for epoch in range(epochs):

        running_loss = 0.0

        for images, labels in train_loader:

            optimizer.zero_grad()

            outputs = model(images)

            loss = criterion(outputs, labels)

            loss.backward()

            optimizer.step()

            running_loss += loss.item()

        epoch_loss = (
            running_loss /
            len(train_loader)
        )

    return epoch_loss

# 6. Función de evaluación
def evaluate_model(
    model,
    test_loader
):
    model.eval()
    correct = 0
    total = 0
    with torch.no_grad():
        for images, labels in test_loader:
            outputs = model(images)
            _, predicted = torch.max(outputs, 1)
            total += labels.size(0)
            correct += (
                predicted == labels
            ).sum().item()
    accuracy = correct / total
    return accuracy

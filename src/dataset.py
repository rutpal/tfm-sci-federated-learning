import config
from torchvision import datasets
from torchvision import transforms

# 1. Carga del Dataset
def load_cifar10():  

    # ==================================================
    # Transformaciones
    # ==================================================

    transform = transforms.ToTensor()

    # ==================================================
    # Dataset
    # ==================================================

    train_dataset = datasets.CIFAR10(
        root=config.DATA_DIR,
        train=True,
        download=True,
        transform=transform
    )

    test_dataset = datasets.CIFAR10(
        root=config.DATA_DIR,
        train=False,
        download=True,
        transform=transform
    )

    return train_dataset, test_dataset
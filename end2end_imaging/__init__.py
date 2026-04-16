import torch


def init_device():
    """Initialize and return the default compute device (CUDA, MPS, or CPU)."""
    if torch.cuda.is_available():
        device = torch.device("cuda")
        device_name = torch.cuda.get_device_name(0)
        print(f"Using CUDA: {device_name} for End2endImaging")
    elif torch.backends.mps.is_available():
        device = torch.device("mps")
        device_name = "Apple MPS"
        print("Using MPS (Apple Silicon) for End2endImaging")
    else:
        device = torch.device("cpu")
        device_name = "CPU"
        print("Using CPU for End2endImaging")
    return device


# deeplens (optics)
from .deeplens import *

# network
from .network import *

# geolens
from .deeplens.geolens_pkg import *

# utilities
from .utils import *

# camera
from .camera import Camera

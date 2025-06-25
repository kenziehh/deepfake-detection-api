import torch
from torchvision import models
import torch.nn as nn

def load_resnet_model(path: str):
    model = models.resnet50(pretrained=False)
    model.fc = nn.Linear(model.fc.in_features, 2)
    model.load_state_dict(torch.load(path, map_location=torch.device("cpu")))
    model.eval()
    return model

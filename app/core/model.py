import torch
from torchvision import models
import torch.nn as nn
import torch
from transformers import Wav2Vec2Processor, Wav2Vec2ForSequenceClassification


def load_resnet_model(path: str):
    model = models.resnet50(pretrained=False)
    model.fc = nn.Linear(model.fc.in_features, 2)
    model.load_state_dict(torch.load(path, map_location=torch.device("cpu"), weights_only=False))
    model.eval()
    return model

def load_wav2vec2_model(path: str, device: torch.device = torch.device("cpu")):
    processor = Wav2Vec2Processor.from_pretrained("facebook/wav2vec2-base")
    model = Wav2Vec2ForSequenceClassification.from_pretrained(
        "facebook/wav2vec2-base",
        num_labels=2
    )
    model.load_state_dict(torch.load(path, map_location=device))
    model = model.to(device)
    model.eval()
    return processor, model
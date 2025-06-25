from torchvision import transforms
from PIL import Image
import torch

transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize([0.5]*3, [0.5]*3)
])

label_map = {0: "Fake", 1: "Real"}  

def predict(image_file, model):
    image = Image.open(image_file.file).convert("RGB")
    image = transform(image).unsqueeze(0)
    with torch.no_grad():
        output = model(image)
        confidence, pred = torch.max(output, 1)
    return label_map[pred.item()],confidence.item()

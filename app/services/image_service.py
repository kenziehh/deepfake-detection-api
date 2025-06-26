import cv2
import numpy as np
import torch

from torchvision import transforms

transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Resize((224, 224)),
    transforms.Normalize([0.5] * 3, [0.5] * 3)
])

label_map = {0: "Fake", 1: "Real"}

def predict(image_bytes_io, model):
    print("[DEBUG] Predict using OpenCV...")

    try:
        # Baca buffer ke dalam NumPy array
        image_bytes = image_bytes_io.read()
        nparr = np.frombuffer(image_bytes, np.uint8)

        # Decode image dari buffer
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        if img is None:
            raise ValueError("cv2 failed to decode image")

        # Konversi BGR ke RGB
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        # Resize + Normalize
        img_tensor = transform(img).unsqueeze(0)  # shape: [1, 3, 224, 224]

        # Predict
        with torch.no_grad():
            output = model(img_tensor)
            confidence, pred = torch.max(output, 1)

        return label_map[pred.item()], confidence.item()

    except Exception as e:
        print(f"[ERROR] OpenCV predict error: {e}")
        raise ValueError("Failed to process image with OpenCV")

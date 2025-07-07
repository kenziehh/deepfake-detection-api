import cv2
import numpy as np
import torch
from torchvision import transforms

label_map = {0: "Fake", 1: "Real"}

transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize([0.5]*3, [0.5]*3)
])

def predict(image_file, model):
    try:
        if hasattr(image_file, "file"):
            image_bytes = image_file.file.read()
        else:
            image_bytes = image_file.read()

        print(f"[DEBUG] image_bytes size: {len(image_bytes)}")

        np_array = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(np_array, cv2.IMREAD_COLOR)

        if img is None:
            raise ValueError("OpenCV gagal decode gambar (img=None)")

        img = cv2.resize(img, (224, 224))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        transform = transforms.Compose([
            transforms.ToTensor(),
            transforms.Normalize([0.5]*3, [0.5]*3)
        ])

        img_tensor = transform(img).unsqueeze(0)

        print(f"[DEBUG] img_tensor shape: {img_tensor.shape}")

        with torch.no_grad():
            output = model(img_tensor)
            confidence, pred = torch.max(output, 1)

        return {
            "label": label_map[pred.item()],
            "confidence": round(confidence.item()/10, 4)  
        }
    except Exception as e:
        print(f"[ERROR] Prediction failed: {e}")
        raise RuntimeError("Failed to process image with OpenCV")

from fastapi import APIRouter, File, UploadFile, HTTPException
from app.services.image_service import predict
from app.schemas.image import ImagePredictionResponse
from app.core.model import load_resnet_model
from io import BytesIO


router = APIRouter()

model = load_resnet_model("models/images/deepfake_resnet50 (1).pth")

@router.post("/predict", response_model=ImagePredictionResponse)
async def predict_deepfake(file: UploadFile = File(...)):
    if not file.filename.lower().endswith((".jpg", ".jpeg", ".png")):
        raise HTTPException(status_code=400, detail="File must be an image")

    try:
        print(f"Received file: {file.filename}, content_type: {file.content_type}")
        
        file_data = await file.read()
        print(f"File size: {len(file_data)} bytes")

        image_io = BytesIO(file_data)
        result = predict(image_io, model)
        prediction = result["label"]
        confidence = result["confidence"]


        return ImagePredictionResponse(
            filename=file.filename,
            prediction=prediction,
            confidence=confidence
        )

    except Exception as e:
        print(f"[ERROR] Prediction failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")


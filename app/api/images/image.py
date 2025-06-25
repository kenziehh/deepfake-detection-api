from fastapi import APIRouter, File, UploadFile, HTTPException
from app.services.image_service import predict
from app.schemas.image import ImagePredictionResponse
from app.core.model import load_resnet_model

router = APIRouter()

model = load_resnet_model("models/images/deepfake_resnet50.pth")

@router.post("/predict", response_model=ImagePredictionResponse)
async def predict_deepfake(file: UploadFile = File(...)):
    if not file.filename.lower().endswith((".jpg", ".jpeg", ".png")):
        raise HTTPException(status_code=400, detail="File must be an image")

    try:
        prediction, confidence = predict(file, model)
        return ImagePredictionResponse(
            filename=file.filename,
            prediction=prediction,
            confidence=confidence
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")

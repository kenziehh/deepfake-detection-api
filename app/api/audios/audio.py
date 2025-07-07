from fastapi import APIRouter, UploadFile, File
from app.schemas.audio import AudioPredictionResponse
from app.services.audio_service import predict_audio

router = APIRouter()

@router.post("/predict", response_model=AudioPredictionResponse)
async def predict(file: UploadFile = File(...)):
    result = await predict_audio(file)
    return result

from fastapi import APIRouter, UploadFile, File, HTTPException
from app.schemas.audio import AudioPredictionResponse
from app.services.audio_service import predict_audio
import logging

router = APIRouter()

@router.post("/predict", response_model=AudioPredictionResponse)
async def predict(file: UploadFile = File(...)):
    try:
        print(f"Received file: {file.filename}")
        print(f"Content type: {file.content_type}")
        print(f"File size: {file.size}")
        
        # Check if file is actually received
        if not file.filename:
            raise HTTPException(status_code=400, detail="No file uploaded")
            
        print(f"File name: {file.filename}")
        print(f"File extension: {file.filename.split('.')[-1] if '.' in file.filename else 'No extension'}")
        
        result = await predict_audio(file)
        return result
        
    except Exception as e:
        print(f"Error in predict endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
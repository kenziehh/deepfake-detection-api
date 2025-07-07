from pydantic import BaseModel

class AudioPredictionResponse(BaseModel):
    filename: str
    prediction: str
    confidence: float

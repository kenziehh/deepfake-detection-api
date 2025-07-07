from pydantic import BaseModel

class ImagePredictionResponse(BaseModel):
    filename: str
    prediction: str
    confidence: float

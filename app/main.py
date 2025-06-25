from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.images.image import router as image_router
app = FastAPI(title="Deepfake Detection API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(image_router, prefix="/api/images", tags=["Image"])


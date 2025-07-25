import torchaudio
import torch
import numpy as np
from io import BytesIO
from app.core.model import load_wav2vec2_model
from app.schemas.audio import AudioPredictionResponse
import tempfile
import os
from pydub import AudioSegment


async def predict_audio(file) -> AudioPredictionResponse:
    contents = await file.read()
    
    # Try to load with different approaches
    try:
        # Jika file adalah M4A, convert ke WAV dulu
        if file.filename.endswith('.m4a') or file.content_type == 'audio/m4a':
            audio_segment = AudioSegment.from_file(BytesIO(contents), format="m4a")
            wav_io = BytesIO()
            audio_segment.export(wav_io, format="wav", parameters=["-ac", "1", "-ar", "16000"])
            wav_io.seek(0)
            waveform, sr = torchaudio.load(wav_io)
        else:
            # Coba load langsung
            waveform, sr = torchaudio.load(BytesIO(contents))
            
    except Exception as e:
        print(f"Error loading audio: {e}")
        raise ValueError(f"Unable to load audio file: {str(e)}")

    if waveform.ndim == 2:
        waveform = waveform.mean(dim=0)

    if sr != 16000:
        waveform = torchaudio.transforms.Resample(sr, 16000)(waveform)

    max_len = 16000 * 6
    if waveform.shape[0] > max_len:
        waveform = waveform[:max_len]
    else:
        waveform = torch.nn.functional.pad(waveform, (0, max_len - waveform.shape[0]))

    processor, model = load_wav2vec2_model("models/audios/wav2vec2_deepfake_audio.pth", device=torch.device("cpu"))

    inputs = processor(
        [waveform.numpy()],
        sampling_rate=16000,
        return_tensors="pt",
        padding=True
    )
    input_values = inputs["input_values"].to(model.device)

    with torch.no_grad():
        outputs = model(input_values)
        probs = torch.softmax(outputs.logits, dim=1)
        pred = torch.argmax(probs, dim=1).item()
        confidence = probs[0][pred].item()

    return AudioPredictionResponse(
        filename=file.filename,
        prediction="FAKE" if pred == 1 else "REAL",
        confidence=confidence
    )

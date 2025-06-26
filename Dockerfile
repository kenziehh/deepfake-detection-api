FROM python:3.10-slim

ENV PYTHONUNBUFFERED=1

# Install OS-level dependencies for Pillow, OpenCV, dan image decoding
RUN apt-get update && apt-get install -y \
    gcc \
    libjpeg-dev \
    zlib1g-dev \
    libpng-dev \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libtiff-dev \
    libopenjp2-7-dev \
    libwebp-dev \
    tzdata \
    && rm -rf /var/lib/apt/lists/*


# Set working directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy project files
COPY . .

# Expose port
EXPOSE 8000

# Run FastAPI with uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

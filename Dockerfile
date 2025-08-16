FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Pre-download model weights
RUN python -c "from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline; AutoTokenizer.from_pretrained('google/flan-t5-small'); AutoModelForSeq2SeqLM.from_pretrained('google/flan-t5-small'); pipeline('summarization', model='sshleifer/distilbart-cnn-12-6')"

# Copy application code
COPY . .

# Make main.py executable
RUN chmod +x main.py

# Set the entrypoint
ENTRYPOINT ["python", "main.py"]
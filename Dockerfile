# Use official lightweight Python image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1     PYTHONUNBUFFERED=1     MPLCONFIGDIR=/tmp/mpl_config     PORT=7860

# Install system dependencies needed for RDKit and headless rendering
RUN apt-get update && apt-get install -y --no-install-recommends     build-essential     libxrender1     libxext6     curl     && rm -rf /var/lib/apt/lists/*

# Set up user for Hugging Face Spaces (UID 1000)
RUN useradd -m -u 1000 user
USER user
ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH

WORKDIR /home/user/app

# Install Python packages
COPY --chown=user requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Copy application source code
COPY --chown=user . /home/user/app

# Expose default port 7860 (Hugging Face / Cloud standard)
EXPOSE 7860

# Launch Streamlit app on port 7860
CMD ["streamlit", "run", "app.py", "--server.port=7860", "--server.address=0.0.0.0", "--server.headless=true"]

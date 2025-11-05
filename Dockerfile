# Use lightweight Python image
FROM python:3.10-slim

WORKDIR /code

# Copy dependencies first
COPY app/requirements.txt /code/requirements.txt

# Install dependencies
RUN pip install --no-cache-dir -r /code/requirements.txt

# Copy your app package
COPY app /code/app

# Expose port (Hugging Face uses 7860 or the platform $PORT)
EXPOSE 7860

# Start FastAPI using the package (no name conflict)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "7860"]


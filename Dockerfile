# Use lightweight Python image
FROM python:3.10-slim

WORKDIR /code

# Copy dependencies first
COPY app/requirements.txt /code/requirements.txt

# Install dependencies
RUN pip install --no-cache-dir -r /code/requirements.txt

# Copy your app files
COPY app /code/app
COPY main_entry.py /code/app.py


# Expose Hugging Face’s port
EXPOSE 7860

# Start FastAPI
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "7860"]


FROM python:3.10-slim

WORKDIR /code

# Copy dependencies first
COPY app/requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir -r /code/requirements.txt

COPY app /code/app

# (Optional) Copy .env if needed
# COPY .env /code/.env

# Ensure upload/data directory exists
RUN mkdir -p /code/data/notes

# Expose app port (Hugging Face uses $PORT by default)
EXPOSE 7860

# Set default CMD: Use env PORT if given, else 7860
CMD [ "sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-7860}" ]


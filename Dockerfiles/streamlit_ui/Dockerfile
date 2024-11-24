FROM docker.io/python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY . .


RUN python -m venv venv && \
    . venv/bin/activate && \
    pip install --upgrade pip && \
    pip install -r requirements.txt


CMD ["./venv/bin/streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
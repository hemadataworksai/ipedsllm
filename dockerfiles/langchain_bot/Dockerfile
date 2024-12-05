FROM docker.io/python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/root_dir

WORKDIR /root_dir

COPY apps/langchain_bot/requirements.txt ./apps/langchain_bot/requirements.txt

RUN pip install --upgrade pip && \
    pip install -r ./apps/langchain_bot/requirements.txt

# Install system dependencies and clean up to keep the image size small
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    vim

ADD apps/langchain_bot ./apps/langchain_bot


CMD ["python", "apps/langchain_bot/app_run.py"]
FROM python:3.9-slim-buster
LABEL authors="sezen"

WORKDIR /app

RUN apt-get update && apt-get install -y \
    ffmpeg \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && rm -rf /tmp/* \
    && rm -rf /var/tmp/*

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py ./
COPY photos_and_videos ./photos_and_videos/
COPY bot_handlers ./bot_handlers/

ENV PYTHONUNBUFFERED=1

CMD ["python", "main.py"]

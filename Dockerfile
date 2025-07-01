FROM python:3.9-slim-buster
LABEL authors="sezen"

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py ./
COPY photos_and_videos ./photos_and_videos/
COPY bot_handlers ./bot_handlers/

ENV PYTHONUNBUFFERED=1

CMD ["python", "main.py"]

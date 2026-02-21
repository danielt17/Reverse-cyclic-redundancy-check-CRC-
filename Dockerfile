FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY pyproject.toml README.md LICENSE requirements.txt ./
COPY src ./src
COPY tests ./tests

RUN python -m pip install --upgrade pip \
    && pip install -e ".[dev]"

ENTRYPOINT ["python", "-m", "crc_reverse"]

FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y build-essential gcc && rm -rf /var/lib/apt/lists/*

ENV PYTHONPATH=/app/src

COPY pyproject.toml ./
RUN apt-get update && apt-get install -y curl && curl -I https://pypi.org && \
    pip install --upgrade pip setuptools wheel && pip install --no-cache-dir .

COPY . .
RUN chmod +x /app/start_fastapi.sh

EXPOSE 29950

CMD ["./start_fastapi.sh"]

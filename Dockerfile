FROM python:3.12-slim

WORKDIR /app

ENV PYTHONPATH=/app/src

COPY pyproject.toml ./
RUN pip install --no-cache-dir .

COPY . .
RUN chmod +x /app/start_fastapi.sh

EXPOSE 29950

CMD ["./start_fastapi.sh"]

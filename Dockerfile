FROM python:3.12-slim
WORKDIR /app
COPY python/ python/
COPY telemetry.jsonl ./telemetry.jsonl
EXPOSE 8080
CMD ["python", "-m", "python.health_api"]

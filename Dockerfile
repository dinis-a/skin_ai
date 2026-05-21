FROM python:3.12-slim

RUN groupadd -r appuser && useradd -r -g appuser -s /bin/false appuser

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p /app/logs /app/photos && chown -R appuser:appuser /app

USER appuser

CMD ["python3", "main.py"]

# OPTIMIZED
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

RUN pip install pytest

CMD ["python", "app.py"]

FROM python:3.9-slim
WORKDIR /app

COPY requirements.txt ./
COPY message_generator.py ./

COPY images/ ./images/

RUN pip install --no-cache-dir -r requirements.txt
CMD ["python", "message_generator.py"]

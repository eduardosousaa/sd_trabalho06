FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt consumer_face.py ./
RUN pip install --no-cache-dir -r requirements.txt
CMD ["python", "consumer_face.py"]

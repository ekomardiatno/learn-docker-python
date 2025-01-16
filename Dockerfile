FROM python:3.9-slim

WORKDIR /project

COPY app/ /project/app/
COPY requirements.txt .
COPY run.py .

# RUN pip install -r requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Set environment variables for production
ENV PORT=5000
ENV FLASK_ENV=development
ENV SECRET_KEY=supersecretkey
ENV REDIS_HOST=redis
ENV REDIS_PORT=6379

EXPOSE 5000

CMD ["python", "run.py"]
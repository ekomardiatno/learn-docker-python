FROM python:3.9-slim

WORKDIR /app

COPY app/ /app/

# RUN pip install -r requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Set environment variables for production
ENV FLASK_ENV=development

EXPOSE 5000

CMD ["python", "app.py"]
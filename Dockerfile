FROM python:3.9-slim

WORKDIR /app

COPY app/ /app/

# RUN pip install -r requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Set environment variables for production
ENV FLASK_ENV=development

EXPOSE 5000

# command for production environment
# CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]

CMD ["python", "app.py"]
FROM python:3.9-slim

WORKDIR /project

COPY . /project/

# RUN pip install -r requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD ["python", "run.py"]
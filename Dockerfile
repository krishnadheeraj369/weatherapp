FROM python:3.12.4-slim

EXPOSE 5002


ENV PYTHONDONTWRITEBYTECODE=1


ENV PYTHONUNBUFFERED=1


COPY requirements.txt .
RUN python -m pip install -r requirements.txt

WORKDIR /app
COPY . .

ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

#CMD ["flask", "run"]
CMD ["gunicorn", "--bind", "0.0.0.0:5002", "connecttomongo:app"]

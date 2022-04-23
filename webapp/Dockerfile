FROM python:3.7-buster

ENV PYTHONUNBUFFERED 1

WORKDIR /code
COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY . ./

Expose 8000

# CMD ["gunicorn"  , "webapp.wsgi:application". "-b", "0.0.0.0:8000", "--pid pid.txt"]
# gunicorn webapp.wsgi:application --bind 0.0.0.0:8000 -D --pid pid.txt
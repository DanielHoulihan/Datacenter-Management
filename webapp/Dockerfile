

# FROM python:3.8-alpine

# RUN apk --update add gcc build-base freetype-dev libpng-dev openblas-dev

# RUN pip install --no-cache-dir matplotlib pandas


# FROM python:3.7-alpine
# RUN apk add g++ jpeg-dev zlib-dev libjpeg make

# RUN mkdir -p /opt/app
# COPY requirements.txt /opt/app/
# WORKDIR /opt/app
# RUN pip3 install -r requirments.txt

# COPY . .


FROM python:3.7-buster
# RUN apk add g++ jpeg-dev zlib-dev libjpeg make

ENV PYTHONUNBUFFERED 1

WORKDIR /code
COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY . ./

# CMD [ "python3", "manage.py", "runserver --bind 0.0.0.0:8000"]

Expose 8000
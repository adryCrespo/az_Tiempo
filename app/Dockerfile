FROM python:3.10.0-slim
RUN mkdir -p /var/app/flask_app
WORKDIR /var/app/flask_app 
COPY requirements.txt /var/app/flask_app
RUN apt-get update && apt-get -y install curl && apt-get -y install sudo
RUN pip install --upgrade pip
# RUN pip install curl
RUN pip install --no-cache-dir -r requirements.txt 
COPY . /var/app/flask_app 
ENV FLASK_APP ../app.py 
RUN    /var/app/flask_app/entry-drivers.sh 
CMD exec gunicorn   -w 1 -b :8000 app:app 

 
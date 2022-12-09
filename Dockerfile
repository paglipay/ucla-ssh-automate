FROM python:3.10.9

RUN apt-get update && apt-get install -y zbar-tools ffmpeg libsm6 libxext6
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /usr/src/app

CMD [ "python", "./app.py" ]

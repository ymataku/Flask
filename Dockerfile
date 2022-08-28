# pythonのバージョンは任意
FROM python:3.8

WORKDIR /usr/src/app
ENV FLASK_APP=app
ENV FLASK_DEBUG 1

COPY /app/requirements.txt ./

RUN curl https://cli-assets.heroku.com/install.sh | sh
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN apt update
RUN apt install -y fonts-ipafont
# COPY /usr/src/app/font /usr/share/fonts

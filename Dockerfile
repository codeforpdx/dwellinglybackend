FROM python:3.8

ENV SECRET_KEY='dwellingly'
ENV PORT=5000
ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8
ENV PYTHONFAULTHANDLER 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV FLASK_SERVER_PORT=5000
EXPOSE 3000
EXPOSE 5000

WORKDIR /root
RUN apt-get update -y && apt-get install -y
COPY ./requirements.txt /root/requirements.txt
RUN pip3 install -r requirements.txt
COPY . .

ENTRYPOINT ["./docker_bash.sh"]

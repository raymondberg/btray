FROM python:2.7

RUN apt-get update
RUN apt-get install -y \
      libpq-dev \
      nginx \
      vim \
      python-dev \
      python-pip

ADD ./requirements.txt /var/app/requirements.txt
RUN pip install -r /var/app/requirements.txt

ADD . /var/app
WORKDIR "/var/app"
EXPOSE 8000

CMD ["bash"]

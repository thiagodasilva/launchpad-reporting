FROM centos:7
MAINTAINER Thiago da Silva

RUN yum -y upgrade
RUN yum -y install git gcc python-devel python-setuptools openssl-devel
RUN easy_install pip

COPY . /app
WORKDIR /app

RUN pip install --upgrade -r requirements.txt

CMD ["main.py"]
ENTRYPOINT ["python"]

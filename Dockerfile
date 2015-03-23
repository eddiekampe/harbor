FROM python:2.7-slim
MAINTAINER Eddie Kämpe <eddiek@kth.se>

RUN apt-get update && \
    apt-get install -y git

RUN git clone https://github.com/eddiekampe/harbor.git /opt/harbor
WORKDIR /opt/harbor

RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["python", "harbor.py"]
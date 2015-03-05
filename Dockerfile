FROM python:2.7-slim
MAINTAINER Eddie Kämpe <eddiek@kth.se>

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY . .
RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["python", "harbor.py"]

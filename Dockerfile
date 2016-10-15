FROM python:3.4-onbuild

WORKDIR /project
ADD . /project

EXPOSE 80

CMD python server.py


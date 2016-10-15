FROM python:onbuild

WORKDIR /project
ADD . /project

RUN python -m unittest *Test.py

EXPOSE 80

CMD python server.py


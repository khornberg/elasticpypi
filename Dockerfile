FROM python:2@sha256:f70aa51df5e8c7b6fd04a9910cbb8170c9257265b2ab4419e4c4d3bcab044ec9
MAINTAINER Shaun Martin <shaun@samsite.ca>

VOLUME /code

ADD requirements.txt /tmp/
ADD test-requirements.txt /tmp/

RUN pip install -r /tmp/requirements.txt && \
    pip install -r /tmp/test-requirements.txt

CMD cd /code && python -m pytest
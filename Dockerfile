FROM python:2@sha256:de3d5c9af1065270242f5e4cbf043fe7c6cf46041a830f1fee9b9bcca6e7a7d8
MAINTAINER Shaun Martin <shaun@samsite.ca>

VOLUME /code

ADD requirements.txt /tmp/
ADD test-requirements.txt /tmp/

RUN pip install -r /tmp/requirements.txt && \
    pip install -r /tmp/test-requirements.txt

CMD cd /code && python -m pytest
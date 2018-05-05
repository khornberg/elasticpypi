FROM python:2@sha256:6d2016499edaedd0f7aa8a20aef2e305f75592b3ed6b79301578a4a8b1a91df3
MAINTAINER Shaun Martin <shaun@samsite.ca>

VOLUME /code

ADD requirements.txt /tmp/
ADD test-requirements.txt /tmp/

RUN pip install -r /tmp/requirements.txt && \
    pip install -r /tmp/test-requirements.txt

CMD cd /code && python -m pytest
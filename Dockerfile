FROM python:2@sha256:1b424a23e059c1bb72ef180964a9baf8b9c13e768ddf8faaa770e7adc3e4eb9e
MAINTAINER Shaun Martin <shaun@samsite.ca>

VOLUME /code

ADD requirements.txt /tmp/
ADD test-requirements.txt /tmp/

RUN pip install -r /tmp/requirements.txt && \
    pip install -r /tmp/test-requirements.txt

CMD cd /code && python -m pytest
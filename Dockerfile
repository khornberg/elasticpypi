FROM python:2@sha256:8907ce99826e948f535e9e2524225a8c5b2d273f2b223c7fe7d82e1fb41efdc3
MAINTAINER Shaun Martin <shaun@samsite.ca>

VOLUME /code

ADD requirements.txt /tmp/
ADD test-requirements.txt /tmp/

RUN pip install -r /tmp/requirements.txt && \
    pip install -r /tmp/test-requirements.txt

CMD cd /code && python -m pytest
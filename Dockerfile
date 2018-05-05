FROM python:2@sha256:e8ad5f06aa0e6a1a0f1ab8142ed624fd72c2bdb85a7cfcfb083837df8d2c6bb7
MAINTAINER Shaun Martin <shaun@samsite.ca>

VOLUME /code

ADD requirements.txt /tmp/
ADD test-requirements.txt /tmp/

RUN pip install -r /tmp/requirements.txt && \
    pip install -r /tmp/test-requirements.txt

CMD cd /code && python -m pytest
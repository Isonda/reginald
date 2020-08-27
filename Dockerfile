FROM ubuntu:18.04
ENV PRODUCTION yes

RUN apt-get update && apt-get install -y \
    dumb-init \
    build-essential \
    python3.7 \
    python3.7-dev \
    python3-pip && \
    apt-get clean

ADD requirements.txt /code/
RUN pip3 install --upgrade pip
RUN pip3 --version
RUN pip3 install -r /code/requirements.txt
ADD . /code
ENTRYPOINT ["/usr/bin/dumb-init", "--"]
CMD ["./code/start.sh"]

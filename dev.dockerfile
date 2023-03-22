FROM docker.io/library/ubuntu:20.04
ARG DEBIAN_FRONTEND=noninteractive

RUN true \
    && apt update -y \
    && apt install -y \
        gettext-base \
        git \
        nodejs \
        npm \
        rsync \
        software-properties-common \
    && add-apt-repository ppa:deadsnakes/ppa \
    && apt install -y \
        python2.7 \
        python3.5 python3.5-venv \
        python3.6 python3.6-venv \
        python3.7 python3.7-venv  \
        python3.8 python3.8-venv \
        python3.9 python3.9-venv \
        python3.10 python3.10-venv \
        python3.11 python3.11-venv \
    && rm -rf /var/lib/apt/lists/* \
    && true

ENV VIRTUAL_ENV=/opt/venv
RUN python3.11 -m venv "${VIRTUAL_ENV}"
ENV PATH="${VIRTUAL_ENV}/bin:${PATH}"

COPY requirements-dev.txt /tmp/
RUN pip install -r /tmp/requirements-dev.txt

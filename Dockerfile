FROM python:3.8.0-slim AS build

LABEL description="Dev image to test ftoolz installation and packaging"
LABEL maintainer="martin.matyasek@blindspot.ai"

ENV SRC_DIR /ftoolz

WORKDIR $SRC_DIR

RUN apt update && apt install -y build-essential

COPY Makefile setup.py $SRC_DIR/
RUN make setup

COPY . $SRC_DIR/
RUN make release-build

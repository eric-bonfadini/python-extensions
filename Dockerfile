FROM python:3.9.9-slim as base_image

RUN apt-get update && apt-get install -y curl xz-utils build-essential debconf locales locales-all git file && apt-get clean

ENV LANGUAGE=en_US.UTF-8
ENV LC_ALL=en_US.UTF-8
ENV LANG=en_US.UTF-8
RUN locale-gen en_US.UTF-8
RUN dpkg-reconfigure locales

# install rust 1.57.0
RUN cd /usr/local && curl -sL https://static.rust-lang.org/dist/rust-1.57.0-x86_64-unknown-linux-gnu.tar.gz | tar xfz -
RUN /usr/local/rust-1.57.0-x86_64-unknown-linux-gnu//install.sh

# install go 1.17.6
RUN cd /usr/local && curl -sL https://go.dev/dl/go1.17.6.linux-amd64.tar.gz | tar xfz -
ENV PATH=$PATH:/usr/local/go/bin


RUN groupadd -g 501 user
RUN useradd -m -u 501 user -d /home/user/ -g user -p password

USER user:user

RUN python3 -m venv /home/user/env_python-ext_3.9.9
ENV PATH=/home/user/env_python-ext_3.9.9/bin:$PATH
RUN pip install -U pip wheel

RUN mkdir -p /tmp/data/

# setup go
ENV GOPATH=/home/user/go
ENV PATH=$PATH:$GOPATH/bin
RUN go get golang.org/x/tools/cmd/goimports
RUN go get github.com/go-python/gopy

ENV NLS_LANG=.AL32UTF8

ENV PYTHONUNBUFFERED 1

CMD ["bash"]

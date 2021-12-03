FROM python:3.9.9-slim as base_image

RUN apt-get update && apt-get install -y wget xz-utils build-essential debconf locales locales-all git file && apt-get clean

ENV LANGUAGE=en_US.UTF-8
ENV LC_ALL=en_US.UTF-8
ENV LANG=en_US.UTF-8
RUN locale-gen en_US.UTF-8
RUN dpkg-reconfigure locales

# install rust 1.57.0
RUN wget -P /tmp/ https://static.rust-lang.org/dist/rust-1.57.0-x86_64-unknown-linux-gnu.tar.gz && tar -C /usr/local -xzf /tmp/rust-1.57.0-x86_64-unknown-linux-gnu.tar.gz && /usr/local/rust-1.57.0-x86_64-unknown-linux-gnu//install.sh && rm -f /tmp/rust-1.57.0-x86_64-unknown-linux-gnu.tar.gz && rm -rf /usr/local/rust-1.57.0*


RUN groupadd -g 501 user
RUN useradd -m -u 501 user -d /home/user/ -g user -p password

USER user:user

RUN python3 -m venv /home/user/env_python-ext_3.9.9
ENV PATH=/home/user/env_python-ext_3.9.9/bin:$PATH
RUN pip install -U pip wheel

RUN mkdir -p /tmp/data/

ENV NLS_LANG=.AL32UTF8

ENV PYTHONUNBUFFERED 1

CMD ["bash"]

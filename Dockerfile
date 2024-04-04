FROM ubuntu:22.04
RUN apt update && \
    DEBIAN_FRONTEND=noninteractive apt install -y\
        git \
        ipython3 \
        ffmpeg \
        python3 \
        curl \
        && \
    apt autoremove -y
RUN apt update && apt install -y python3-pip && apt autoremove -y
RUN python3 -m pip install internetarchive
RUN curl -LOs https://archive.org/download/ia-pex/ia && \
    chmod +x ./ia && \
    mv ./ia /usr/bin/ia

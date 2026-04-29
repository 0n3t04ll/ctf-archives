FROM ubuntu:22.04

RUN apt-get update && apt-get install -y \
    qemu-user \
    socat \
    libc6-armel-cross \
    && rm -rf /var/lib/apt/lists/*

RUN useradd -m ctf

WORKDIR /home/ctf

COPY echo .
COPY flag.txt .

RUN chmod +x echo

EXPOSE 1337

CMD socat TCP-LISTEN:1337,reuseaddr,fork EXEC:"qemu-arm -L /usr/arm-linux-gnueabi ./echo",stderr

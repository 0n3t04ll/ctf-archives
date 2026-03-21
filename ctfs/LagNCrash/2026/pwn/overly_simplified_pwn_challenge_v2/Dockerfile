FROM alpine:3.21 AS builder

RUN apk add --no-cache gcc musl-dev socat

WORKDIR /build
COPY main.c .

RUN gcc -o main main.c -no-pie -fno-stack-protector

RUN adduser -D -h /home/user user
RUN mv /build/main /home/user/main
COPY flag.txt /home/user/flag.txt

RUN chown -R root:root /home/user && \
    chmod 755 /home/user && \
    chmod 755 /home/user/main && \
    chmod 444 /home/user/flag.txt

EXPOSE 1337
WORKDIR /home/user
CMD ["socat", "-T60", "TCP-LISTEN:1337,reuseaddr,fork", "EXEC:/home/user/main,su=user,stderr"]

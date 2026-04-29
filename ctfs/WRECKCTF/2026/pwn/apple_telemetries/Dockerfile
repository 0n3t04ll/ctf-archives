# Built with:
#    gcc apple_telemetries.c -o apple_telemetries -Wl,-z,relro,-z,now -Wl,-rpath,. -Wl,--dynamic-linker=./ld-linux-x86-64.so.2
FROM ubuntu:24.04

RUN apt-get update && apt-get install -y --no-install-recommends \
    socat \
    && rm -rf /var/lib/apt/lists/*

RUN useradd -m ctfuser
WORKDIR /home/ctfuser

COPY ./apple_telemetries .
COPY ./libc.so.6 .
COPY ./ld-linux-x86-64.so.2 .
COPY ./flag.txt /home/ctfuser/flag.txt

RUN chown -R root:ctfuser /home/ctfuser && \
    chmod 755 /home/ctfuser/apple_telemetries && \
    chmod 444 /home/ctfuser/flag.txt

USER ctfuser

EXPOSE 1339

CMD ["socat", "TCP-LISTEN:1339,fork,reuseaddr", "EXEC:/home/ctfuser/apple_telemetries"]

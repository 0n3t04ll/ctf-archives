FROM python:3.12-slim

RUN apt-get update \
    && apt-get install -y socat \
    && rm -rf /var/lib/apt/lists/*

RUN echo "ulimit -c 0" >> /etc/profile
RUN useradd --system --no-create-home --shell /usr/sbin/nologin hyper
WORKDIR /app
COPY flag.txt /flag.txt
COPY ouroboros.py /app/
RUN chown -R root:root /app \
    && chmod -R 555 /app
EXPOSE 1337
USER hyper
CMD ["socat", "TCP-LISTEN:1337,reuseaddr,fork", "EXEC:python3 -u /app/ouroboros.py"]

FROM ubuntu:24.04@sha256:c4a8d5503dfb2a3eb8ab5f807da5bc69a85730fb49b5cfca2330194ebcc41c7b AS app

FROM pwn.red/jail
COPY --from=app / /srv
RUN mkdir -p /srv/app

COPY buzzvm /srv/app/run
COPY flag.txt /srv/app/flag.txt

RUN chmod 755 /srv/app/run
RUN chmod 644 /srv/app/flag.txt

ENV JAIL_TIME=60

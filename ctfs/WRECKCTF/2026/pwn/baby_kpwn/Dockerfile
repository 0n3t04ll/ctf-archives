FROM ubuntu:24.04@sha256:c4a8d5503dfb2a3eb8ab5f807da5bc69a85730fb49b5cfca2330194ebcc41c7b AS build
RUN apt-get update -y && apt-get install -y --no-install-recommends \
        ca-certificates make gcc libc6-dev gcc-riscv64-linux-gnu binutils-riscv64-linux-gnu git \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /src
RUN git clone https://github.com/mit-pdos/xv6-riscv.git . && \
    git checkout 5474d4bf72fd95a6e5c735c2d7f208f58990ceab
COPY patch.diff /tmp/patch.diff
COPY flag.txt /tmp/flag.txt
RUN git apply /tmp/patch.diff
RUN sed -i "s/wreck{REDACTED}/$(cat /tmp/flag.txt)/" kernel/main.c
RUN make CPUS=2 TOOLPREFIX=riscv64-linux-gnu- kernel/kernel fs.img

FROM ubuntu:24.04@sha256:c4a8d5503dfb2a3eb8ab5f807da5bc69a85730fb49b5cfca2330194ebcc41c7b AS app
RUN apt-get update -y && apt-get install -y --no-install-recommends \
        qemu-system-misc ca-certificates coreutils \
    && rm -rf /var/lib/apt/lists/*
COPY --from=build /src/kernel/kernel /app/kernel
COPY --from=build /src/mkfs/mkfs /app/mkfs
COPY --from=build /src/user/_init /app/uprogs/_init
COPY run.sh /app/run
RUN chmod 755 /app/run /app/mkfs

FROM pwn.red/jail
COPY --from=app / /srv
RUN mkdir -p /srv/tmp
ENV JAIL_TIME=600
ENV JAIL_TMP_SIZE=64M
ENV JAIL_MEM=512M
ENV JAIL_PIDS=64
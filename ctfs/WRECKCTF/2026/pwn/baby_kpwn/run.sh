#!/bin/sh
set -eu
DIR="$(cd "$(dirname "$0")" && pwd)"

head -1 | base64 -d > /tmp/exploit.elf

mkdir -p /tmp/build/user
cp "$DIR/uprogs/_init" /tmp/build/user/
cp /tmp/exploit.elf /tmp/build/user/_exploit

cd /tmp/build
"$DIR/mkfs" /tmp/fs.img user/_init user/_exploit

exec qemu-system-riscv64 \
    -machine virt -bios none -kernel "$DIR/kernel" \
    -m 128M -smp 2 -nographic \
    -global virtio-mmio.force-legacy=false \
    -drive "file=/tmp/fs.img,if=none,format=raw,id=x0" \
    -device virtio-blk-device,drive=x0,bus=virtio-mmio-bus.0
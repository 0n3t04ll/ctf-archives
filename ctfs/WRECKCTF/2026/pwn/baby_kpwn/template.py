#!/usr/bin/env python3
from pwn import *
import base64

HOST = "challs.wreckctf.com"
PORT = 0  # fill in

# Cross-compile your exploit:
#   cd xv6-riscv && make CPUS=2 TOOLPREFIX=riscv64-linux-gnu-
# Your binary will be at user/_exploit

EXPLOIT_PATH = "xv6-riscv/user/_exploit"

def main():
    elf = open(EXPLOIT_PATH, "rb").read()

    io = remote(HOST, PORT)
    io.sendline(base64.b64encode(elf))
    io.interactive()

if __name__ == "__main__":
    main()

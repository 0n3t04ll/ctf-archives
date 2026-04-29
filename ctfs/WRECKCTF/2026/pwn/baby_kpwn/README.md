AmIAHuman
baby's first kernel pwn. xv6-riscv with shared memory that doesn't quite work right.

send a base64-encoded RISC-V ELF on a single line. xv6 boots and runs it.


# baby-kpwn

## Protocol

Send a base64-encoded RISC-V ELF binary on a single line.
xv6 boots with your binary on the filesystem and runs it automatically.

## Building a binary

```
git clone https://github.com/mit-pdos/xv6-riscv.git
cd xv6-riscv
git checkout 5474d4bf72fd95a6e5c735c2d7f208f58990ceab
git apply ../patch.diff
```

Write your program as `user/exploit.c`, add `$U/_exploit` to `UPROGS` in the
Makefile, then build:

```
make CPUS=2 TOOLPREFIX=riscv64-linux-gnu-
```

Your binary is at `user/_exploit`.

## Submitting

See `template.py` for a pwntools stub.

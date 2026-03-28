I can't seem to link this object file correctly... I think some of my array sizes might be off?

$ mips-linux-gnu-gcc main.c flagchecker.o -fno-toplevel-reorder -static && qemu-mips ./a.out

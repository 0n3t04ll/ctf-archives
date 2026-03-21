// gcc -o chal chal.c -Wl,-z,relro,-z,now
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <stdint.h>
#include <signal.h>
#include <string.h>

void handle() {
        system("/bin/sh");
        _exit(1);
}

int main() {
        signal(SIGSEGV, handle);
        setbuf(stdin, NULL);
        setbuf(stdout, NULL);
        uint64_t mem=0;
        scanf("%lld", &mem);
        char* heap = malloc(mem);
        printf("heap @ %llx\n", heap);
        memset(heap, 0, mem);
        fgets(heap, UINT64_MAX, stdin);
        free(heap);
        _exit(0);
}

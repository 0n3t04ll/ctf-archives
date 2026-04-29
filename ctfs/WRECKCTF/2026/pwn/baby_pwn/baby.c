#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

void win(void) {
    char buf[128];
    FILE *f = fopen("flag.txt", "r");
    if (!f) {
        puts("flag.txt missing");
        exit(1);
    }
    size_t n = fread(buf, 1, sizeof(buf) - 1, f);
    buf[n] = '\0';
    fputs(buf, stdout);
    fclose(f);
}

void vuln(void) {
    char buf[64];
    puts("whisper your secret:");
    gets(buf);
    printf("thanks, %s\n", buf);
}

int main(void) {
    setbuf(stdout, NULL);
    puts("welcome to baby-pwn");
    vuln();
    puts("bye");
    return 0;
}

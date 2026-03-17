#include <stdio.h>
#include <unistd.h>

void vuln() {
    char buf[64];
    write(1, "[WARD-COMM v1.3] Diagnostic mode active. Transmit message:\n", 59);
    read(0, buf, 1000);
}

int main() {
    vuln();
    return 0;
}

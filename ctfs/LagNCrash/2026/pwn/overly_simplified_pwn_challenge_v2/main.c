#include <stdio.h>
#include <unistd.h>

int __attribute__((used)) gift(void)  {
  __asm__("mov %rdx, %rax ; ret");
  __asm__("pop %rbx ; ret");
}

int main(void) {
  char buf[0x50];
  read(0, buf, 0x1000);
  return 0;
}

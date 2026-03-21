#include "vm.h"
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <stdint.h>

#include <stddef.h>
#include <linux/seccomp.h>
#include <linux/filter.h>
#include <linux/audit.h>
#include <sys/prctl.h>
#include <sys/syscall.h>

#define DENY_SYSCALL(name) \
    BPF_JUMP(BPF_JMP | BPF_JEQ | BPF_K, __NR_##name, 0, 1), \
    BPF_STMT(BPF_RET | BPF_K, SECCOMP_RET_KILL_PROCESS)


#define MAX_NOTES 0x10
#define TRAIN_THRESHOLD 3

struct Mem {
    char   *notes[MAX_NOTES];
    size_t  sizes[MAX_NOTES];
};

static struct Mem memory;
static VM *vm;

static const char menu_str[] =
    "1. create a note\n"
    "2. delete a note\n"
    "3. read a note\n"
    "4. edit a note\n"
    "5. exit\n";

int install_seccomp(void) {
    struct sock_filter filter[] = {
        /* Load syscall number */
        BPF_STMT(BPF_LD | BPF_W | BPF_ABS,
                 offsetof(struct seccomp_data, nr)),

        /* Deny execve family */
        DENY_SYSCALL(execve),
        DENY_SYSCALL(execveat),

        /* Allow everything else */
        BPF_STMT(BPF_RET | BPF_K, SECCOMP_RET_ALLOW),
    };

    struct sock_fprog prog = {
        .len = (unsigned short)(sizeof(filter) / sizeof(filter[0])),
        .filter = filter,
    };

    prctl(PR_SET_NO_NEW_PRIVS, 1, 0, 0, 0);
    return prctl(PR_SET_SECCOMP, SECCOMP_MODE_FILTER, &prog);
}


static int get_int(const char *prompt) {
    char buf[0x100];
    write(1, prompt, strlen(prompt));
    read(0, buf, sizeof(buf));
    buf[strcspn(buf, "\n")] = 0;
    return atoi(buf);
}

static size_t get_size(const char *prompt) {
    char buf[0x100];
    write(1, prompt, strlen(prompt));
    read(0, buf, sizeof(buf));
    buf[strcspn(buf, "\n")] = 0;
    return strtoull(buf, NULL, 10);
}

static int get_index(const char *prompt) {
    int idx = get_int(prompt);
    if (idx < 0 || idx >= MAX_NOTES)
        _exit(1);
    return idx;
}

static void menu(void) {
    write(1, menu_str, strlen(menu_str));
}

enum {
    ENTRY_DISPATCH = 0x0,
    ENTRY_GIFT   = 0x50,
    ENTRY_CREATE = 0x100,
    ENTRY_DELETE = 0x200,
    ENTRY_READ   = 0x300,
    ENTRY_EDIT   = 0x400,
};

static Instruction program[] = {
    [ENTRY_DISPATCH] = INST(OP_CALL, 0, 0, ENTRY_CREATE),
    INST(OP_HALT, 0, 0, 0),
    INST(OP_CALL, 0, 0, ENTRY_DELETE),
    INST(OP_HALT, 0, 0, 0),
    INST(OP_CALL, 0, 0, ENTRY_READ),
    INST(OP_HALT, 0, 0, 0),
    INST(OP_CALL, 0, 0, ENTRY_EDIT),
    INST(OP_HALT, 0, 0, 0),

    [ENTRY_CREATE] = INST(OP_ENTER, 0, 0, 0),

    INST(OP_PUSH, R0, 0, 0),
    INST(OP_MOV,   R0, R1, 0),              
    INST(OP_LOADI, R7, 0, SYS_ALLOC),
    INST(OP_SYSCALL, 0, 0, 0),              
    INST(OP_LOADI, R5, 0, 0),               
    INST(OP_LOADI, R6, 0, 0),              

    INST(OP_POP, R0, 0, 0),
    INST(OP_STORE, R0, R7, 0),             

    INST(OP_ADD,   R0, 0, MAX_NOTES),
    INST(OP_STORE, R0, R1, 0),             

    INST(OP_LEAVE, 0, 0, 0),
    INST(OP_RET,   0, 0, 0),

    [ENTRY_DELETE] = INST(OP_ENTER, 0, 0, 0),

    INST(OP_PUSH, R0, 0, 0),
    INST(OP_LOAD,  R0, R0, 0),             
    INST(OP_LOADI, R7, 0, SYS_FREE),
    INST(OP_SYSCALL, 0, 0, 0),

    INST(OP_LOADI, R5, 0, 1),              

    INST(OP_POP, R0, 0, 0),
    INST(OP_LOADI, R7, 0, 0),
    INST(OP_STORE, R0, R7, 0),              
    INST(OP_ADD, R0, 0, MAX_NOTES),
    INST(OP_STORE, R0, R7, 0),

    INST(OP_LEAVE, 0, 0, 0),
    INST(OP_RET,   0, 0, 0),

    [ENTRY_READ] = INST(OP_ENTER, 0, 0, 0),

    INST(OP_PUSH, R0, 0, 0),
    INST(OP_MOV, R10, R0, 0),
    INST(OP_LOADI, R0, 0, 1),

    INST(OP_ADD,   R6, 0, 1),               
    INST(OP_CMP,   R6, 0, TRAIN_THRESHOLD),
    INST(OP_JG,    0, 0, ENTRY_READ + 18),
    INST(OP_JNZ,   0, 0, ENTRY_READ + 13),

    INST(OP_POP,   R2, 0, 0),
    INST(OP_ADD,   R2, 0, MAX_NOTES),
    INST(OP_LOAD,  R4, R2, 0),              
    INST(OP_LOADI, R5, 0, 1),               
    INST(OP_JMP, 0, 0, ENTRY_READ + 18),

    INST(OP_POP,   R2, 0, 0),
    INST(OP_ADD,   R2, 0, MAX_NOTES),
    INST(OP_LOAD,  R2, R2, 0),              
    INST(OP_MOV,   R3, R2, 0),
    INST(OP_JMP,   0, 0, ENTRY_READ + 19),

    INST(OP_MOV,   R3, R4, 0),              

    INST(OP_LOAD,  R10, R10, 0),
    INST(OP_MOV,   R1, R10, 0),
    INST(OP_MOV,   R2, R3, 0),

    INST(OP_LOADI, R7, 0, SYS_WRITE),
    INST(OP_SYSCALL, 0, 0, 0),

    INST(OP_LEAVE, 0, 0, 0),
    INST(OP_RET,   0, 0, 0),

    [ENTRY_EDIT] = INST(OP_ENTER, 0, 0, 0),

    INST(OP_PUSH,  R0, 0, 0),
    INST(OP_MOV, R10, R0, 0),
    INST(OP_LOADI, R0, 0, 0),

    INST(OP_ADD,   R6, 0, 1),               
    INST(OP_CMP,   R6, 0, TRAIN_THRESHOLD),
    INST(OP_JG,    0, 0, ENTRY_EDIT + 18),
    INST(OP_JNZ,   0, 0, ENTRY_EDIT + 13),

    INST(OP_POP,   R2, 0, 0),
    INST(OP_ADD,   R2, 0, MAX_NOTES),
    INST(OP_LOAD,  R4, R2, 0),              
    INST(OP_LOADI, R5, 0, 1),               
    INST(OP_JMP, 0, 0, ENTRY_EDIT + 18),

    INST(OP_POP,   R2, 0, 0),
    INST(OP_ADD,   R2, 0, MAX_NOTES),
    INST(OP_LOAD,  R2, R2, 0),              
    INST(OP_MOV,   R3, R2, 0),
    INST(OP_JMP,   0, 0, ENTRY_EDIT + 19),

    INST(OP_MOV,   R3, R4, 0),              

    INST(OP_LOAD,  R10, R10, 0),            
    INST(OP_MOV,   R1, R10, 0),             
    INST(OP_MOV,   R2, R3, 0),              

    INST(OP_LOADI, R7, 0, SYS_READ),
    INST(OP_SYSCALL, 0, 0, 0),

    INST(OP_LEAVE, 0, 0, 0),
    INST(OP_RET,   0, 0, 0),

    [ENTRY_GIFT] = INST(OP_PUSH, BP, 0, 0),
    INST(OP_POP, R7, 0, 0),
    INST(OP_ADD, SP, 0, 1),
    INST(OP_LOADI, BP, 0, 0),
    INST(OP_RET, 0, 0, 0),
};

static VM *init_vm(Instruction *prog, long *mem, size_t len) {
    VM *v = malloc(sizeof(VM));
    if (!v)
        _exit(1);

    v->memory = mem;
    v->pc = 0;
    v->frame = frame_alloc(NULL, -1, 64);
    v->zf = 0;

    v->regs[SP] = 0;
    v->regs[BP] = 0;

    for (size_t i = 0; i < len; i++)
        v->program[i] = prog[i];

    return v;
}

int main(void) {
    install_seccomp();
    vm = init_vm(
        program,
        (long *)&memory,
        sizeof(program) / sizeof(Instruction)
    );

    while (1) {
        menu();
        int choice = get_int(">> ");

        switch (choice) {
            case 1:
                REG(R0) = get_index("idx: ");
                REG(R1) = get_size("size: ");
                vm->pc = ENTRY_DISPATCH;
                break;

            case 2:
                REG(R0) = get_index("idx: ");
                vm->pc = ENTRY_DISPATCH + 2;
                break;

            case 3:
                REG(R0) = get_index("idx: ");
                vm->pc = ENTRY_DISPATCH + 4;
                break;

            case 4:
                REG(R0) = get_index("idx: ");
                vm->pc = ENTRY_DISPATCH + 6;
                break;

            case 5:
                _exit(0);

            default:
                continue;
        }

        run(vm);
    }
}


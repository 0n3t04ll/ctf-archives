#ifndef VM_IMPL
#define VM_IMPL

#include <unistd.h>
#include <string.h>
#include <sys/mman.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <stdint.h>

#define NUM_REGS 14
#define MAX_PROG 0x1000
#define MEM_SIZE 0x1000
#define HEAP_MAX 0x10000000

#define REG(i) (vm->regs[i])

typedef uint32_t Instruction;

#define OP(i)   (((i) >> 24) & 0xff)
#define A(i)    (((i) >> 20) & 0x0f)
#define B(i)    (((i) >> 16) & 0x0f)
#define IMM(i)  ((int16_t)((i) & 0xffff))

#define INST(op, a, b, imm) \
    (((op) << 24) | ((a) << 20) | ((b) << 16) | ((uint16_t)(imm)))


enum {
	R0,
	R1,
	R2,
	R3,
	R4,
	R5,
	R6,
	R7,
	R8,
	R9,
	R10,
	R11,
	SP,
	BP
};

typedef enum {
	SYS_READ,
	SYS_WRITE,
	SYS_ALLOC,
	SYS_FREE,
} Syscall;

typedef enum {
	OP_HALT,
	OP_MOV,
	OP_LOADI,
	OP_LOAD, 
	OP_STORE,
	OP_ADD,
	OP_SUB,
	OP_MUL,
	OP_DIV,
	OP_PRINT,
	OP_JMP,
	OP_CALL,
	OP_RET,
	OP_SYSCALL,
	OP_ENTER,
	OP_LEAVE,
	OP_POP,
	OP_PUSH,
	OP_JLT,
	OP_CMP,
	OP_JNZ,
	OP_JG,
} Opcode;

typedef struct {
	long regs[NUM_REGS];
	Instruction program[MAX_PROG];
	long pc;
} CPU; 

typedef struct Frame {
	long *slots;
	size_t size;
	long ret_pc;
	long saved_bp;
	struct Frame *prev;
} Frame;

typedef struct {
	long regs[NUM_REGS];
	Instruction program[MAX_PROG];
	Frame *frame;
	long pc;
	long *memory;
	int zf;
	int sf;
} VM;

void run(VM *vm);
Frame *frame_alloc(Frame *prev, long ret_pc, size_t slots);
void frame_free(Frame *f);

#endif // !VM_IMPL

#include "vm.h"
#include "alloc.h"

static int handle_read(VM *vm, int fd, char *buf, size_t size) {
	char *heap_base = (char *)vm + 0x4070;
	
	if (!((uintptr_t)buf < (uintptr_t)heap_base && (uintptr_t)buf > ((uintptr_t)heap_base + HEAP_MAX)))
		return read(fd, buf, size);
	return -1;
}

static int handle_write(VM *vm, int fd, char *buf, size_t size) {
	char *heap_base = (char *)vm + 0x4070;
	
	if (!((uintptr_t)buf < (uintptr_t)heap_base))
		return write(fd, buf, size);
	return -1;
}


static long handle_alloc(VM *vm, size_t size) {
	return (long)custom_alloc(vm, size);
}

static void handle_free(VM *vm, void *ptr) {
	free(ptr);
}

static void handle_syscall(VM *vm, Instruction instr) {
	switch (REG(R7)) {
		case SYS_READ: 
			REG(R7) = handle_read(vm, REG(R0), (char*)REG(R1), (size_t)REG(R2));
			break;
		case SYS_WRITE:
			REG(R7) = handle_write(vm, REG(R0), (char*)REG(R1), (size_t)REG(R2));
			break;
		case SYS_ALLOC:
			REG(R7) = handle_alloc(vm, (size_t)REG(R0));
			break;
		case SYS_FREE:
			handle_free(vm, (void*)REG(R0));
			break;
		default: 
			_exit(1);
	}
}

Frame *frame_alloc(Frame *prev, long ret_pc, size_t slots) {
    Frame *f = malloc(sizeof(Frame));
    if (!f) _exit(1);

    f->slots = calloc(slots, sizeof(long));
    if (!f->slots) _exit(1);

    f->size = slots;
    f->ret_pc = ret_pc;
    f->saved_bp = 0;
    f->prev = prev;

    return f;
}

void frame_free(Frame *f) {
    free(f->slots);
    free(f);
}

static void handle_call(VM *vm, Instruction instr) {
	Frame *newf = frame_alloc(
		vm->frame,
		vm->pc,
		64
	);

	vm->frame = newf;
	REG(SP) = 0;
	REG(BP) = 0;
	vm->pc = IMM(instr);
}

static void handle_ret(VM *vm) {
	if (!vm->frame)
		_exit(1);
	Frame *cur = vm->frame;
	vm->pc = cur->ret_pc;
	vm->frame = cur->prev;
	frame_free(cur);

	if (!vm->frame) {
		return;
	}
}

static void handle_enter(VM *vm) {
	Frame *f = vm->frame;
	if (!f) _exit(1);

	if (REG(SP) + 1 >= f->size)
		_exit(1);

	f->slots[REG(SP)++] = REG(BP);
	REG(BP) = REG(SP);
}

static void handle_leave(VM *vm) {
	Frame *f = vm->frame;
	if (!f) _exit(1);

	REG(SP) = REG(BP);
	REG(BP) = f->slots[--REG(SP)];
}

void run(VM *vm) {
	while (1) {
		if (vm->pc >= MAX_PROG || vm->pc < 0) {
			write(1, "[!] bad pc\n", 11);
			_exit(1);
		}
		Instruction instr = vm->program[vm->pc++];

		switch (OP(instr)) {
			case OP_HALT: return;
			case OP_MOV: REG(A(instr)) = REG(B(instr)); break;
			case OP_LOADI: REG(A(instr)) = IMM(instr); break;
			case OP_ADD: REG(A(instr)) += IMM(instr); break;
			case OP_SUB: REG(A(instr)) -= IMM(instr); break;
			case OP_MUL: REG(A(instr)) *= IMM(instr); break;
			case OP_DIV: REG(A(instr)) /= IMM(instr); break;
			case OP_JMP: vm->pc = IMM(instr); break;
			case OP_CALL: 
				handle_call(vm, instr);
				break;
			case OP_RET:
				handle_ret(vm);
				break;
			case OP_LOAD:
				REG(A(instr)) = vm->memory[REG(B(instr))];
				break;
			case OP_STORE:
				vm->memory[REG(A(instr))] = REG(B(instr));
				break;
			case OP_SYSCALL:
				handle_syscall(vm, instr);
				break;
			case OP_ENTER:
				handle_enter(vm);
				break;
			case OP_LEAVE:
				handle_leave(vm);
				break;
			case OP_PUSH:
				vm->frame->slots[REG(SP)++] = REG(A(instr));
				break;
			case OP_POP:
				REG(A(instr)) = vm->frame->slots[--REG(SP)];
				break;
			case OP_JLT:
				if (REG(A(instr)) < REG(B(instr)))
					vm->pc = IMM(instr);
				break;
			case OP_CMP:
				vm->zf = ((REG(A(instr))) == IMM(instr));
				vm->sf = ((REG(A(instr))) < IMM(instr));
				break;
			case OP_JNZ:
				if (vm->zf == 0)
					vm->pc = IMM(instr);
				break;
			case OP_JG:
				if (!vm->sf && !vm->zf)
					vm->pc = IMM(instr);
				break;
			default:
				_exit(1);
		}
	}
}


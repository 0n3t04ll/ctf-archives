#include "alloc.h"

void *custom_alloc(VM *vm, size_t size) {
	long resp = (long)malloc(size);
	
	if ((resp <= (long)vm + 0x4070) || (resp >= ((long)(vm) + HEAP_MAX))) {
		free((void*)resp);
		return NULL;
	}
		
	return (void*)resp;
}

void custom_free(VM *vm, void* ptr) {
	return free(ptr);
}

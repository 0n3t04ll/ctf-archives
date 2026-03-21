#ifndef ALLOC_IMPL
#define ALLOC_IMPL

#include <sys/mman.h>
#include <stddef.h>
#include <stdlib.h>

#include "vm.h"

void *custom_alloc(VM *vm, size_t size);
void custom_free(VM *vm, void* ptr);

#endif // !ALLOC_IMPL

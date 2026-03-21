import ctypes

def hyperboros():
    offset = int(input('offset\n>> '))
    char = bytes.fromhex(input('char\n>> '))
    assert len(char) == 1
    ctypes.memmove(id(hyperboros.__code__) + offset, char, len(char))

for i in range(1, 1000):
    hyperboros()

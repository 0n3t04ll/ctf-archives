import string

def str_to_bits(s):
    b = []
    for char in s:
        a = bin(ord(char))[2:].zfill(8)
        for _ in a:
            b.append(int(_))
    return b

def xor(list_of_vecs):
    i = [0 for i in range(8)]
    for vec in list_of_vecs:
        for j in range(8):
            i[j] ^= vec[j]
    return i

def step_lfsr(state, taps):
    out_bit = state[-1]
    new_state = [0] + state[:-1]
    if out_bit == 1:
        for i in range(len(new_state)):
            if taps[i] == 1:
                new_state[i] ^= 1
    return new_state

def simulate(state, taps, count):
    for i in range(count):
        state = step_lfsr(state, taps)
    return state

flag = open('flag.txt', 'r').read().strip('\n')
print(len(flag), flag)
assert len(flag) == 64
assert all([i in string.printable for i in flag])

taps = str_to_bits(flag[:16])
taps[0] = 1 # necessary so the lfsr doesnt just zero itself out
states = str_to_bits(flag[16:32]), str_to_bits(flag[32:48]), str_to_bits(flag[48:64])

out_txt = open('out.txt', 'w')
for state in states:
    a, b = simulate(state, taps, 10000), simulate(state, taps, 20000)
    out_txt.write(str(a))
    out_txt.write('\n')
    out_txt.write(str(b))
    out_txt.write('\n')
out_txt.close()

sizeT  = 3             
sizeW  = 3             
poly    = (2, 0, 1, 1)  
poly2   = ((2, 0, 1), (1, 2, 0), (0, 2, 1), (2, 0, 1)) 
cons    = ((1, 2, 0), (2, 0, 1), (1, 1, 1))     
cons2  = ((0, 0, 2), (2, 2, 1), (2, 2, 2))     
box    = (9, 10, 11, 1, 2, 0, 20, 18, 19, 3, 4, 5, 22, 23, 21, 14, 12, 26, 24, 25, 13, 16, 17, 15, 8, 6, 7)
len = 8

def down(array): 
    return sum(array, ())

def up(array, size, filler): 
    l = len(array)
    array += (filler,) * (-l % size)
    return tuple([array[i:i + size] for i in range(0, l, size)])

def look(array):
    if type(array) is int:
        return array
    while type(array[0]) is not int:
        array = down(array)
    return sum(array)

def clean(array):
    while len(array) > 1:
        if look(array[-1]):
            break
        array = array[:-1]
    return tuple(array)

def int_to_tri(num):    
    out = []
    while num:
        num, trit = divmod(num, 3)
        out.append(trit)
    return tuple(out) if out else (0,)

def tri_to_int(tri):
    out = 0
    for i in tri[::-1]:
        out *= 3
        out += i
    return out

tri_to_tyt  = lambda tri: up(tri, sizeT, 0)
tyt_to_tri  = lambda tyt: down(tyt)

int_to_tyt  = lambda num: tri_to_tyt(int_to_tri(num))
tyt_to_int  = lambda tyt: tri_to_int(down(tyt))

tyt_to_wrd  = lambda tyt: up(tyt, sizeW, (0,) * sizeT)
wrd_to_tyt  = lambda wrd: down(wrd)

def apply(func, filler=None):    
    def wrapper(a, b):
        return tuple(func(i, j) for i, j in zip(a, b))
    return wrapper

xor     = lambda a, b: (a + b) % 3
uxor    = lambda a, b: (a - b) % 3
t_xor   = apply(xor)
t_uxor  = apply(uxor)
T_xor   = apply(t_xor)
T_uxor  = apply(t_uxor)
W_xor   = apply(T_xor)
W_uxor  = apply(T_uxor)

def tri_mul(A, B):
    c = [0] * len(B)
    for a in A[::-1]:
        c = [0] + c
        x = tuple(b * a % 3 for b in B)
        c[:len(x)] = t_xor(c, x)
    return clean(c)

def tri_divmod(A, B):
    B = clean(B)
    A2  = list(A)
    c   = [0]
    while len(A2) >= len(B):
        c = [0] + c
        while A2[-1]:
            A2[-len(B):] = t_uxor(A2[-len(B):], B)
            c[0] = xor(c[0], 1)
        A2.pop()
    return clean(c), clean(A2) if sum(A2) else (0,)

def tri_mulmod(A, B, mod=poly):
    c = [0] * (len(mod) - 1)
    for a in A[::-1]:
        c = [0] + c
        x = tuple(b * a % 3 for b in B)
        c[:len(x)] = t_xor(c, x)
        while c[-1]:
            c[:] = t_xor(c, mod)
        c.pop()
    return tuple(c)

def egcd(a, b):
    x0, x1, y0, y1 = (0,), (1,), b, a
    while sum(y1):
        q, _ = tri_divmod(y0, y1)
        u, v = tri_mul(q, y1), tri_mul(q, x1)
        x0, y0 = x0 + (0,) * len(u), y0 + (0,) * len(v)
        y0, y1 = y1, clean(t_uxor(y0, u) + y0[len(u):])
        x0, x1 = x1, clean(t_uxor(x0, v) + x0[len(v):])
    return x0, y0

def modinv(a, m=poly):
    _, a = tri_divmod(a, m)
    x, y = egcd(a, m)
    if len(y) > 1:
        raise Exception('modular inverse does not exist')
    return tri_divmod(x, y)[0]

def tyt_mulmod(A, B, mod=poly2, mod2=poly):
    fil = [(0,) * sizeT]
    C = fil * (len(mod) - 1)
    for a in A[::-1]:
        C = fil + C
        x = tuple(tri_mulmod(b, a, mod2) for b in B)
        C[:len(x)] = T_xor(C, x)
        
        num = modinv(mod[-1], mod2)
        num2 = tri_mulmod(num, C[-1], mod2)
        x = tuple(tri_mulmod(m, num2, mod2) for m in mod)
        C[:len(x)] = T_uxor(C, x)

        C.pop()
    return C

int_to_byt = lambda x: x.to_bytes((x.bit_length() + 7) // 8, "big")
byt_to_int = lambda x: int.from_bytes(x, byteorder="big")

def gen_row(size = sizeW):
    out = () 
    for i in range(size):
        row = tuple(list(range(i * size, (i + 1) * size)))
        out += row[i:] + row[:i]
    return out

SHIFT_ROWS = gen_row()
UN_SHIFT_ROWS = tuple([SHIFT_ROWS.index(i) for i in range(len(SHIFT_ROWS))])

def rot_wrd(tyt):
    return tyt[1:] + tyt[:1]
    
def sub_wrd(tyt):
    return tuple(int_to_tyt(box[tri_to_int(tri)])[0] for tri in tyt)

def u_sub_wrd(tyt):
    return tuple(int_to_tyt(box.index(tri_to_int(tri)))[0] for tri in tyt)

def rcon(num): 
    out = int_to_tyt(1)
    for _ in range(num - 1):
        j = (0,) + out[-1]
        while j[-1]:
            j = t_xor(j, poly)
        out += (j[:sizeT],)
    return out

def expand(tyt):
    words   = tyt_to_wrd(tyt) 
    size    = len(words)
    rnum    = size + 3
    rcons   = rcon(rnum * 3 // size)

    for i in range(size, rnum * 3):
        k   = words[i - size]
        l   = words[i - 1]
        if i % size == 0:
            s = sub_wrd(rot_wrd(l))
            k = T_xor(k, s)
            k = (t_xor(k[0], rcons[i // size - 1]),) + k[1:]
        else:
            k = T_xor(k, l)
        words = words + (k,)

    return up(down(words[:rnum * 3]), sizeW ** 2, int_to_tyt(0)[0])

def mix_columns(tyt, cons=cons):
    tyt = list(tyt)
    for i in range(sizeW):
        tyt[i::sizeW] = tyt_mulmod(tyt[i::sizeW], cons)
    return tuple(tyt)

def a3s(msg, key): 
    m       = byt_to_int(msg)
    k       = byt_to_int(key)
    m       = up(int_to_tyt(m), sizeW ** 2, int_to_tyt(0)[0])[-1] 
    k       = int_to_tyt(k)
    keys    = expand(k)
    assert len(keys) == len

    ctt = T_xor(m, keys[0])

    for r in range(1, len(keys) - 1):
        ctt = sub_wrd(ctt)                         
        ctt = tuple([ctt[i] for i in SHIFT_ROWS])  
        ctt = mix_columns(ctt)                    
        ctt = T_xor(ctt, keys[r])              

    ctt  = sub_wrd(ctt)
    ctt  = tuple([ctt[i] for i in SHIFT_ROWS])
    ctt  = T_xor(ctt, keys[-1])                   

    ctt = tyt_to_int(ctt)
    return int_to_byt(ctt)

def d_a3s(ctt, key):
    c       = byt_to_int(ctt)
    k       = byt_to_int(key)
    c       = up(int_to_tyt(c), sizeW ** 2, int_to_tyt(0)[0])[-1] 
    k       = int_to_tyt(k)
    keys    = expand(k)[::-1]
    assert len(keys) == len

    msg = c
    msg = T_uxor(msg, keys[0])

    for r in range(1, len(keys) - 1):
        msg = tuple([msg[i] for i in UN_SHIFT_ROWS])   
        msg = u_sub_wrd(msg)                           
        msg = T_uxor(msg, keys[r])                     
        msg = mix_columns(msg, cons2)                 

    msg  = tuple([msg[i] for i in UN_SHIFT_ROWS])
    msg  = u_sub_wrd(msg)
    msg  = T_uxor(msg, keys[-1])                   

    msg = tyt_to_int(msg)
    return int_to_byt(msg)

def chunk(c):
    c   = byt_to_int(c)
    c   = up(int_to_tyt(c), sizeW ** 2, int_to_tyt(0)[0])
    x   = tuple(tyt_to_int(i) for i in c)
    x   = tuple(int_to_byt(i) for i in x)
    return x

def unchunk(c):
    out = []
    for i in c:
        j   = byt_to_int(i)
        j   = up(int_to_tyt(j), sizeW ** 2, int_to_tyt(0)[0])
        assert len(j) == 1
        out.append(j[0])
    out = down(out)
    out = tyt_to_int(out)
    return int_to_byt(out)

def pad(a):
    return a + b"\x00" * (64 - len(a))

def byte_xor(a, b):
    return bytes([i ^ j for i, j in zip(a, b)])

def gen():
    from hashlib import sha512
    flag, key = eval(open("secret.txt", "r").read())
    
    hsh = sha512(key).digest()
    with open("output.txt", "w+") as f:
        f.write(f"enc_flag = {byte_xor(hsh, pad(flag))}" + "\n")
        f.write(f"all_enc = {tuple(a3s(int_to_byt(i), key) for i in range(3 ** 9))}")

if __name__ == "__main__":
    gen()
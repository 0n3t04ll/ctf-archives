ROUNDS = 4
# 32-bit left shift rotation
rot = lambda x,n: ((x<<n)&0xffffffff)|(x>>(32-n))

def aaa(k):
    ks=[]
    for i in range(ROUNDS):
        k=rot(k,3)
        ks.append((k^(0x9E3779B9*(i+1)))&0xffffffff) # Golden Ratio: 0x9E3779B9
    return ks

def bbb(r,k):
    return (rot(r^k,5)*0x45D9F3B)&0xffffffff

def ccc(block,keys):
    l=int.from_bytes(block[:4],"big")
    r=int.from_bytes(block[4:],"big")
    for k in keys:
        l,r=r,l^bbb(r,k) # t = l ^ bbb(r,k)
    # final swap back
    return r.to_bytes(4,"big")+l.to_bytes(4,"big")

def encrypt(data,key):
    # encryption function
    ks=aaa(key)
    return b''.join(ccc(data[i:i+8],ks) for i in range(0,len(data),8))

if __name__ == "__main__": 
    key_hint=0xD4D4A1A0#     
    ciphertext=b"9\xbd/\x9588\x0bwo\xce+\xd4*\xd8\xda\x8d\x1f*\xac\x07f\xf1a\x9b\xd7$O\xbdU\\\xe2\xc5" 
    print("cipher:",ciphertext.hex())
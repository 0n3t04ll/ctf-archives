import random
import os
import hashlib

class RandomCipher:

    def __init__(self, master_key : bytes, sbox=None):
        self.k0 = master_key
        self.k1 = hashlib.md5(master_key).digest()
        
        if sbox == None:
            byte_perms = list(range(2**8))
            random.shuffle(byte_perms)
            self.sbox = byte_perms
        else:
            self.sbox = sbox
            
        print(f"Here's your SBox: {self.sbox}")
        
        self.sbox_inv = [None]*256
        for i in range(256):
            self.sbox_inv[self.sbox[i]] = i
        
    def encrypt(self, chunk : bytes):
        # Step 1: xor with k0
        chunk = [a ^ b for a, b in zip(chunk, self.k0)]
        
        # Step 2: input into the s_box
        chunk = [self.sbox[c] for c in chunk]
        
        # Step 3: xor with k1
        chunk = [a ^ b for a, b in zip(chunk, self.k1)]
        
        return bytes(chunk)
    
    def decrypt(self, chunk : bytes):
        # Step 1: xor with k1
        chunk = [a ^ b for a, b in zip(chunk, self.k1)]
        
        # Step 2: input into the inverse s_box
        chunk = [self.sbox_inv[c] for c in chunk]
        
        # Step 3: xor with k0
        chunk = [a ^ b for a, b in zip(chunk, self.k0)]
        
        return bytes(chunk)
        
    def encrypt_bytes(self, input : bytes):
        input_len = len(input)
        
        # ensure the input is a multiple of 16 bytes in length
        if input_len % 16 != 0:
            raise ValueError("input must be a multiple of 16 bytes")
        
        # process each chunk at once
        chunks = [input[i:i+16] for i in range(0, input_len, 16)]
        
        encrypted = list()
        for chunk in chunks:
            encrypted.append(self.encrypt(chunk))
            
        return b''.join(encrypted)
    
    def decrypt_bytes(self, input : bytes):
        input_len = len(input)
        
        # ensure the input is a multiple of 16 bytes in length
        if input_len % 16 != 0:
            raise ValueError("input must be a multiple of 16 bytes")
        
        # process each chunk at once
        chunks = [input[i:i+16] for i in range(0, input_len, 16)]
        
        decrypted = list()
        for chunk in chunks:
            decrypted.append(self.decrypt(chunk))
            
        return b''.join(decrypted)

if __name__ == '__main__':
    key = os.urandom(16)
    
    cipher = RandomCipher(key)

    flag = b"REDACTED"
    plaintext = b"I have a secret, please don't share: " + flag

    ciphertext = cipher.encrypt_bytes(plaintext)
    print(f"Ciphertext: {ciphertext.hex()}")

def round_function(block, key):
    # A simple non-linear function
    res = (block ^ key)
    return ((res << 3) | (res >> 13)) & 0xFFFF

def feistel_step(left, right, subkey):
    # Standard Feistel transformation
    new_left = right
    new_right = left ^ round_function(right, subkey)
    return new_left, new_right

def encrypt(plaintext_int, subkeys):
    # Split 32-bit into two 16-bit halves
    left = (plaintext_int >> 16) & 0xFFFF
    right = plaintext_int & 0xFFFF
    
    # 3 Rounds of Feistel
    for k in subkeys:
        left, right = feistel_step(left, right, k)
    
    # Final swap and combine
    return (right << 16) | left
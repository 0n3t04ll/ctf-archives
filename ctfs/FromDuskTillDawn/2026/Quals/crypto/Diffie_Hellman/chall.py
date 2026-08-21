import random
from hashlib import sha256
from Crypto.Cipher import AES
import os

FLAG = os.environ.get("FLAG").encode()

G = 2
P = 12142749931376146140306157979861612767925954500929247303219819042473653803530336299739506430037376217658586479693532417328915918057580329327083933174451542851696222896740577840268145854408485050990778623567462748414216440306125686162233732778060644607477458183123456674044282478651657206076772004813717346889024858893555295677822948950631188857430682528140776155876741847923841750755966762673721690709480563770610300718830043780172550006529129271618746407756883135571994513240207878537012680871952095145621706513860611820805675408577731719590221425476154946753220923868329985949301972909823596690727791039115668683329048674555979984249552581656330534178132505080849200469763

class DHParty:
  def __init__(self, p : int = P, g: int = G):
    self.p = p
    self.g = g
    self.private_key = random.getrandbits(self.p.bit_length() - 1)
    self.public_key = pow(self.g, self.private_key, self.p)

  def get_shared_key(self, other_public_key: int) -> bytes:
    s = pow(other_public_key, self.private_key, self.p)
    h = sha256(s.to_bytes((s.bit_length() + 7) // 8, 'big')).digest()
    return h
  
  @staticmethod
  def simmetric_encrypt(data: bytes, key: bytes) -> bytes:
    cipher = AES.new(key, AES.MODE_GCM)
    ciphertext = cipher.encrypt(data)
    return cipher.nonce + ciphertext
  
Alice = DHParty()
Bob = DHParty()

shared_key = Alice.get_shared_key(Bob.public_key)
enc_flag = Alice.simmetric_encrypt(FLAG, shared_key)

print(f"{enc_flag.hex()=!s}, {Alice.public_key=:x}, {Bob.public_key=:x}")

while True:
  try:
    public_key = int(input("Public key: "))
    Charlie = DHParty()
    shared_key = Charlie.get_shared_key(public_key)
    enc_msg = Charlie.simmetric_encrypt(b"Hello!", shared_key)
    print(f"{enc_msg.hex()=!s}, {Charlie.public_key=:x}")
  except:
    break
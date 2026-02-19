import os
from Crypto.Cipher import AES
from Crypto.PublicKey import RSA
from Crypto.Util.number import bytes_to_long, long_to_bytes

BIT_LENGTH = 1337

class PaddingError(Exception):
	pass

def pad(msg : bytes):
	padbyte = 16 - (len(msg) % 16)
	msg += padbyte.to_bytes(1) * padbyte
	return msg

def unpad(msg : bytes):
	pad_byte = msg[-1]
	if pad_byte == 0 or pad_byte > 16: raise PaddingError
	for i in range(1, pad_byte+1):
		if msg[-i] != pad_byte: raise PaddingError
	return msg[:-pad_byte]

def decrypt(cipher : bytes, privkey, opt = True):
	l = bytes_to_long(cipher[:4])
	iv = cipher[4:20]
	enc_msg = cipher[20:20+l]
	enc_key = bytes_to_long(cipher[20+l:])
	if opt:
		c_p = enc_key % privkey.p
		m_p = pow(c_p, privkey.dp, privkey.p)
		c_q = enc_key % privkey.q
		m_q = pow(c_q, privkey.dq, privkey.q)
		h = privkey.invq * (m_p - m_q) % privkey.q
		key = (m_q + h*privkey.q) % privkey.n
	else:
		key = pow(enc_key, privkey.d, privkey.n)
	if key > 1<<128:
		raise Exception('Error in key decryption')
	key = key.to_bytes(16)
	if len(enc_msg) % 16 > 0: raise PaddingError
	decrypter = AES.new(key, AES.MODE_CBC, iv = iv)
	msg_raw = decrypter.decrypt(enc_msg)
	return unpad(msg_raw)

def encrypt(message : str, pubkey):
	key = bytes(8) + os.urandom(8)
	encrypter = AES.new(key, AES.MODE_CBC)
	enc_message = encrypter.encrypt(pad(message.encode()))
	enc_key = pow(bytes_to_long(key), pubkey.e, pubkey.n)
	return len(enc_message).to_bytes(4) + encrypter.iv + enc_message + long_to_bytes(enc_key)

if __name__ == '__main__':
	flag = open('flag.txt','r').read().strip()
	RSA_key = RSA.generate(BIT_LENGTH)
	print(RSA_key.n)
	cipher = encrypt(flag, RSA_key)
	print(cipher.hex())

	while True:
		try:
			cipher_hex = input('input cipher (hex): ')
			if cipher_hex == 'exit': break
			cipher = bytes.fromhex(cipher_hex)
			message = decrypt(cipher, RSA_key)
			if message[:3] == b'ENO':
				print('That\'s the right start')
		except PaddingError:
			print('invalid padding')
		except Exception as err:
			print('something else went wrong')

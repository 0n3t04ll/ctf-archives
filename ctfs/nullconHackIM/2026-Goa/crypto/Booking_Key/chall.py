import random
import string

def encrypt(message, book, start):
	current = start
	cipher = []
	for char in message:
		count = 0
		while book[current] != char: 
			current = (current + 1) % len(book)
			count += 1
		cipher.append(count)
	return cipher

if __name__ == '__main__':
	flag = open('flag.txt','r').read().strip()

	BOOK = open('book.txt','r').read()
	charset = list(set(c for c in string.ascii_letters if c in BOOK))

	print('Three times is the charm.')
	for _ in range(3):
		key = random.randint(0,len(BOOK)-1)
		password = ''.join(random.choice(charset) for _ in range(32))

		cipher = encrypt(password, BOOK, key)
		print(cipher)

		user_password = input('password: ')
		if user_password != password:
			print('wrong password')
			exit(1)
		print('correct')
	print(flag)

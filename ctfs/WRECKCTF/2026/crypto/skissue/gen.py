from Crypto.Util.number import getPrime, bytes_to_long

bits = 1024
p = getPrime(bits)
q = getPrime(bits)
n = p * q
e = 65537

flag = open("flag.txt", "rb").read().strip()
m = bytes_to_long(flag)
c = pow(m, e, n)

print("p =", p)
print("q =", q)
print("n =", n)
print("e =", e)
print("c =", c)

with open("output.txt", "w") as f:
    f.write(f"n = {n}\n")
    f.write(f"e = {e}\n")
    f.write(f"c = {c}\n")

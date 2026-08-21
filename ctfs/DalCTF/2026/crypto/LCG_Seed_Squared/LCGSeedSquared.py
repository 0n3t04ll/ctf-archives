flag = "DalCTF{test}"

seed = "" # Turn the bytes into an int for the seed

x = 0

for i in range(0, len(seed)):
    x += ord(seed[i])

def rng(y):
    x = pow(int((175*y + 17)/14 + 45), 15, 4294967295)
    return x
    
for i in range(0, len(flag)):
    x = rng(x)
    t = ord(flag[i])*x
    print(t)

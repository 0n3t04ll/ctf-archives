print(f'Sage version = {version()}')

set_random_seed(input("seed: "))

F = GF(0xdead1337cec2a21ad8d01f0ddabce77f57568d649495236d18df76b5037444b1)
A = random_matrix(F, 52)[:,:-3]

# github.com/AustICCQuals/Challenges2025/blob/main/crypto/missingno/publish/Ab.sobj
if A == load("Ab")[0]:
    print("kalmar{...}")
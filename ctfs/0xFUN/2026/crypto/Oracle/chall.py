from secret_gen import gen

class Matrix:
    def __init__(self, data, mod):
        self.mat = data
        self.rows = len(data)
        self.cols = len(data[0])
        self.n = mod

    def __mul__(self, other):
        if self.cols != other.rows:
            raise ValueError("Dimension mismatch")
        
        res_data = [[0] * other.cols for _ in range(self.rows)]
        
        for i in range(self.rows):
            for k in range(self.cols):
                if self.mat[i][k] == 0: continue
                for j in range(other.cols):
                    res_data[i][j] = (res_data[i][j] + self.mat[i][k] * other.mat[k][j]) % self.n
            
        return Matrix(res_data, self.n)

    def __pow__(self, exp):
        if self.rows != self.cols:
            raise ValueError("Only square matrices can be exponentiated")
        
        res_data = [[(1 if i == j else 0) for j in range(self.cols)] for i in range(self.rows)]
        res = Matrix(res_data, self.n)
        base = self
        
        while exp > 0:
            if exp % 2 == 1:
                res = res * base
            base = base * base
            exp //= 2
        return res
    
def oracle(x):
    a, b = x // n, x % n
    
    matrix_data = []
    
    for r in range(SIZE):
        row = []
        for c in range(SIZE):
            if r == c:
                row.append(b + 1 + r)
            else:
                row.append(a)
        matrix_data.append(row)
        
    m = Matrix(matrix_data, n)
    m_pow = m ** d
    diag_sum = sum(m_pow.mat[i][i] for i in range(SIZE)) % n
    
    return diag_sum >> 20   # Hopefully, I'm truncating enough bits:3

n_bits = 1024
SIZE = 4   # This should be enough, right?

n, e, c, d, p, q, r = gen(n_bits)
assert n == p * q * r

print(f'e = {e}')
print(f'c = {c}')

while True:
    try:
        x = int(input('Enter message to decrypt: '))
        assert 0 < x and x != c - 1 
        print(oracle(x))
    except:
        print('Error!')

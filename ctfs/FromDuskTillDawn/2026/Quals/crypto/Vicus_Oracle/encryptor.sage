import os
import random
import itertools
import json
import sys
from hashlib import sha256
import numpy as np 
from sage.stats.distributions.discrete_gaussian_polynomial import DiscreteGaussianDistributionPolynomialSampler

q = 2**25
N = 16
n = 48
p = 2**8
rr = 2**17
h = 280
sigma = 2**8
B_sigma = round(13.4 * sigma)
Delta = Integer((q + p // 2) // p)

RqBase.<t> = PolynomialRing(Zmod(q))
Rq.<X> = RqBase.quotient(t^N + 1)
RZZ.<xZ> = PolynomialRing(ZZ)
gauss_poly_sampler = DiscreteGaussianDistributionPolynomialSampler(RZZ, N, sigma)

def setup(q, N, p, n, Delta):
    """Generate system parameters and matrix A."""
    A = sample_uniform_A_nxn(n, q, N)
    params = {'q': q, 'N': N, 'p': p, 'Delta': Delta, 'Rq': Rq, 'A': A, 'n': n}
    return params

def gaussian_poly_in_Rq(q, N):
    fZ = gauss_poly_sampler()
    coeffs = [Zmod(q)(fZ[i]) for i in range(N)]
    return Rq(RqBase(coeffs))

def gaussian_poly_in_Rq_pos(q, N):
    fZ = gauss_poly_sampler()
    coeffs = [Zmod(q)(abs(fZ[i])) for i in range(N)]
    return Rq(RqBase(coeffs))

def uniform_poly_in_Rq(q, N):
    coeffs = [Zmod(q).random_element() for _ in range(N)]
    return Rq(RqBase(coeffs))

def sample_uniform_A_nxn(n, q, N):
    set_random_seed(2025)
    a= Matrix(Rq, [[uniform_poly_in_Rq(q, N) for _ in range(n)] for __ in range(n)])
    set_random_seed(None)
    return a

def poly01_from_indices(idx_list, q, N):
    coeffs = [0]*N
    for i in idx_list: coeffs[i] = 1
    return Rq(RqBase(coeffs))

def sample_binary_vector_totalHW(vec_len, total_weight, q, N):
    base = total_weight // vec_len
    rem  = total_weight % vec_len
    vec = []
    for i in range(vec_len):
        w_i = base + (1 if i < rem else 0)
        idx = random.sample(range(N), w_i) if w_i > 0 else []
        vec.append(poly01_from_indices(idx, q, N))
    return vector(Rq, vec)

def uniform_poly_in_range(r, q, N):
    coeffs = [Zmod(q)(ZZ.random_element(-r//2, r//2)) for _ in range(N)]
    return Rq(RqBase(coeffs))

def inner_product(u, v):
    return sum(u[i] * v[i] for i in range(len(u)))

def embed_message(m, Delta, q, N):
    pr = m.lift()
    coeffs = [Zmod(q)(int(pr[i]) * Delta) for i in range(N)]
    return Rq(RqBase(coeffs))

def random_p_ary_poly(p, q, N):
    coeffs = [ZZ.random_element(0, p) for _ in range(N)]
    return Rq(RqBase(coeffs))

def coeffs_low_to_high(poly, N):
    return [int(poly[i]) for i in range(N)]

def keygen(params):
    A = params['A']; n = params['n']; q = params['q']; N = params['N']
    sk = sample_binary_vector_totalHW(vec_len=n, total_weight=h, q=q, N=N)
    e  = vector(Rq, [gaussian_poly_in_Rq(q, N) for _ in range(n)])
    pk = A.transpose() * sk + e
    return pk, sk

def validate_pk(v, n_expected, t=8):
    if len(v) != n_expected: return False
    g = []
    for p in v:
        c = [int(x) for x in p.lift().list()]
        z = [x for x in c if x != 0]
        if len(z) < t: return False
        if len(set(z)) < 3: return False
        g.extend(z)
    if len(set(g)) < 100: return False
    return True


def enc(params, pk_list, T=1):
    A = params['A']; n = params['n']; q = params['q']; N = params['N']
    p_loc = params['p']; Delta_loc = params['Delta']
    
    r = sample_binary_vector_totalHW(vec_len=n, total_weight=h, q=q, N=N)
    e_u = vector(Rq, [gaussian_poly_in_Rq_pos(q, N) for _ in range(n)])
    ct = A * r + e_u
    
    digest_list = []
    ci_list = []
    m_list = []
    
    for i in range(T):
        e_i = gaussian_poly_in_Rq_pos(q, N)
        m = random_p_ary_poly(p_loc, q, N)
        m_list.append(m)
        byte_len = 2
        m_bytes = b''.join(int(m.lift()[j]).to_bytes(byte_len, byteorder='big') for j in range(N))
        digest_list.append(sha256(m_bytes).hexdigest())
        
        y_i = uniform_poly_in_range(rr, q, N)
        
     
        ci = inner_product(pk_list[i], r) + e_i + embed_message(m, Delta_loc, q, N) + y_i
        ci_list.append(ci)

    return (ct, ci_list), r, m_list, digest_list

# --------------------- MAIN ---------------------

if __name__ == "__main__":

    params = setup(q, N, p, n, Delta)
    print("--- VICUS ORACLE SERVER ---")
    sys.stdout.flush()

    pk_list = []
    
    for i in range(n):
        try:
            line = sys.stdin.readline()
            if not line: break
            data = json.loads(line)
            
            pk_vec_elems = []
            for poly_coeffs in data:
                pk_vec_elems.append(Rq(RqBase(poly_coeffs)))
            
            pk_candidate = vector(Rq, pk_vec_elems)
            if not validate_pk(pk_candidate, n_expected=n):
                print("Error: Malformed public key detected.")
                sys.stdout.flush()
                sys.exit(0)
            
            pk_list.append(pk_candidate)
            
        except (ValueError, json.JSONDecodeError):
            break

 
    pk_h, sk_h = keygen(params)
    pk_list.append(pk_h)

 
    (ct, ci_list), r_secret, m_true_list, digest_list = enc(params, pk_list, T=n+1)


    output = {
        "c": [[int(x) for x in poly.lift()] for poly in ct],
        "v": [[int(x) for x in poly.lift()] for poly in ci_list],
        "hints": digest_list, 
        "pk_honest": [[int(x) for x in poly.lift()] for poly in pk_h],
    }
    print(json.dumps(output))
    sys.stdout.flush()

    user_sol = sys.stdin.readline().strip()
    target_sol = ""
    for poly in r_secret:
        target_sol += "".join(map(str, coeffs_low_to_high(poly, N)))
        
    if user_sol == target_sol:
        print("Attack success!")
        sys.stdout.flush()
        print(f"honest recipient's message: {m_true_list[n]}")
        with open("flag.txt", "r") as f:
            flag = f.read().strip()
            print(f"Congratulations! Here is your flag: {flag}")
    else:
        print("FAILURE: Secret r is incorrect.")
    sys.stdout.flush()

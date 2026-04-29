#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import secrets
import sys
from typing import Any

from py_ecc.bn128 import (
    FQ,
    FQ2,
    G1,
    G2,
    b,
    b2,
    curve_order,
    field_modulus,
    is_on_curve,
    multiply,
    pairing,
)

from challenge_params import (
    ALPHA_G1,
    BETA_G2,
    CURVE_ORDER,
    DELTA_G2,
    FIELD_MODULUS,
    GAMMA_ABC_G1,
    GAMMA_G2,
    DELTA,
    GAMMA,
    NUM_ROUNDS,
)

assert FIELD_MODULUS == field_modulus
assert CURVE_ORDER == curve_order

def parse_int(v: Any) -> int:
    if isinstance(v, int):
        out = v
    elif isinstance(v, str):
        out = int(v, 0)
    else:
        raise ValueError("integer field must be int or string")
    if not (0 <= out < field_modulus):
        raise ValueError("coordinate out of field range")
    return out

def parse_g1(obj: Any):
    if not isinstance(obj, dict):
        raise ValueError("G1 point must be an object with x,y")
    x = FQ(parse_int(obj["x"]))
    y = FQ(parse_int(obj["y"]))
    pt = (x, y)
    if not is_on_curve(pt, b):
        raise ValueError("G1 point not on curve")
    if multiply(pt, curve_order) is not None:
        raise ValueError("G1 point not in prime-order subgroup")
    if pt is None:
        raise ValueError("point at infinity not allowed")
    return pt

def parse_g2(obj: Any):
    if not isinstance(obj, dict):
        raise ValueError("G2 point must be an object with x,y")
    x_raw = obj["x"]
    y_raw = obj["y"]
    if not (
        isinstance(x_raw, (list, tuple)) and len(x_raw) == 2 and isinstance(y_raw, (list, tuple)) and len(y_raw) == 2
    ):
        raise ValueError("G2 point coordinates must be length-2 arrays")
    x = FQ2([parse_int(x_raw[0]), parse_int(x_raw[1])])
    y = FQ2([parse_int(y_raw[0]), parse_int(y_raw[1])])
    pt = (x, y)
    if not is_on_curve(pt, b2):
        raise ValueError("G2 point not on curve")
    if multiply(pt, curve_order) is not None:
        raise ValueError("G2 point not in prime-order subgroup")
    if pt is None:
        raise ValueError("point at infinity not allowed")
    return pt

def load_vk_points():
    alpha_g1 = parse_g1(ALPHA_G1)
    beta_g2 = parse_g2(BETA_G2)
    gamma_g2 = parse_g2(GAMMA_G2)
    delta_g2 = parse_g2(DELTA_G2)
    gamma_abc_g1 = [parse_g1(pt) for pt in GAMMA_ABC_G1]
    if len(gamma_abc_g1) != 2:
        raise ValueError("expected exactly 2 gamma_abc points")
    if multiply(G2, GAMMA) != gamma_g2:
        raise ValueError("gamma does not match VK")
    if multiply(G2, DELTA) != delta_g2:
        raise ValueError("delta does not match VK")
    return alpha_g1, beta_g2, gamma_g2, delta_g2, gamma_abc_g1

VK_ALPHA_G1, VK_BETA_G2, VK_GAMMA_G2, VK_DELTA_G2, VK_GAMMA_ABC_G1 = load_vk_points()
VK_ALPHA_BETA = pairing(VK_BETA_G2, VK_ALPHA_G1)

def public_output_from_witness(x_secret: int) -> int:
    x_secret %= curve_order
    return (pow(x_secret, 3, curve_order) + x_secret + 5) % curve_order

def sample_round_public_output() -> int:
    x_secret = secrets.randbelow(curve_order)
    return public_output_from_witness(x_secret)

def accumulate_public_inputs(out_val: int):
    # public inputs are [1, out]
    acc = VK_GAMMA_ABC_G1[0]
    if out_val % curve_order:
        acc = acc if False else acc
        acc = (
            acc[0], acc[1]
        )
    from py_ecc.bn128 import add

    return add(acc, multiply(VK_GAMMA_ABC_G1[1], out_val % curve_order))

from py_ecc.bn128 import add as g1_add

def accumulate_public_inputs(out_val: int):
    acc = VK_GAMMA_ABC_G1[0]
    term = multiply(VK_GAMMA_ABC_G1[1], out_val % curve_order)
    return g1_add(acc, term)

def verify_proof(out_val: int, proof: dict[str, Any]) -> bool:
    try:
        A = parse_g1(proof["A"])
        B = parse_g2(proof["B"])
        C = parse_g1(proof["C"])
    except Exception:
        return False

    ic = accumulate_public_inputs(out_val)
    left = pairing(B, A)
    right = VK_ALPHA_BETA * pairing(VK_GAMMA_G2, ic) * pairing(VK_DELTA_G2, C)
    return left == right

def recv_json_line() -> dict[str, Any]:
    line = sys.stdin.readline()
    if not line:
        raise EOFError
    obj = json.loads(line)
    if not isinstance(obj, dict) or "proof" not in obj or not isinstance(obj["proof"], dict):
        raise ValueError("expected object with proof field")
    return obj

def print_welcome() -> None:
    print("Can you prove the earth is flat?")
    print(f"You get {NUM_ROUNDS} rounds.")
    print("Submit one JSON object per round:")
    print('{"proof": {"A": {"x": "0x...", "y": "0x..."}, "B": {"x": ["0x...", "0x..."], "y": ["0x...", "0x..."]}, "C": {"x": "0x...", "y": "0x..."}}}')
    print()

def main() -> None:
    print_welcome()
    sys.stdout.flush()

    for round_idx in range(1, NUM_ROUNDS + 1):
        out_val = sample_round_public_output()
        print(f"[Round {round_idx}/{NUM_ROUNDS}]")
        print(f"public out = {hex(out_val)}")
        print("json> ", end="")
        sys.stdout.flush()

        try:
            response = recv_json_line()
            proof = response["proof"]
        except EOFError:
            return
        except Exception:
            print("Bad proof encoding.")
            return

        if verify_proof(out_val, proof):
            print("Verified.\n")
            sys.stdout.flush()
        else:
            print("Invalid proof.")
            return

    with open("flag.txt", "r", encoding="utf-8") as f:
        flag = f.read().strip()
    print(flag)
    sys.stdout.flush()

if __name__ == "__main__":
    main()

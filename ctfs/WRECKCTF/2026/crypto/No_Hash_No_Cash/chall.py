#!/usr/local/bin/python3

from pathlib import Path
from secrets import randbelow


P = 11719074539505701570179551256761475579474630788098935157186366782163497511838277919152843883183287276995046555100101944094983110257847476121069350632264323
G = 2
FLAG = Path(__file__).with_name("flag.txt").read_text().strip()


def sign(secret_key, message):
    k = randbelow(P - 2) + 1
    r = pow(G, k, P)
    e = (r + message) % (P - 1)
    s = (k - secret_key * e) % (P - 1)
    return r, s


def verify(public_key, message, r, s):
    if not (0 <= message < P - 1):
        return False
    if not (1 <= r < P):
        return False
    if not (0 <= s < P - 1):
        return False
    e = (r + message) % (P - 1)
    return pow(G, s, P) == (r * pow(public_key, -e, P)) % P


def read_int(prompt):
    print(prompt, end="", flush=True)
    return int(input().strip())


def main():
    secret_key = randbelow(P - 2) + 1
    public_key = pow(G, secret_key, P)
    signed_messages = set()

    print("Welcome to my hashless signature service.")
    print("The public parameters are:")
    print(f"p = {P}")
    print(f"g = {G}")
    print(f"h = {public_key}")
    print()
    print("You may request 3 signatures on messages modulo p - 1.")

    for index in range(3):
        message = read_int(f"message #{index + 1} = ") % (P - 1)
        signed_messages.add(message)
        r, s = sign(secret_key, message)
        print(f"r{index + 1} = {r}")
        print(f"s{index + 1} = {s}")

    print()
    print("Now give me a valid signature on a fresh message.")
    message = read_int("m = ") % (P - 1)
    r = read_int("r = ")
    s = read_int("s = ")

    if message in signed_messages:
        print("That message was already signed.")
        return

    if verify(public_key, message, r, s):
        print("Nice forgery.")
        print(FLAG)
    else:
        print("Nope.")


if __name__ == "__main__":
    try:
        main()
    except Exception:
        print("Input error.")

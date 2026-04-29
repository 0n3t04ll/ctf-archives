#!/usr/bin/env python3
T = bytes.fromhex("7066444d5033220a5b08d6a2fcc38ca7a788c2a17b6a15554d78341b")

flag = input("flag: ")
if len(flag) == len(T) and all(
    ord(flag[i]) ^ ((i * 13 + 7) & 0xFF) == T[i] for i in range(len(T))
):
    print("correct!")
else:
    print("nope")

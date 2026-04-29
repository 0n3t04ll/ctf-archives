"""
Bob runs a little 'secure' broadcast.  Each week he posts a public safety
bulletin and, separately, drops a private note to his friends -- both
encrypted with AES-CTR under the same key.

This week he also got lazy and picked the same nonce for both.
"""

from Crypto.Cipher import AES
import os

key = os.urandom(16)
nonce = os.urandom(8)

bulletin = (
    b"BULLETIN: This week's safety reminders from the helpdesk. "
    b"Lock your screen when you walk away. Do not reuse passwords. "
    b"And for the love of all that is good, never reuse a nonce with "
    b"a stream cipher -- that's basically a two-time pad, and a "
    b"two-time pad is no pad at all."
)
flag = open("flag.txt", "rb").read().strip()

ct_bulletin = AES.new(key, AES.MODE_CTR, nonce=nonce).encrypt(bulletin)
ct_flag = AES.new(key, AES.MODE_CTR, nonce=nonce).encrypt(flag)

with open("output.txt", "w") as f:
    f.write("bulletin (plaintext, posted publicly):\n")
    f.write(bulletin.decode() + "\n\n")
    f.write(f"ct_bulletin = {ct_bulletin.hex()}\n")
    f.write(f"ct_flag = {ct_flag.hex()}\n")

from Crypto.Util.number import bytes_to_long
flag = "CPCTF{REDACTED}"
flag_bytes = flag.encode()
print(f"c = {bytes_to_long(flag_bytes)}")

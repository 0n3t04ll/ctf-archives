#!/usr/bin/python3

from hashlib import sha256
import os

# check out my AWESOME DECENTRALIZED BANK !!
# implementing a merkle tree with an Uber Fast xor system !!
# who has the time to compute all those hashes ! not me !

nodes = []
root = 0
FLAG = open('flag.txt', 'r').read()

def xor(a: bytes, b: bytes):
    return bytes([a[i] ^ b[i] for i in range(len(a))])

def encode_node(account: str, balance: int):
    return account.encode().ljust(16, b'\x00') + balance.to_bytes(16, byteorder='little')

def decode_node(node: bytes):
    if len(node) != 32: raise Exception("[WrenchesBank]: Malformed node")
    return node[:16].decode().strip('\x00'), int.from_bytes(node[16:32], byteorder='little')

def parse_deposits(nodes: list):
    accounts = {}
    for node in nodes:
        account, balance = decode_node(node)
        if account not in accounts:
            accounts[account] = 0
        accounts[account] += balance
    return accounts

def accept_deposit(node: bytes):
    account, balance = decode_node(node)
    if account in ["alice", "bob", "charlie", "david"]: raise Exception("[WrenchesBank]: That's not you...")
    if balance > 1000: raise Exception("[WrenchesBank]: You do NOT have motion like this, bro. Who are you trying to fool?")
    if node in nodes: raise Exception("[WrenchesBank]: Duplicate node!")
    else:
        nodes.append(node)

def generate_root(nodes: list):
    hashes = [sha256(sha256(node).digest()).digest() for node in nodes]
    next_layer = []
    while len(hashes) != 1:
        if len(hashes) % 2 == 1: next_layer.append(hashes.pop());
        for idx in range(0, len(hashes), 2):
            next_layer.append(xor(hashes[idx], hashes[idx+1]))
        hashes = next_layer
        next_layer = []
    
    return hashes[0]

def verify_node_duplicates(nodes: list):
    return len(set(nodes)) == len(nodes)

### initial transactions

import random

transactions = {
    "alice":   random.randint(10 ** 10, 10 ** 11),
    "bob":     random.randint(10 ** 10, 10 ** 11),
    "charlie": random.randint(10 ** 10, 10 ** 11),
    "david":   random.randint(10 ** 10, 10 ** 11),
}

for account in transactions:
    balance = transactions[account]
    nodes.append(
        encode_node(account, balance)
    )

accounts = parse_deposits(nodes)

for i in range(0, 0x1000):
    print('[WrenchesBank]')
    print('1. Deposit')
    print('2. Sync bank state')
    print('3. Purchase flag with shareholder value')
    print('4. View bank nodes')

    choice = int(input('Select option > '))
    if choice == 1:
        name = input('Input account name > ')
        bal = input('Input account balance > ')
        node = encode_node(name, int(bal))
        accept_deposit(node)
    if choice == 2:
        inp = input("Input hex-encoded nodes, comma separated, no spaces (i.e. 01ab...23,02bc...de,) > ")
        inp_nodes = [bytes.fromhex(a) for a in inp.split(',')]
        if not verify_node_duplicates(inp_nodes):
            raise Exception("[WrenchesBank] Duplicate nodes detected!")
        if generate_root(inp_nodes) == generate_root(nodes):
            print("Nodes successfully synced!")
            nodes = inp_nodes
            accounts = parse_deposits(nodes)
        else:
            raise Exception("[WrenchesBank] Nodes failed to sync!")
    if choice == 3:
        print(accounts)
        inp = input("Input your name > ")
        if inp not in accounts:
            print("[WrenchesBank] There's no account with that name...")
        if accounts[inp] > 0xcafebeef12345678:
            print("[WrenchesBank] Nice! Here's the flag:")
            print(FLAG)
        else:
            print("[WrenchesBank] Come back when you have bands, bro...")
    if choice == 4:
        print("[WrenchesBank] Here is every single node in the system currently...")
        print(",".join([node.hex() for node in nodes]))

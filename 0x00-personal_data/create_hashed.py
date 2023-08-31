#!/usr/bin/env python3

import bcrypt
import time

passwd = b's$cret12'
start = time.time()
salt = bcrypt.gensalt()
hashed = bcrypt.hashpw(passwd, salt)
end = time.time()
print(end - start)

print(salt)
print(hashed)

if bcrypt.checkpw(passwd, hashed):
    print("Match")
else:
    print("Nah it doesnt")

print("Timed hashing")
"""Timed Hashing"""
passwd = b's$cret12'

start = time.time()
salt = bcrypt.gensalt(rounds=16)
hashed = bcrypt.hashpw(passwd, salt)
end = time.time()

print(end - start)

print(hashed)

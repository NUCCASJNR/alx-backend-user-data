#!/usr/bin/env python3
"""
Main file
"""
from auth import Auth, DB, User

email = 'bob@bob.com'
password = 'MyPwdOfBob'
auth = Auth()

a = auth.register_user(email, password)

print(auth.create_session(email))
print(auth.create_session("unknown@email.com"))

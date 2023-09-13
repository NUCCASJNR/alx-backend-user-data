#!/usr/bin/env python3

from auth import Auth  # Replace with the actual import path

# Create an instance of the Auth class
auth = Auth()

# Test the register_user method
try:
    auth.register_user("test@example.com", "testpassword")
    print("User registered successfully")
except ValueError as e:
    print(f"Error: {e}")

# Test the valid_login method
if auth.valid_login("test@example.com", "testpassword"):
    print("Login successful")
else:
    print("Login failed")

# Test the create_session method
session_id = auth.create_session("test@example.com")
if session_id:
    print(f"Session created with session ID: {session_id}")
else:
    print("Failed to create a session")

# Test the get_user_from_session_id method
user = auth.get_user_from_session_id(session_id)
if user:
    print(f"User found with email: {user.email}")
else:
    print("User not found")

# Test the destroy_session method
auth.destroy_session(user.id)
print("Session destroyed")

# Test the get_reset_password_token method
try:
    reset_token = auth.get_reset_password_token("test@example.com")
    print(f"Reset token generated: {reset_token}")
except ValueError as e:
    print(f"Error: {e}")
auth.update_password(user.reset_token, user.hashed_password)
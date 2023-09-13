#!/usr/bin/env python3

"""
End-to-end integration test
"""

import requests

URL = "http://localhost:5000"


def register_user(email: str, password: str) -> None:
    """
    test register user
    :param email: email address
    :param password: password
    :return:
        user obj
    """
    data = {"email": email, "password": password}
    response = requests.post(f"{URL}/users", data=data)
    if response.status_code == 400:
        assert response.json()['message'] == "email already registered"
    else:
        assert response.status_code == 200
        assert response.json().get("email") == email
        assert response.json().get("message") == "user created"
        print("User successfully registered")


def log_in_wrong_password(email: str, password: str) -> None:
    """
    logs in using a wrong password
    :param email: email
    :param password: password
    :return:
        message
    """
    data = {"email": email, "password": password}
    response = requests.post(f"{URL}/sessions", data=data)
    assert response.status_code == 401
    print("Incorrect login attempt handled")


def log_in(email: str, password: str) -> str:
    """
    Logs in a user
    :param email: email address
    :param password: password
    :return:
        user obj
    """
    data = {"email": email, "password": password}
    response = requests.post(f"{URL}/sessions", data=data)
    if response.status_code == 200:
        session_id = response.cookies.get("session_id")
        assert response.json().get("email") == email
        assert response.json().get("message") == "logged in"
        print("User Successfully logged in")
        return session_id


def profile_unlogged() -> None:
    """
    Un logged profile
    :return:
        None
    """
    response = requests.get(f"{URL}/profile")
    assert response.status_code == 403
    print("Unlogged user")


def profile_logged(session_id: str) -> None:
    """
    View profile while loggedin
    :param session_id: session_id
    :return:
        user obj
    """
    data = {"session_id": session_id}
    response = requests.get(f"{URL}/profile", cookies=data)
    assert response.status_code == 200
    assert response.json().get("email")


def log_out(session_id: str) -> None:
    """
    log out
    """
    cookie = {"session_id": session_id}
    response = requests.delete(f"{URL}/sessions", cookies=cookie)
    assert response.history == []
    # assert response.status_code == 200


def reset_password_token(email: str) -> str:
    """reset pwd"""
    data = {"email": email}
    response = requests.post(f"{URL}/reset_password", data=data)
    if response.status_code == 200:
        assert response.json().get("email") == email
        print("Reset token has been successfully sent to user")


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """Update pwd"""
    data = {"email": email, "reset_token": reset_token,
            "new_password": new_password}
    response = requests.put(f"{URL}/reset_password", data=data)
    if response.status_code == 200:
        assert response.json().get("email") == email
        assert response.json().get("reset_token") == reset_token
        assert response.json().get("new_password") == new_password


if __name__ == "__main__":
    EMAIL = "guillaume@holberton.io"
    PASSWD = "b4l0u"
    NEW_PASSWD = "t4rt1fl3tt3"

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)

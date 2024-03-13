"""
This file contains the logout handler.
"""
from flask import session, redirect


def handler():
    """
    Logout handler. This is where we can clear the session and redirect to the login page.
    :return:
    """
    session.pop('user', None)
    return redirect('/')

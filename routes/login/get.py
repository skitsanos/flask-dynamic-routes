"""
This file is responsible for rendering the login page.
"""
from flask import render_template


def handler():
    """
    Renders the login page.
    :return:
    """
    return render_template("login.html")

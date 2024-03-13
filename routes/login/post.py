"""
This file contains the handler for the login form submission.
"""
from flask import session, render_template, redirect, request

users = {
    "demo": "password123"
}


def handler():
    """
    Handles the login form submission.
    :return:
    """
    username = request.form["username"]
    password = request.form["password"]

    if username in users and users[username] == password:
        session["user"] = username
        return redirect("/dashboard")

    return render_template("login.html", error="Invalid username or password")

from flask import render_template


def handler():
    return render_template("login.html")

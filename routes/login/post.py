from flask import session, render_template, redirect, request

users = {
    "demo": "password123"
}


def handler():
    username = request.form["username"]
    password = request.form["password"]

    if username in users and users[username] == password:
        session["user"] = username
        return redirect("/dashboard")
    else:
        return render_template("login.html", error="Invalid username or password")

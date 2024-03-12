from flask import session, redirect


def handler():
    session.pop('user', None)
    return redirect('/')

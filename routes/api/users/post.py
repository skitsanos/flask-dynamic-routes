"""
This module is responsible for handling the POST requests to the API Users endpoint.
"""
from flask import request


def handler():
    """
    Handles the POST request to the API Users endpoint
    :return:
    """
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')

    # Perform some action with the data, such as saving it to a database
    # ...

    return {
        "demo": "yes",
        "name": name,
        "email": email
    }

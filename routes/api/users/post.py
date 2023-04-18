from flask import request


def handler():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')

    # Perform some action with the data, such as saving it to a database
    # ...

    return {
        "demo": "yes"
    }

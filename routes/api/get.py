from flask import jsonify, Response


def handler():
    response: Response = jsonify({
        "version": "1.0.0"
    })

    response.headers['Content-Type'] = 'application/json'
    return response

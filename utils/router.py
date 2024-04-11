"""
This module contains utility functions for the router and request handling. It includes
a function to validate a token, a function to convert a string to a Flask-style URL parameter,
and a function to load routes from a directory.
"""
import os
import re

from flask import request, make_response


def validate_token(secret_key: str):
    """
    Validate a token from the request header
    :param secret_key:
    :return:
    """
    if request.method == 'OPTIONS':
        return make_response({}, 200)

    token = request.headers.get('Authorization')
    if not token or not token.startswith('Bearer '):
        return make_response({'error': {"message": "Token is missing or invalid"}}, 401)

    # Extract the token from the header
    token = token.split(' ')[1]

    # Here you'd typically verify and decode the token using your preferred method,
    # such as JWT decoding and verification.
    # For demonstration purposes, let's assume simple verification with a secret key.
    if token != secret_key:
        return make_response({'message': 'Token is invalid'}, 401)

    return None


def convert_to_url_params(input_string: str):
    """
    Convert a string to a Flask-style URL parameter
    :param input_string:
    :return:
    """
    pattern = r'\$([a-zA-Z0-9_]+)'
    result = re.sub(pattern, r'<\1>', input_string)
    return result


def load_routes(app, path):
    """
    Load routes from a directory
    :param app:
    :param path:
    :return:
    """
    for root, dirs, _files in os.walk(path, followlinks=False):
        for found_dir in dirs:
            entry_point = str(os.path.join(root, found_dir))
            route_path = (os.path.relpath(path=entry_point, start=path)
                          .replace("\\", "/"))
            module_path = os.path.relpath(entry_point, path)

            methods = []
            for method in ("get", "post", "put", "delete", "options", "head", "patch"):
                if os.path.exists(os.path.join(root, found_dir, f"{method}.py")):
                    params_formatted_path = convert_to_url_params(str(route_path))
                    methods.append(method.upper())
                    module_name = f"routes.{module_path.replace(os.sep, '.')}.{method}"

                    app.logger.info(f'Route: {method.upper()} '
                                    f'/{params_formatted_path} ({module_name})')

                    module = __import__(module_name, fromlist=["*"])
                    app.add_url_rule(f"/{params_formatted_path}",
                                     view_func=module.handler,
                                     endpoint=module_name,
                                     methods=[method.upper()],
                                     strict_slashes=False
                                     )

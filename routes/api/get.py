"""
This module is responsible for handling the GET requests to the API Info endpoint.
"""


def handler():
    """
    Returns a dictionary containing the version of the API.
    :return:
    """
    return {
        "version": "1.0.0"
    }

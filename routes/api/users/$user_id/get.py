"""
This file contains the handler for the GET request to the API Users by ID endpoint
"""


def handler(user_id):
    """
    Handles the GET request to the API Users by ID endpoint
    :param user_id:
    :return:
    """
    return {
        "info": f"Get User by ID #{user_id}"
    }

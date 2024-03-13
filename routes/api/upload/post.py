"""
This module is responsible for handling the POST requests to the API Upload endpoint.
"""
import os

from flask import request, make_response, g


def handler():
    """
    Uploads a file to the server
    :return:
    """
    if 'file' not in request.files:
        return make_response(
            {
                "error":
                    {
                        "message": 'No file uploaded.'}
            },
            400
        )

    for file in request.files.getlist('file'):
        path_to_file = os.path.join(g.app.config['server']['uploads'], file.filename)
        if os.access(g.app.config['server']['uploads'], os.W_OK):
            file.save(path_to_file)

            return {
                "result": f"{len(request.files)} files saved"
            }

        return make_response(
            {
                "error":
                    {
                        "message": 'File storage is not writable'}
            },
            400
        )

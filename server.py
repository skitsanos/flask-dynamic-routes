import logging
import os
import re
import socket
import sys

from pathlib import Path

import yaml
from flask import Flask, g, render_template, request, jsonify
from flask_cors import CORS
from waitress import serve

from utils import system, router

app = Flask(__name__)


@app.before_request
def before_request():
    #
    # The request handler requires having access to the app context
    #
    g.app = app
    app.logger.info(f"{request.method} {request.path}")

    public_routes = app.config.get('server', {}).get('public', [])

    # use regex to match the public routes
    public_route_patterns = [re.compile(route) for route in public_routes]
    if not any(pattern.match(request.path) for pattern in public_route_patterns):
        return router.validate_token(os.getenv('AUTH_TOKEN'))


@app.errorhandler(404)
def page_not_found(error):
    app.logger.error(f'Page not found: {request.path}')
    return {'error': {'message': 'Page not found', 'code': 404, 'details': error.description}}, 404


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    hostname = socket.gethostname()
    logging.basicConfig(
        level=logging.INFO,  # Set the desired logging level
        format=f'%(asctime)s [%(levelname)s] {hostname} %(message)s',
        handlers=[
            logging.StreamHandler()
        ]
    )

    with app.app_context():
        app.config.update({"APP_HOME": os.path.dirname(Path(__file__).resolve())})
        #
        # Checking environment variables
        #
        app.logger.info('Checking environment...')

        if not system.check_env([
            'AUTH_TOKEN',
        ]):
            app.logger.error('Missing environment variables')
            sys.exit(1)

    app.logger.info('Checking config...')

    if os.path.exists('config.yaml'):
        with open('config.yaml', 'r') as config_file:
            config = yaml.safe_load(config_file)
            app.config.update(config)

            cors_config = app.config.get('cors', {})
            CORS(app, resources={r"/*": cors_config})

    app.logger.info(f'Loading routes ({os.getcwd()}/routes)...')

    router.load_routes(app, "routes")

    app.logger.info('Routes loaded.')

    # Specify the host and port
    host = os.getenv('BIND') or app.config.get('server', {}).get('bind') or '127.0.0.1'
    port = int(os.getenv('PORT') or app.config.get('server', {}).get('port') or '5000')

    # Start the Waitress server. To run the app behind reverse proxy:
    # https://github.com/Pylons/waitress/blob/main/docs/reverse-proxy.rst
    serve(app, host=host, port=port,
          url_scheme='https' if app.config.get('server', {}).get('ssl') else 'http')

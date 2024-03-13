"""
Flask server Template
@version: 1.0.0
@author: skitsanos
"""
import logging
import os
import re
import socket
import sys

from pathlib import Path

import yaml
from flask import Flask, g, render_template, request, redirect, session
from flask_cors import CORS
from waitress import serve

from utils import system, router

app = Flask(__name__)


@app.before_request
def before_request():
    """
    Before request handler. This is where we can check for the token or session and redirect to
    login page if not authenticated or authorized to access the page or API endpoint.
    :return:
    """
    #
    # The request handler requires having access to the app context
    #
    g.app = app
    app.logger.info("%s %s", request.method, request.path)

    public_routes = app.config.get('server', {}).get('public', [])
    public_route_patterns = [re.compile(route) for route in public_routes]

    is_public_route = any(pattern.match(request.path) for pattern in public_route_patterns)

    # if request.path starts with '/api' then check for the token
    if request.path.startswith('/api'):
        # use regex to match the public routes
        if not is_public_route:
            return router.validate_token(os.getenv('AUTH_TOKEN'))

    # if request.path not starts with '/api' then check for the session
    if not request.path.startswith('/api'):
        if 'user' not in session and not is_public_route:
            return redirect('/login')

    return None


@app.errorhandler(404)
def page_not_found(error):
    """
    Page not found error handler. This is where we can log the error and return a JSON response
    to the client.
    :param error:
    :return:
    """
    app.logger.error('Page not found: %s}', request.path)
    return {'error': {'message': 'Page not found', 'code': 404, 'details': error.description}}, 404


@app.context_processor
def inject_global_variables():
    """
    Inject global variables into the template context
    :return:
    """

    def format_price(amount, currency="€"):
        return f"{currency}{amount:.2f}"

    return {
        'page_title': 'API Server',
        'page_description': '(Powered by skitsanos/flask-dynamic-routes)',
        'format_price': format_price
    }


@app.route('/')
def index():
    """
    Index page handler
    :return:
    """
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
        with open('config.yaml', mode='r', encoding='utf8') as config_file:
            config = yaml.safe_load(config_file)
            app.config.update(config)

            cors_config = app.config.get('cors', {})
            CORS(app, resources={r"/*": cors_config})

    app.logger.info('Setting the secret key...')
    app.secret_key = os.getenv('SECRET_KEY') or app.config.get('server', {}).get(
        'secret_key') or 'default_secret_key'

    app.logger.info('Loading routes (%s/routes)...', os.getcwd())

    app.static_folder = 'public'

    router.load_routes(app, "routes")

    app.logger.info('Routes loaded.')

    # Specify the host and port
    host = os.getenv('BIND') or app.config.get('server', {}).get('bind') or '127.0.0.1'
    port = int(os.getenv('PORT') or app.config.get('server', {}).get('port') or '5000')

    # Start the Waitress server. To run the app behind reverse proxy:
    # https://github.com/Pylons/waitress/blob/main/docs/reverse-proxy.rst
    serve(app, host=host, port=port,
          url_scheme='https' if app.config.get('server', {}).get('ssl') else 'http')

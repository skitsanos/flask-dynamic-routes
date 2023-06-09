import os
import yaml

from flask import Flask, render_template, g
from flask_sock import Sock

from startup import startup

app = Flask(__name__)
websocket = Sock(app)

if os.path.exists('config.yaml'):
    with open('config.yaml', 'r') as config_file:
        config = yaml.safe_load(config_file)
        app.config.update(config)

app.config['UPLOADS_FOLDER'] = f"{os.getcwd()}/data/uploads"


def load_routes(app, path):
    for root, dirs, files in os.walk(path):
        for dir in dirs:
            route_path = os.path.relpath(os.path.join(root, dir), path)
            module_path = os.path.relpath(os.path.join(root, dir), path)

            # Check if dir starts with $
            if dir.startswith("$"):
                # Replace $ with < and > to make a path parameter
                route_path = os.path.relpath(os.path.join(root, f"<{dir.replace('$', '')}>"), path)

            methods = []
            for method in ("get", "post", "put", "delete"):
                if os.path.exists(os.path.join(root, dir, f"{method}.py")):
                    methods.append(method.upper())
                    module_name = f"routes.{module_path.replace(os.sep, '.')}.{method}"

                    module = __import__(module_name, fromlist=["*"])
                    app.add_url_rule(f"/{route_path}",
                                     view_func=module.handler,
                                     endpoint=module_name,
                                     methods=[method.upper()]
                                     )
                    break


load_routes(app, "routes")


@app.before_request
def before_request():
    g.app = app


@app.route('/')
def index():
    return render_template('index.html')


@websocket.route('/echo')
def echo(sock):
    while True:
        data = sock.receive()
        sock.send(f"pingback: {data}")


if __name__ == "__main__":
    startup(app)
    app.run(port=8000)

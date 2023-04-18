from flask import Flask
import os


def load_routes(app, path):
    for root, dirs, files in os.walk(path):
        for dir in dirs:
            route_path = os.path.relpath(os.path.join(root, dir), path)
            module_path = os.path.relpath(os.path.join(root, dir), path)

            # Check if dir starts with $
            if dir.startswith("$"):
                # Replace $ with < and > to make a path parameter
                route_path = os.path.relpath(os.path.join(root, f"<{dir.replace('$', '')}>"), path)
                print(route_path)
                print(module_path)

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


app = Flask(__name__)

load_routes(app, "routes")

if __name__ == "__main__":
    app.run()

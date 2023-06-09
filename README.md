# flask-dynamic-routes

> This script sets up a Flask application and dynamically loads route modules, allowing for a modular and extensible
> architecture


Flask is a popular Python web framework that is used for building web applications. It is a lightweight and flexible
framework that allows developers to create web applications quickly and easily. Flask is based on the Werkzeug WSGI
toolkit and the Jinja2 templating engine.

Flask provides a wide range of features and tools for web development, including routing, request handling, templating,
session management, and more. Flask applications can be built using a modular approach, with individual components such
as routes and views being separated into different files and modules.

One of the key advantages of Flask is its simplicity and ease of use. Flask applications can be built with just a few
lines of code, and the framework provides a clear and concise API that makes it easy to understand and use.

Flask is also highly customizable, allowing developers to extend and modify the framework to suit their specific needs.
It provides a wide range of extensions and plugins that can be used to add additional functionality to the framework.

Another advantage of Flask is its compatibility with a wide range of tools and technologies, including databases,
authentication systems, and more. Flask can be used with popular databases such as MySQL, PostgreSQL, and SQLite, and it
also supports various authentication and security mechanisms.

## requirements.txt

In Python, the requirements.txt file is a text file that lists all the required third-party packages and their versions
for a Python project to function properly. It is commonly used in conjunction with package managers such as pip to
automate the installation of dependencies for a project.

```shell
pip install -r requirements.txt
```

## Running the app

### With gunicorn

Gunicorn (short for "Green Unicorn") is a Python Web Server Gateway Interface (WSGI) HTTP server. It's designed to be a
fast and reliable server that can handle multiple requests simultaneously. Gunicorn is commonly used to serve web
applications built with Python frameworks such as Django or Flask.

Gunicorn can be run from the command line or as a service, and it can be configured using a configuration file or
command line arguments. Some of the configuration options include the number of worker processes, the address and port
to listen on, logging settings, and more.

One of the advantages of using Gunicorn is that it integrates well with other tools commonly used in Python web
development, such as Nginx and load balancers. It's also designed to be simple and easy to use, making it a popular
choice for deploying Python web applications

```shell
gunicorn main:app --reload
```
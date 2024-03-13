# flask-dynamic-routes

> This script sets up a Flask application and dynamically loads route modules, allowing for a modular and extensible architecture


Flask is a popular Python web framework that is used for building web applications. It is a lightweight and flexibleframework that allows developers to create web applications quickly and easily. Flask is based on the Werkzeug WSGI toolkit and the Jinja2 templating engine.

Flask provides a wide range of features and tools for web development, including routing, request handling, templating, session management, and more. Flask applications can be built using a modular approach, with individual components such as routes and views being separated into different files and modules.

One of the key advantages of Flask is its simplicity and ease of use. Flask applications can be built with just a few lines of code, and the framework provides a clear and concise API that makes it easy to understand and use.

Flask is also highly customizable, allowing developers to extend and modify the framework to suit their specific needs. It provides a wide range of extensions and plugins that can be used to add additional functionality to the framework.

Another advantage of Flask is its compatibility with a wide range of tools and technologies, including databases,
authentication systems, and more. Flask can be used with popular databases such as MySQL, PostgreSQL, and SQLite, and italso supports various authentication and security mechanisms.

## Prerequisites

Ensure you have Python and pip installed on your system. The application relies on a virtual environment for managing dependencies.

## requirements.txt

In Python, the requirements.txt file is a text file that lists all the required third-party packages and their versions
for a Python project to function properly. It is commonly used in conjunction with package managers such as pip to
automate the installation of dependencies for a project.

```shell
pip install -r requirements.txt
```

## Running the app

To run the Flask application, you can use the following command:

```shell
python server.py
```

## Using Taskfile for Project Management

Taskfile provides a series of tasks to streamline the development and deployment process of the Flask application. Below are the key tasks defined in the Taskfile and how to use them:

### Install Dependencies

Sets up a virtual environment (if not already present), upgrades pip, and installs all required Python packages listed in `requirements.txt`.

```shell
task install
```

### Lint Python Files

Lints Python files in the project using pylint to ensure code quality.

```shell
task lint
```

### Start the Application

Runs the Flask application using the virtual environment.

```shell
task start
```

### Docker Build

Cleans the project, builds a Docker image with the application, tagging it accordingly.

```shell
task docker-build
```

### Generate SystemD Unit File

Generates a SystemD service file for deploying the application as a service on a Linux server.

```shell
task generate-unit-file
```

### Deploy to Remote Server

Deploys the application to a remote server. It includes copying necessary files, installing Python packages, and setting up the application as a SystemD service.

```shell
task deploy-to-remote
```

For this task, detailed attention must be given to configuring environment variables crucial for successful remote deployment. This process involves setting up SSH connections and utilizing SCP for file transfers to the remote server, which are pivotal operations within the task. Here, we’ll elaborate on the required variables, particularly focusing on `DEPLOYMENT_ENDPOINT` and `DEPLOYMENT_USERNAME`, and how they facilitate the deployment process.

#### `DEPLOYMENT_ENDPOINT`

- **Description**: Specifies the IP address or hostname of the remote server where the Flask application will be deployed. This is the destination for SSH connections and SCP file transfers.
- **Usage**: Set this variable to the remote server's IP address or hostname. It is used in the `ssh` and `scp` commands to identify where to connect for deploying the application and managing remote operations.

#### `DEPLOYMENT_USERNAME`

- **Description**: The username used to log into the remote server. This user must have sufficient permissions to execute commands, manage files, and, optionally, perform operations like restarting system services.
- **Usage**: This variable is crucial for both `ssh` and `scp` commands, serving as the authentication identity when connecting to the remote server. Ensure that this user has the necessary permissions to perform actions defined in the deploy tasks.

Before running the "Deploy to Remote Server" task, ensure that you have correctly set the values for these variables in your Taskfile. For example:

```yaml
env:
  # Replace with your server's address or hostname
  DEPLOYMENT_ENDPOINT: "192.168.1.100"
  # Replace with your deployment username on the remote server
  DEPLOYMENT_USERNAME: "deployuser"

```

### Execution of "Deploy to Remote Server" Task

With these variables configured, the `deploy-to-remote` task will perform a series of actions:

1. **Preparation**: Generates a SystemD unit file for the application and cleans up any pre-existing bytecode files.
2. **Remote Setup**: Checks and sets up the required user and group on the remote server, if necessary.
3. **File Transfer**: Utilizes `scp` to securely copy the application files (including the Taskfile, requirements, configurations, and source code) to the specified `DEPLOYMENT_PATH` on the remote server.
4. **Remote Installation**: Executes `ssh` commands to install dependencies on the remote server, leveraging the `task install` command remotely.
5. **Service Installation**: Copies the generated SystemD unit file to the appropriate location on the remote server and enables the service for automatic start at boot.
6. **Service Management**: Starts the newly installed service, ensuring the Flask application is running as a background service on the server.

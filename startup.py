from os import path, makedirs


def startup(app):
    print("Running startup code...")
    if not path.exists(app.config['UPLOADS_FOLDER']):
        makedirs(app.config['UPLOADS_FOLDER'], exist_ok=True)

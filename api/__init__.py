from flask import Flask


def create_app():
    app = Flask(__name__)

    from . import generate_name  # noqa

    app.register_blueprint(generate_name.bp)

    return app

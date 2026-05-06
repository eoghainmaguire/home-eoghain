from flask import Flask, jsonify

from .db import close_db, init_db
from .routes import bp
from .security import add_security_headers


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        DATABASE=app.instance_path + "/portfolio.db",
        SECRET_KEY="dev-change-me",
    )

    app.teardown_appcontext(close_db)
    app.after_request(add_security_headers)
    app.register_blueprint(bp)
    register_error_handlers(app)

    with app.app_context():
        init_db()

    return app


def register_error_handlers(app):
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"error": "Not found"}), 404

    @app.errorhandler(500)
    def server_error(error):
        return jsonify({"error": "Something went wrong."}), 500

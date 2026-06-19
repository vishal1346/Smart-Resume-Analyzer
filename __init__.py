"""
app/
-----------------
Flask application factory. Keeping app creation in a factory function
(instead of a global app object) is a clean-coding best practice that
makes testing and future scaling easier.
"""

from flask import Flask


def create_app():
    """
    Builds and returns the configured Flask application.
    """
    app = Flask(__name__)

    # Register the API blueprint that holds Module 1 and Module 4 routes.
    from app.routes.api_routes import api_bp
    app.register_blueprint(api_bp)

    # Simple root route, useful for confirming the server is alive.
    @app.route("/")
    def index():
        return {
            "message": "Smart Resume Analyzer API is running.",
            "endpoints": [
                "/api/resume-score [POST]",
                "/api/resume-feedback [POST]",
                "/api/analyze-resume [POST]",
            ],
        }

    return app

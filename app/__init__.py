from flask import Flask


def create_app():
    app = Flask(__name__)

    from app.routes.api_routes import api_bp
    app.register_blueprint(api_bp)

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

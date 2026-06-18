"""
run.py
-------
Entry point to start the Flask development server.

Usage:
    python run.py
"""

from app import create_app

app = create_app()

if __name__ == "__main__":
    # debug=True enables auto-reload and detailed error pages during
    # development. Set to False in production.
    app.run(debug=True, host="0.0.0.0", port=5000)

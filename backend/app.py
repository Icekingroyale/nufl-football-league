# This file has been refactored into a modular Flask structure.
# The main app is now created in app/__init__.py using the app factory pattern.
# All routes are organized as blueprints in app/routes/.
# Database logic is in app/models.py, helpers in app/utils.py.
# Use run.py as the entry point to run the app.

from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run() 
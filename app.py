from flask import Flask
from src.models.models import db
from flask_migrate import Migrate


def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///dogs.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SQLALCHEMY_BINDS"] = {
        "runs": "sqlite:///runs.db",
        "owner": "sqlite:///owner.db",
        "titles": "sqlite:///titles.db",
    }

    db.init_app(app)  # Bind SQLAlchemy to the app
    Migrate(app, db)

    # Import and register Blueprints here
    from src.routes import runs, blueprint, dogs, search

    app.register_blueprint(blueprint)
    app.register_blueprint(dogs)
    app.register_blueprint(runs)
    app.register_blueprint(search)

    return app

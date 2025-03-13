from flask import Flask
from src.models.models import db, User
from flask_migrate import Migrate
from flask_login import LoginManager
import os
from src.routes import blueprint, dogs, runs, search, leaderboard, events
from src.routes.auth import auth  # Import auth blueprint directly


def create_app():
    app = Flask(__name__)
    
    # Create absolute paths for the database
    base_dir = os.path.abspath(os.path.dirname(__file__))
    instance_path = os.path.join(base_dir, 'instance')
    
    # Create instance directory if it doesn't exist
    os.makedirs(instance_path, exist_ok=True)
    
    # Set database URI using absolute path for SQLite
    db_path = os.path.join(instance_path, 'dogs.db')
    
    # Configure SQLAlchemy with SQLite (not PostgreSQL)
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SQLALCHEMY_BINDS"] = {
        "dogs": f"sqlite:///{db_path}"
    }

    # Set a secret key for session management
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-key-for-development-only")

    # Initialize extensions
    db.init_app(app)
    migrate = Migrate(app, db)
    
    # Initialize Flask-Login
    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Register blueprints
    app.register_blueprint(blueprint)
    app.register_blueprint(dogs)
    app.register_blueprint(runs)
    app.register_blueprint(search)
    app.register_blueprint(leaderboard)
    app.register_blueprint(auth)  # Register auth blueprint
    app.register_blueprint(events)  # Register events blueprint

    # Create tables within app context
    with app.app_context():
        db.create_all()

    return app

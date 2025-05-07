from app import create_app, db
from waitress import serve
import os


# Create the application instance
app = create_app()

# Ensure we're in the application context
with app.app_context():
    try:
        # Create all tables
        db.create_all()
        print("Database tables created successfully")
    except Exception as e:
        print(f"Error creating database tables: {e}")
        # Print additional debugging information
        print(f"Current working directory: {os.getcwd()}")
        print(f"SQLALCHEMY_DATABASE_URI: {app.config['SQLALCHEMY_DATABASE_URI']}")
        print(f"Instance path: {app.instance_path}")

if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=8080)

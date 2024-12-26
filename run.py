from app import create_app, db
from src.models.models import Dogs, Runs

app = create_app()

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)

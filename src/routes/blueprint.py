from flask import Blueprint, render_template
from src.models.models import Runs, Dogs, db
from sqlalchemy import select


# Create a Blueprint instance
blueprint = Blueprint("main", __name__)


# Landing page route
@blueprint.route("/")
def index():
    try:
        # More explicit query using with_entities to specify columns
        items = db.session.execute(
            select(Dogs)
            .order_by(Dogs.points.desc())
            .limit(10)
        ).scalars().all()  # Add .all() to materialize the query
        return render_template("index.html", items=items if items else [])
    except Exception as e:
        print(f"Database error: {e}")  # For debugging
        return render_template("index.html", items=[])

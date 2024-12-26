from flask import Blueprint, render_template
from src.models.models import Runs, Dogs, db
from sqlalchemy import select


# Create a Blueprint instance
blueprint = Blueprint("main", __name__)


# Landing page route
@blueprint.route("/")
def index():
    items = db.session.execute(select(Dogs).order_by(Dogs.points).limit(10)).scalars()
    #    Runs.query.all()
    return render_template("index.html", items=items if items is not None else [])

from datetime import datetime
from flask import Flask, render_template, request, redirect
from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Float,
    Boolean,
    Enum,
)
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import backref


app = Flask(__name__)

# Configure SQLite database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///dogs.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

app.config["SQLALCHEMY_BINDS"] = {"runs": "sqlite:///runs.db"}

db = SQLAlchemy()
db.init_app(app)


# Define the database model
class Dogs(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    show_name = Column(String(100), nullable=True)
    points = Column(Integer, nullable=True)
    owner = Column(String(50), nullable=False)


PLACEMENTS = {"1st", "2nd", "3rd", "4th", "N/A"}
CLASSES = {"JWW", "STD", "FAST", "PJWW", "PSTD", "T2B"}
JUMP_HEIGHTS = {"24", "20", "16", "12", "8", "4"}


class Runs(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    pet_id = Column(Integer, nullable=False)
    show_name = Column(String(100), ForeignKey("dogs.show_name"), nullable=False)
    run_time = Column(Float, nullable=False)
    course_time = Column(Float, nullable=False)
    qualification = Column(Boolean, nullable=False)
    points = Column(Integer, nullable=False)
    handler = Column(String(50))
    trial = Column(String(100), nullable=True)
    timestamp = Column(DateTime, nullable=False)
    height = Column(String(8), nullable=False)
    place = Column(String(20), nullable=False)
    judge = Column(String(50), nullable=False)
    run_class = Column(String(10), nullable=False)

    db.relationship("dogs", backref=backref("show_name"), lazy=True)


# Initialize the database
with app.app_context():
    db.create_all()


# Landing page route
@app.route("/")
def index():
    items = Dogs.query.all()
    Runs.query.all()
    return render_template("index.html", items=items if items is not None else [])


@app.route("/runs/<string:name>")
def runs(name):
    # Query the details for the clicked item
    run_records = Runs.query.filter_by(show_name=name).all()
    dog = Dogs.query.filter(Dogs.show_name == name).one()
    return render_template(
        "runs.html",
        items=run_records if run_records is not None else [],
        show_name=name,
        dog=dog,
    )


# Create new record route
@app.route("/create-dog", methods=["GET", "POST"])
def create_dog():
    if request.method == "POST":
        name = request.form["name"]
        show_name = request.form["show_name"]
        points = request.form["points"]
        owner = request.form["owner"]
        new_item = Dogs(name=name, show_name=show_name, points=points, owner=owner)
        db.session.add(new_item)
        db.session.commit()
        return redirect("/")
    return render_template("create-dog.html")


# Update existing record route
@app.route("/update-dog/<int:id>", methods=["GET", "POST"])
def update(id):
    item = Dogs.query.get(id)
    if request.method == "POST":
        item.name = request.form["name"]
        item.show_name = request.form["show_name"]
        item.points = request.form["points"]

        db.session.commit()
        return redirect("/")
    return render_template("update-dog.html", item=item)


def delete_item(Table, arg):
    item = Table.query.get(arg)
    assert item
    db.session.delete(item)
    db.session.commit()

    return bool(Table.query.get(arg))


def points_calc(run_time, course_time):
    points = int(float(course_time) - float(run_time))
    return points if points > 0 else 0


# Delete a record route
# TODO: add a flag for 'deleted' items
@app.route("/delete-dog/<int:id>")
def delete_dog(id):
    delete_item(Dogs, id)
    return redirect("/")


@app.route("/create-run/<string:show_name>", methods=["GET", "POST"])
def create_run(show_name: str):
    dog = Dogs.query.filter(Dogs.show_name == show_name).one()
    if request.method == "POST":
        run_time = request.form["run_time"]
        course_time = request.form["course_time"]
        new_item = Runs(
            pet_id=dog.id,
            name=request.form["name"],
            show_name=request.form["show_name"],
            run_time=run_time,
            course_time=course_time,
            qualification=False,
            handler=request.form["handler"],
            points=points_calc(run_time, course_time),
            trial=request.form["trial"],
            timestamp=datetime.fromisoformat(request.form["timestamp"]),
            height=request.form["height"],
            place=request.form["place"],
            judge=request.form["judge"],
            run_class=request.form["run_class"],
        )

        db.session.add(new_item)
        db.session.commit()
        return redirect(f"/runs/{show_name}")
    return render_template(
        "create-run.html",
        show_name=show_name,
        dog=dog,
        run_class=CLASSES,
        placements=PLACEMENTS,
        jump_heights=JUMP_HEIGHTS,
    )


# Update existing record route
@app.route("/update-run/<int:id>", methods=["GET", "POST"])
def update_run(id):
    item = Dogs.query.get(id)
    if request.method == "POST":
        item.name = request.form["name"]
        item.show_name = request.form["show_name"]
        item.points = request.form["points"]

        db.session.commit()
        return redirect("/")
    return render_template("update-run.html", item=item)


# Delete a record route
# TODO: add a flag for 'deleted' items
@app.route("/delete-run/<int:id>")
def delete_run(id):
    item = Runs.query.filter(Runs.id == id).one()
    delete_item(Runs, id)
    return redirect(f"/runs/{item.show_name}")


if __name__ == "__main__":
    app.run(debug=True)

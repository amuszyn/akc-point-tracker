from flask import Blueprint
from src.models.models import Runs, Dogs, db
from src.models.helpers import delete_item_by_id, query_items, get_item
from src.constants import PLACEMENTS, CLASSES, JUMP_HEIGHTS
from flask import render_template, request, redirect
from datetime import datetime

runs = Blueprint("runs", __name__)


@runs.route("/runs/<string:name>")
def get_runs(name):
    # Query the details for the clicked item
    run_records = query_items(Runs, Runs.show_name, name)
    dog = get_item(Dogs, Dogs.show_name, name)
    return render_template(
        "runs.html",
        items=run_records if run_records is not None else [],
        show_name=name,
        dog=dog,
    )


@runs.route("/create-run/<string:show_name>", methods=["GET", "POST"])
def create_run(show_name: str):
    dog = get_item(Dogs, Dogs.show_name, show_name)
    assert isinstance(dog, Dogs)
    if request.method == "POST":
        run_time = request.form["run_time"]
        course_time = request.form["course_time"]
        new_item = Runs(
            pet_id=dog.id,
            name=dog.name,
            show_name=dog.show_name,
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
@runs.route("/update-run/<int:id>", methods=["GET", "POST"])
def update_run(id):
    item = get_item(Dogs, Dogs.id, id)
    assert isinstance(item, Dogs)
    if request.method == "POST":
        item.name = request.form["name"]
        item.show_name = request.form["show_name"]
        item.points = int(request.form["points"])

        db.session.commit()
        return redirect("/")
    return render_template("update-run.html", item=item)


# Delete a record route
# TODO: add a flag for 'deleted' items
@runs.route("/delete-run/<int:id>")
def delete_run(id):
    item = get_item(Runs, Runs.id, id)
    delete_item_by_id(Runs, id)
    assert isinstance(item, Runs)
    return redirect(f"/runs/{item.show_name}")


def points_calc(run_time, course_time):
    points = int(float(course_time) - float(run_time))
    return points if points > 0 else 0

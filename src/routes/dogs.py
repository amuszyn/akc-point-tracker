from flask import Blueprint
from src.models.models import Dogs, db
from src.models.helpers import delete_item_by_id, get_item
from flask import render_template, request, redirect

dogs = Blueprint("dogs", __name__)


# Create new record route
@dogs.route("/create-dog", methods=["GET", "POST"])
def create_dog():
    if request.method == "POST":
        name = request.form["name"]
        show_name = request.form["show_name"]
        points = request.form["points"]
        owner = request.form["owner"]
        dog = Dogs(name=name, show_name=show_name, points=points, owner=owner)
        db.session.add(dog)
        db.session.commit()
        return redirect("/")
    return render_template("create-dog.html")


# Update existing record route
@dogs.route("/update-dog/<int:id>", methods=["GET", "POST"])
def update(id):
    item = get_item(Dogs, "id", id)
    assert isinstance(item, Dogs)
    if request.method == "POST":
        item.name = request.form["name"]
        item.show_name = request.form["show_name"]
        item.points = int(request.form["points"])

        db.session.commit()
        return redirect("/")
    return render_template("update-dog.html", item=item)


# Delete a record route
# TODO: add a flag for 'deleted' items
@dogs.route("/delete-dog/<int:id>")
def delete_dog(id):
    delete_item_by_id(Dogs, id)
    return redirect("/")

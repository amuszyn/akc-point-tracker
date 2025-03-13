from flask import Blueprint, redirect, request
from src.models.models import Owner, db

owner = Blueprint("owner", __name__)


@owner.get("/owner")
def get_owner():
    owners = Owner.query.all()
    return {"owners": [{"name": o.name} for o in owners]}


@owner.post("/owner/<string:name>/update")
def update_owner(name):
    owner = Owner.query.filter_by(name=name).first()
    if owner:
        owner.name = request.json.get("name", owner.name)
        db.session.commit()
    return {}


@owner.delete("/owner/<string:name>/delete")
def delete_owner(name):
    owner = Owner.query.filter_by(name=name).first()
    if owner:
        owner.deleted = True  # Soft delete
        db.session.commit()
    return redirect("/")

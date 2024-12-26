from flask import Blueprint, redirect

owner = Blueprint("owner", __name__)


@owner.get("/owner")
def get_owner():
    return {}


@owner.post("/owner/<string:name>/update")
def update_owner():
    return {}


@owner.delete("owner/<string:name>/delete")
def delete_owner():
    return redirect("/")

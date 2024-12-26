from flask import Blueprint, jsonify, request
from sqlalchemy import or_, select
from src.models.models import Dogs
from src.models.helpers import db, get_item

search = Blueprint("search", __name__)


@search.post("/search")
def do_search():
    query = request.form.get("query")
    #    owner_q = select(Owner).where(Owner.name.ilike(f"%{query}%"))
    #    owner_results = db.session.execute(owner_q).scalars().all()

    dog_query = select(Dogs).where(
        or_(Dogs.name.__eq__(query), Dogs.show_name.__eq__(query))
    )
    dog_results = db.session.execute(dog_query).scalars().all()

    dog_results = get_item(Dogs, Dogs.name, f"%{query}%")

    return jsonify(dog_results)

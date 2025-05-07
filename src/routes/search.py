from flask import Blueprint, jsonify, request
from sqlalchemy import or_
from src.models.models import Dogs, Owner

search = Blueprint("search", __name__)


@search.post("/search")
def do_search():
    query = request.form.get("query")
    
    # Search dogs
    dog_results = Dogs.query.filter(
        or_(
            Dogs.name.ilike(f"%{query}%"),
            Dogs.show_name.ilike(f"%{query}%")
        )
    ).all()

    # Search owners
    owner_results = Owner.query.filter(
        Owner.name.ilike(f"%{query}%")
    ).all()

    return jsonify({
        "dogs": [{"name": d.name, "show_name": d.show_name} for d in dog_results],
        "owners": [{"name": o.name} for o in owner_results]
    })

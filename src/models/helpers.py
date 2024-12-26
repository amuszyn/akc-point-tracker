from sqlalchemy import select
from .models import db


def delete_item_by_id(Table, arg):
    q = select(Table).filter(Table.id == arg)
    item = db.session.execute(q).scalar_one()
    assert item
    db.session.delete(item)
    db.session.commit()

    return bool(db.session.execute(q).scalar_one_or_none()) is None


def get_item(Table, property, arg):
    """
    Grabs a single item equal to the arg
    """
    q = select(Table).filter(property == arg)
    return db.session.execute(q).scalar()


def query_items(Table, property, arg):
    """
    Grabs all items equal to the arg
    """
    q = select(Table).filter(property == arg)
    return db.session.execute(q).scalars()

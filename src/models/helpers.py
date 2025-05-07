from .models import db


def delete_item_by_id(model, id):
    """Delete an item by ID"""
    item = model.query.get(id)
    if item:
        db.session.delete(item)
        db.session.commit()
        return True
    return False


def get_item(model, column, value):
    """Get a single item by a specific column value"""
    # If looking up by primary key/id
    if column == "id" or (isinstance(column, str) and column == model.__mapper__.primary_key[0].name):
        return model.query.get(value)
    
    # Otherwise, filter by the column
    if isinstance(column, str):
        column = getattr(model, column)
    
    return model.query.filter(column == value).first()


def query_items(model, column, value):
    """Query items by a specific column value"""
    # Get the actual column object if a string was passed
    if isinstance(column, str):
        column = getattr(model, column)
    
    return model.query.filter(column == value).all()

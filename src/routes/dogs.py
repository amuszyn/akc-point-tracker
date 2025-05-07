from flask import Blueprint
from src.models.models import Dogs, db
from flask import render_template, request, redirect, flash
from flask_login import current_user, login_required

dogs = Blueprint("dogs", __name__)


# Create new record route
@dogs.route("/create-dog", methods=["GET", "POST"])
@login_required
def create_dog():
    if request.method == "POST":
        try:
            name = request.form["name"]
            show_name = request.form["show_name"]
            points = request.form["points"]
            owner = request.form["owner"]
            
            dog = Dogs(
                name=name, 
                show_name=show_name, 
                points=points if points else 0, 
                owner=owner,
                created_by=current_user.id
            )
            
            db.session.add(dog)
            db.session.commit()
                
            return redirect("/")
        except Exception as e:
            print(f"Error creating dog: {e}")  # For debugging
            db.session.rollback()  # Rollback on error
            return render_template("create-dog.html", error=str(e))
            
    # For GET request, pass the current user's name as default owner
    default_owner = f"{current_user.first_name} {current_user.last_name}".strip() if current_user.first_name or current_user.last_name else current_user.username
    return render_template("create-dog.html", default_owner=default_owner)


# Update existing record route
@dogs.route("/update-dog/<int:id>", methods=["GET", "POST"])
@login_required
def update(id):
    # Get the dog directly using query
    item = Dogs.query.get(id)
    
    if not item:
        flash("Record not found.", "error")
        return redirect("/")
        
    # Check if user is authorized to update
    if not (current_user.id == item.created_by or current_user.is_admin):
        flash("You are not authorized to update this record.", "error")
        return redirect("/")
    
    if request.method == "POST":
        try:
            item.name = request.form["name"]
            item.show_name = request.form["show_name"]
            item.points = int(request.form["points"]) if request.form["points"] else 0
            item.owner = request.form["owner"]
            
            db.session.commit()
            flash("Record updated successfully.", "success")
            return redirect("/")
        except Exception as e:
            print(f"Error updating dog: {e}")  # For debugging
            db.session.rollback()  # Rollback on error
            flash("Error updating record.", "error")
            return render_template("update-dog.html", item=item)
            
    return render_template("update-dog.html", item=item)


# Delete a record route
@dogs.route("/delete-dog/<int:id>")
@login_required
def delete_dog(id):
    try:
        # Get the dog directly
        item = Dogs.query.get(id)
        if not item:
            flash("Record not found.", "error")
            return redirect("/")
            
        # Check if user is authorized to delete
        if not (current_user.id == item.created_by or current_user.is_admin):
            flash("You are not authorized to delete this record.", "error")
            return redirect("/")
            
        db.session.delete(item)
        db.session.commit()
        flash("Record deleted successfully.", "success")
        return redirect("/")
    except Exception as e:
        print(f"Error deleting dog: {e}")  # For debugging
        db.session.rollback()
        flash("Error deleting record.", "error")
        return redirect("/")

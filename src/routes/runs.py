from flask import Blueprint
from src.models.models import Runs, Dogs, db
from src.models.helpers import delete_item_by_id, query_items, get_item
from src.constants import PLACEMENTS, CLASSES, JUMP_HEIGHTS
from flask import render_template, request, redirect, flash
from flask_login import current_user, login_required
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
@login_required
def create_run(show_name):
    dog = get_item(Dogs, Dogs.show_name, show_name)
    if not dog:
        flash("Dog not found.", "error")
        return redirect("/")

    if request.method == "POST":
        try:
            # Get form data
            run_time = float(request.form.get("run_time"))
            course_time = float(request.form.get("course_time"))
            handler = request.form.get("handler")
            trial = request.form.get("trial")
            judge = request.form.get("judge")
            height = request.form.get("height")
            place = request.form.get("place")
            run_class = request.form.get("run_class")
            timestamp_str = request.form.get("timestamp")
            
            if not timestamp_str:
                flash("Run date is required.", "error")
                raise ValueError("Run date is required")
                
            timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d")

            # Calculate qualification and points
            qualification = run_time <= course_time
            points = points_calc(run_time, course_time)

            # Create new run
            run = Runs(
                name=dog.name,
                pet_id=dog.id,
                show_name=show_name,
                run_time=run_time,
                course_time=course_time,
                qualification=qualification,
                points=points,
                handler=handler or "",  # Ensure not None
                trial=trial or "",
                timestamp=timestamp,
                height=height or "N/A",
                place=place or "N/A",
                judge=judge or "",
                run_class=run_class or "N/A",
                created_by=current_user.id
            )

            db.session.add(run)
            db.session.commit()
            flash("Run added successfully!", "success")
            return redirect(f"/runs/{show_name}")

        except ValueError as e:
            print(f"Validation error creating run: {e}")
            db.session.rollback()
            flash(str(e) if str(e) != "Run date is required" else "Run date is required.", "error")
            return render_template(
                "create-run.html",
                dog=dog,
                placements=sorted(list(PLACEMENTS)),
                classes=sorted(list(CLASSES)),
                heights=sorted(list(JUMP_HEIGHTS)),
            )
        except Exception as e:
            print(f"Error creating run: {e}")
            db.session.rollback()
            flash("Error creating run: Please check all fields are filled correctly.", "error")
            return render_template(
                "create-run.html",
                dog=dog,
                placements=sorted(list(PLACEMENTS)),
                classes=sorted(list(CLASSES)),
                heights=sorted(list(JUMP_HEIGHTS)),
            )

    # GET request
    return render_template(
        "create-run.html",
        dog=dog,
        placements=sorted(list(PLACEMENTS)),
        classes=sorted(list(CLASSES)),
        heights=sorted(list(JUMP_HEIGHTS)),
    )


# Update existing record route
@runs.route("/update-run/<int:id>", methods=["GET", "POST"])
@login_required
def update_run(id):
    item = Runs.query.get(id)
    if not item:
        flash("Record not found.", "error")
        return redirect("/")
        
    # Check if user is authorized to update
    if not (current_user.id == item.created_by or current_user.is_admin):
        flash("You are not authorized to update this record.", "error")
        return redirect(f"/runs/{item.show_name}")
        
    if request.method == "POST":
        try:
            # Update run data
            item.run_time = float(request.form["run_time"])
            item.course_time = float(request.form["course_time"])
            item.handler = request.form.get("handler", "")
            item.points = points_calc(item.run_time, item.course_time)
            item.trial = request.form.get("trial", "")
            
            # Handle date properly
            date_str = request.form["timestamp"]
            try:
                if date_str:
                    item.timestamp = datetime.strptime(date_str, "%Y-%m-%d")
            except ValueError:
                flash("Invalid date format. Please use YYYY-MM-DD.", "error")
                return render_template(
                    "update-run.html", 
                    item=item,
                    placements=sorted(list(PLACEMENTS)),
                    classes=sorted(list(CLASSES)),
                    heights=sorted(list(JUMP_HEIGHTS))
                )
                
            item.height = request.form.get("height", "N/A")
            item.place = request.form.get("place", "N/A")
            item.judge = request.form.get("judge", "")
            item.run_class = request.form.get("run_class", "N/A")

            db.session.commit()
            flash("Run updated successfully.", "success")
            return redirect(f"/runs/{item.show_name}")
        except Exception as e:
            print(f"Error updating run: {e}")
            db.session.rollback()
            flash("Error updating run.", "error")
            return render_template(
                "update-run.html", 
                item=item,
                placements=sorted(list(PLACEMENTS)),
                classes=sorted(list(CLASSES)),
                heights=sorted(list(JUMP_HEIGHTS))
            )
            
    return render_template(
        "update-run.html", 
        item=item,
        placements=sorted(list(PLACEMENTS)),
        classes=sorted(list(CLASSES)),
        heights=sorted(list(JUMP_HEIGHTS))
    )


# Delete a record route
@runs.route("/delete-run/<int:id>")
@login_required
def delete_run(id):
    try:
        item = Runs.query.get(id)
        if not item:
            flash("Record not found.", "error")
            return redirect("/")
            
        # Check if user is authorized to delete
        if not (current_user.id == item.created_by or current_user.is_admin):
            flash("You are not authorized to delete this record.", "error")
            return redirect("/")
            
        show_name = item.show_name
        db.session.delete(item)
        db.session.commit()
        flash("Run deleted successfully.", "success")
        return redirect(f"/runs/{show_name}")
    except Exception as e:
        print(f"Error deleting run: {e}")
        db.session.rollback()
        flash("Error deleting run.", "error")
        return redirect("/")


def points_calc(run_time, course_time):
    points = int(float(course_time) - float(run_time))
    return points if points > 0 else 0

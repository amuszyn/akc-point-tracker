from flask import Blueprint, render_template, request, flash, redirect, url_for 
from flask_login import login_required, current_user
from src.models.models import Event, db
from datetime import datetime
import json
from math import radians, cos, sin, asin, sqrt
from markupsafe import Markup

events = Blueprint("events", __name__)

@events.app_template_filter('from_json')
def from_json(value):
    """Convert a JSON string to Python object."""
    if value:
        return json.loads(value)
    return []

@events.app_template_filter('nl2br')
def nl2br(value):
    """Convert newlines to HTML line breaks."""
    if not value:
        return ''
    return Markup(value.replace('\n', '<br>'))

def haversine(lon1, lat1, lon2, lat2):
    """Calculate the great circle distance between two points on the earth"""
    # Convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    # Radius of earth in miles
    r = 3956
    return c * r

def get_coordinates(zipcode):
    """Get latitude and longitude from zipcode using a geocoding service"""
    # You would need to implement this using a geocoding service
    # For example, using Google Maps API or similar
    # For now, return dummy data
    return (0, 0)

@events.route("/events")
def list_events():
    view_type = request.args.get('view', 'list')  # 'list' or 'calendar'
    zipcode = request.args.get('zipcode')
    radius = request.args.get('radius', 50, type=int)
    
    # Base query for upcoming events
    query = Event.query.filter(Event.end_date >= datetime.utcnow())
    
    if zipcode:
        # If implementing location filtering, you would:
        # 1. Get coordinates for the provided zipcode
        # 2. Calculate distances
        # 3. Filter based on radius
        pass
        
    events = query.order_by(Event.start_date).all()
    
    if view_type == 'calendar':
        return render_template('events/calendar.html', events=events)
    else:
        # Group events by month for list view
        events_by_month = {}
        for event in events:
            month_key = event.start_date.strftime('%B %Y')
            if month_key not in events_by_month:
                events_by_month[month_key] = []
            events_by_month[month_key].append(event)
            
        return render_template('events/list.html', events_by_month=events_by_month)

@events.route("/events/create", methods=["GET", "POST"])
@login_required
def create_event():
    if request.method == "POST":
        try:
            # Get form data
            classes = request.form.getlist('classes_offered')
            
            event = Event(
                name=request.form['name'],
                start_date=datetime.strptime(request.form['start_date'], '%Y-%m-%d'),
                end_date=datetime.strptime(request.form['end_date'], '%Y-%m-%d'),
                location_name=request.form['location_name'],
                address=request.form['address'],
                city=request.form['city'],
                state=request.form['state'],
                zipcode=request.form['zipcode'],
                club_name=request.form['club_name'],
                website=request.form.get('website'),
                entry_fee=float(request.form['entry_fee']) if request.form.get('entry_fee') else None,
                closing_date=datetime.strptime(request.form['closing_date'], '%Y-%m-%d') if request.form.get('closing_date') else None,
                judge_name=request.form.get('judge_name'),
                classes_offered=json.dumps(classes),
                notes=request.form.get('notes'),
                created_by=current_user.id
            )
            
            db.session.add(event)
            db.session.commit()
            flash('Event created successfully!', 'success')
            return redirect(url_for('events.list_events'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error creating event: {str(e)}', 'error')
            return render_template('events/create.html')
            
    return render_template('events/create.html')

@events.route("/events/<int:id>")
def view_event(id):
    event = Event.query.get_or_404(id)
    return render_template('events/view.html', event=event)

@events.route("/events/<int:id>/edit", methods=["GET", "POST"])
@login_required
def edit_event(id):
    event = Event.query.get_or_404(id)
    
    if not (current_user.id == event.created_by or current_user.is_admin):
        flash('You are not authorized to edit this event.', 'error')
        return redirect(url_for('events.view_event', id=id))
        
    if request.method == "POST":
        try:
            classes = request.form.getlist('classes_offered')
            
            event.name = request.form['name']
            event.start_date = datetime.strptime(request.form['start_date'], '%Y-%m-%d')
            event.end_date = datetime.strptime(request.form['end_date'], '%Y-%m-%d')
            event.location_name = request.form['location_name']
            event.address = request.form['address']
            event.city = request.form['city']
            event.state = request.form['state']
            event.zipcode = request.form['zipcode']
            event.club_name = request.form['club_name']
            event.website = request.form.get('website')
            event.entry_fee = float(request.form['entry_fee']) if request.form.get('entry_fee') else None
            event.closing_date = datetime.strptime(request.form['closing_date'], '%Y-%m-%d') if request.form.get('closing_date') else None
            event.judge_name = request.form.get('judge_name')
            event.classes_offered = json.dumps(classes)
            event.notes = request.form.get('notes')
            
            db.session.commit()
            flash('Event updated successfully!', 'success')
            return redirect(url_for('events.view_event', id=id))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating event: {str(e)}', 'error')
            
    return render_template('events/edit.html', event=event)

@events.route("/events/<int:id>/delete", methods=["POST"])
@login_required
def delete_event(id):
    event = Event.query.get_or_404(id)
    
    if not (current_user.id == event.created_by or current_user.is_admin):
        flash('You are not authorized to delete this event.', 'error')
        return redirect(url_for('events.view_event', id=id))
        
    try:
        db.session.delete(event)
        db.session.commit()
        flash('Event deleted successfully!', 'success')
        return redirect(url_for('events.list_events'))
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting event: {str(e)}', 'error')
        return redirect(url_for('events.view_event', id=id)) 
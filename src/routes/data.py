from flask import Blueprint, jsonify, request, send_file
import json
import tempfile
from datetime import datetime
from src.models.models import Dogs, Runs, db

data_bp = Blueprint("data", __name__)

@data_bp.route("/export", methods=["GET"])
def export_data():
    """Export all data as JSON"""
    # Query all data
    dogs = Dogs.query.all()
    runs = Runs.query.all()
    
    # Convert to dictionaries
    dogs_data = [{
        'id': dog.id,
        'name': dog.name,
        'show_name': dog.show_name,
        'points': dog.points,
        'owner': dog.owner
    } for dog in dogs]
    
    runs_data = [{
        'id': run.id,
        'name': run.name,
        'pet_id': run.pet_id,
        'show_name': run.show_name,
        'run_time': run.run_time,
        'course_time': run.course_time,
        'qualification': run.qualification,
        'points': run.points,
        'handler': run.handler,
        'trial': run.trial,
        'timestamp': run.timestamp.isoformat(),
        'height': run.height,
        'place': run.place,
        'judge': run.judge,
        'run_class': run.run_class
    } for run in runs]
    
    # Create export data
    export_data = {
        'dogs': dogs_data,
        'runs': runs_data,
        'export_date': datetime.now().isoformat()
    }
    
    # Create a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix='.json') as tmp:
        tmp.write(json.dumps(export_data, indent=2).encode('utf-8'))
    
    # Send the file
    return send_file(
        tmp.name,
        as_attachment=True,
        download_name=f"dog_data_export_{datetime.now().strftime('%Y%m%d')}.json",
        mimetype="application/json"
    )

@data_bp.route("/import", methods=["POST"])
def import_data():
    """Import data from JSON file"""
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
        
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
        
    try:
        # Read and parse the JSON data
        data = json.loads(file.read().decode('utf-8'))
        
        # Import dogs
        for dog_data in data.get('dogs', []):
            # Check if dog already exists
            existing_dog = Dogs.query.filter_by(show_name=dog_data['show_name']).first()
            if existing_dog:
                # Update existing dog
                existing_dog.name = dog_data['name']
                existing_dog.points = dog_data['points']
                existing_dog.owner = dog_data['owner']
            else:
                # Create new dog
                new_dog = Dogs(
                    name=dog_data['name'],
                    show_name=dog_data['show_name'],
                    points=dog_data['points'],
                    owner=dog_data['owner']
                )
                db.session.add(new_dog)
        
        # Import runs
        for run_data in data.get('runs', []):
            # Check if run already exists
            existing_run = Runs.query.filter_by(id=run_data['id']).first()
            if existing_run:
                # Update existing run
                for key, value in run_data.items():
                    if key != 'id' and key != 'timestamp':
                        setattr(existing_run, key, value)
                if 'timestamp' in run_data:
                    existing_run.timestamp = datetime.fromisoformat(run_data['timestamp'])
            else:
                # Create new run
                new_run = Runs(
                    name=run_data['name'],
                    pet_id=run_data['pet_id'],
                    show_name=run_data['show_name'],
                    run_time=run_data['run_time'],
                    course_time=run_data['course_time'],
                    qualification=run_data['qualification'],
                    points=run_data['points'],
                    handler=run_data['handler'],
                    trial=run_data['trial'],
                    timestamp=datetime.fromisoformat(run_data['timestamp']),
                    height=run_data['height'],
                    place=run_data['place'],
                    judge=run_data['judge'],
                    run_class=run_data['run_class']
                )
                db.session.add(new_run)
        
        # Commit changes
        db.session.commit()
        return jsonify({'success': 'Data imported successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500 
from flask import Blueprint, render_template
from sqlalchemy import func, desc
from src.models.models import Dogs, Runs, db
from src.constants import JUMP_HEIGHTS

leaderboard = Blueprint("leaderboard", __name__)

@leaderboard.route("/leaderboards")
def show_leaderboards():
    print("Rendering leaderboard template...")
    try:
        # Get top 10 dogs by points
        top_dogs_by_points = Dogs.query.order_by(desc(Dogs.points)).limit(10).all()
        
        # Get fastest runs per jump height
        fastest_runs_by_height = {}
        
        for height in JUMP_HEIGHTS:
            # Get the fastest run for each jump height
            fastest_runs = Runs.query.filter(
                Runs.height == height,
                Runs.run_time > 0  # Ensure valid run times
            ).order_by(Runs.run_time).limit(5).all()
            
            fastest_runs_by_height[height] = fastest_runs
        
        # Get dogs with most runs
        dogs_with_most_runs = db.session.query(
            Runs.show_name, 
            func.count(Runs.id).label('run_count')
        ).group_by(
            Runs.show_name
        ).order_by(
            desc('run_count')
        ).limit(10).all()
        
        # Get dogs with most qualifications
        dogs_with_most_quals = db.session.query(
            Runs.show_name, 
            func.count(Runs.id).label('qual_count')
        ).filter(
            Runs.qualification == True
        ).group_by(
            Runs.show_name
        ).order_by(
            desc('qual_count')
        ).limit(10).all()
        
        return render_template(
            "leaderboard.html",
            top_dogs_by_points=top_dogs_by_points,
            fastest_runs_by_height=fastest_runs_by_height,
            dogs_with_most_runs=dogs_with_most_runs,
            dogs_with_most_quals=dogs_with_most_quals,
            jump_heights=sorted(JUMP_HEIGHTS, key=lambda x: int(x) if x.isdigit() else 0, reverse=True)
        )
    except Exception as e:
        print(f"Error rendering template: {e}")
        # Return a simple response for debugging
        return f"Error: {e}", 500

    return render_template(
        "leaderboard.html",
        top_dogs_by_points=top_dogs_by_points,
        fastest_runs_by_height=fastest_runs_by_height,
        dogs_with_most_runs=dogs_with_most_runs,
        dogs_with_most_quals=dogs_with_most_quals,
        jump_heights=sorted(JUMP_HEIGHTS, key=lambda x: int(x) if x.isdigit() else 0, reverse=True)
    ) 
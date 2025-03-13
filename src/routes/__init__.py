from src.routes.blueprint import blueprint
from src.routes.dogs import dogs
from src.routes.runs import runs
from src.routes.search import search
from src.routes.leaderboard import leaderboard
from src.routes.auth import auth
from src.routes.events import events

# Export all blueprints
__all__ = ['blueprint', 'dogs', 'runs', 'search', 'leaderboard', 'auth', 'events']

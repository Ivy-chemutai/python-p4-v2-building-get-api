from flask import Flask, jsonify, make_response, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from models import db, User, Review, Game

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return "Index for Game/Review/User API"

# start building your API here
@app.route('/games', methods=['GET', 'POST'])
def games():
    if request.method == 'GET':
        games = [game.to_dict() for game in Game.query.all()]
        return make_response(games, 200)
    
    elif request.method == 'POST':
        print(f"Content-Type: {request.content_type}")
        print(f"Raw data: {request.data}")
        try:
            data = request.get_json()
            print(f"Parsed JSON: {data}")
            if not data:
                return make_response({'error': 'No JSON data provided'}, 400)
            
            required_fields = ['title', 'genre', 'platform', 'price']
            for field in required_fields:
                if field not in data:
                    return make_response({'error': f'Missing required field: {field}'}, 400)
            
            new_game = Game(
                title=data['title'],
                genre=data['genre'],
                platform=data['platform'],
                price=data['price']
            )
            db.session.add(new_game)
            db.session.commit()
            return make_response(new_game.to_dict(), 201)
        except Exception as e:
            print(f"Exception: {e}")
            return make_response({'error': str(e)}, 400)

@app.route('/games/<int:id>')
def game_by_id(id):
    game = Game.query.filter(Game.id == id).first()

    game_dict = game.to_dict()

    response = make_response(
        game_dict,
        200
    )

    return response

@app.route('/games/users/<int:id>')
def game_users_by_id(id):
    game = Game.query.filter(Game.id == id).first()

    # use association proxy to get users for a game
    users = [user.to_dict(rules=("-reviews",)) for user in game.users]
    response = make_response(
        users,
        200
    )

    return response

if __name__ == '__main__':
    app.run(port=5000, debug=True)
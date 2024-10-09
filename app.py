from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
import uuid
import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///connections.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class UserConnection(db.Model):
    id = db.Column(db.String(36), primary_key=True)
    count = db.Column(db.Integer, default=1)
    last_visit = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __init__(self, id):
        self.id = id
        self.count = 1
        self.last_visit = datetime.datetime.utcnow()

@app.route('/')
def index():
    user_id = request.cookies.get('user_id')
    current_time = datetime.datetime.utcnow()

    if not user_id:
        user_id = str(uuid.uuid4())
        new_connection = UserConnection(id=user_id)
        db.session.add(new_connection)
        db.session.commit()
        response = make_response(jsonify(message=f"Bienvenue ! Nombre de connexions pour cet utilisateur: 1"))
        response.set_cookie('user_id', user_id)
        return response
    else:
        user_connection = UserConnection.query.filter_by(id=user_id).first()
        if user_connection:
            last_visit = user_connection.last_visit
            # Supposons qu'une nouvelle session est commencée après 30 minutes d'inactivité
            if (current_time - last_visit).total_seconds() > 1800:
                user_connection.count += 1
            user_connection.last_visit = current_time
            db.session.commit()
        else:
            new_connection = UserConnection(id=user_id)
            db.session.add(new_connection)
            db.session.commit()

        return jsonify(message=f"Nombre de connexions pour cet utilisateur: {user_connection.count if user_connection else 1}")

@app.route('/stats')
def stats():
    all_connections = UserConnection.query.all()
    stats = {conn.id: {"count": conn.count, "last_visit": conn.last_visit} for conn in all_connections}
    return jsonify(stats)

if __name__ == '__main__':
    # Initialiser la base de données
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000, debug=True)

from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/messages', methods=["GET", "POST"])
def messages():
    if request.method == 'GET':
        return make_response([ x.to_dict() for x in Message.query.order_by(Message.created_at).all()], 200, {'Content-Type': 'application/json'})
    elif request.method == 'POST':
        json = request.get_json()
        username, body = json['username'], json['body']
        m = Message(username=username, body=body)
        db.session.add(m)
        db.session.commit()
        return make_response(m.to_dict(), 201, {'Content-Type': 'application/json'})
    

@app.route('/messages/<int:id>', methods=["PATCH", "DELETE"])
def messages_by_id(id):
    if request.method == 'PATCH':
        json = request.get_json()
        m = Message.query.filter_by(id=id).first()
        for attr in json:
            setattr(m, attr, json[attr])
        db.session.add(m)
        db.session.commit()
        return make_response(m.to_dict(), 200, {'Content-Type': 'application/json'})
    elif request.method == 'DELETE':
        m = Message.query.filter_by(id=id).first()
        db.session.delete(m)
        db.session.commit()
        return make_response(m.to_dict(), 200, {'Content-Type': 'application/json'})

if __name__ == '__main__':
    app.run(port=5555)

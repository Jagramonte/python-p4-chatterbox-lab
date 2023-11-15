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

@app.route('/messages',methods = ['GET', 'POST'])
def messages():
    if request.method == 'GET':
        messages = [message.to_dict() for message in Message.query.all()]
        return make_response (messages, 200)
    
    if request.method == 'POST':
        params = request.json
        new_message = Message(body = params['body'], username = params['username'])
        db.session.add(new_message)
        db.session.commit()
        message_dict = {
            'id': new_message.id, 'body': new_message.body, 'username': new_message.username
        }
        return make_response(message_dict, 201)

@app.route('/messages/<int:id>',methods = ['PATCH', 'DELETE'])
def messages_by_id(id):
    message = Message.query.get(id)
    if not message:
        return make_response( {'error': 'message not found'}, 404 )
    if request.method == 'PATCH':
        params = request.json
        for attr in params:
            setattr( message, attr, params[attr] )
        db.session.commit()
        return make_response( message.to_dict(), 200 )
    
    if request.method == 'DELETE':
        db.session.delete(message)
        db.session.commmit()
        return make_response('', 204)


if __name__ == '__main__':
    app.run(port=5000)

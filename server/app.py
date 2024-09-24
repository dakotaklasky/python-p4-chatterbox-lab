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

@app.route('/messages', methods = ['GET','POST'])
def messages():
    if request.method == 'GET':
        #returns array of all messages as JSON ordered by created_at
        messages = Message.query.order_by("created_at").all()
        return [m.to_dict() for m in messages], 200
    
    elif request.method == 'POST':
        data = request.get_json()
        new_message = Message(body = data.get('body'), username = data.get('username'))
        db.session.add(new_message)
        db.session.commit()
        return new_message.to_dict(), 201


@app.route('/messages/<int:id>', methods = ['PATCH','DELETE'])
def messages_by_id(id):

    message = Message.query.filter(Message.id == id).first()

    if message is None:
        return {'error':'message not found'}, 404

    if request.method == 'PATCH':
        data = request.get_json()
        if 'body' in data:
            message.body = data['body']
        db.session.add(message)
        db.session.commit()
        return message.to_dict(), 200
    
    elif request.method == 'DELETE':
        
        db.session.delete(message)
        db.session.commit()
        return {"delete_successful": True, "message":"Message deleted"}, 200

if __name__ == '__main__':
    app.run(port=5555)

from flask import Flask, request, jsonify

from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.sqlite')
db = SQLAlchemy(app)
ma = Marshmallow(app)

class HotMember(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=False)
    birth_name = db.Column(db.String(100), unique=False)
    quirk = db.Column(db.String(50), unique=False)
    age = db.Column(db.Integer, unique=False)
    rank = db.Column(db.Integer, unique=False)
    location = db.Column(db.String(100), unique=False)
    villain_vigilante = db.Column(db.String(15), unique=False)
    description = db.Column(db.String(144), unique=False)


    def __init__(self, name, birth_name, quirk, age, rank, location, villain_vigilante, description):
        self.name = name
        self.birth_name = birth_name
        self.quirk = quirk
        self.age = age
        self.rank = rank
        self.location = location
        self.villain_vigilante = villain_vigilante
        self.description = description

class HotSchema(ma.Schema):
    class Meta:
        fields = ('name', 'birth_name', 'quirk', 'age', 'rank', 'location', 'villain_vigilante', 'description', 'id')

hot_schema = HotSchema()
hots_schema = HotSchema(many=True)

# Endpoint to create a new guide
@app.route('/member', methods=['POST'])
def add_member():
    name = request.json['name']
    birth_name = request.json['birth_name']
    quirk = request.json['quirk']
    age = request.json['age']
    rank = request.json['rank']
    location = request.json['location']
    villain_vigilante = request.json['villain_vigilante']
    description = request.json['description']

    new_member = HotMember(name, birth_name, quirk, age, rank, location, villain_vigilante, description)

    db.session.add(new_member)
    db.session.commit()

    member = HotMember.query.get(new_member.id)
    return hot_schema.jsonify(member)

# Endpoint to query all guides
@app.route('/members', methods=["GET"])
def get_guides():
    all_members = HotMember.query.all()
    result = hots_schema.dump(all_members)
    return jsonify(result)


# Endpoint for querying a single guide
@app.route('/member/<id>', methods=['GET'])
def get_guide(id):
    member = HotMember.query.get(id)
    return hot_schema.jsonify(member)


# Endpoint for updating guide
@app.route('/member/<id>', methods=["PUT"])
def guide_update(id):
    member = HotMember.query.get(id)
    name = request.json['name']
    birth_name = request.json['birth_name']
    quirk = request.json['quirk']
    age = request.json['age']
    rank = request.json['rank']
    location = request.json['location']
    villain_vigilante = request.json['villain_vigilante']
    description = request.json['description']

    if member:
        member.name = name
        member.birth_name = birth_name
        member.quirk = quirk
        member.age = age
        member.rank = rank
        member.location = location
        member.villain_vigilante = villain_vigilante
        member.description = description

        db.session.commit()
        return hot_schema.jsonify(member)
    else:
        return "User not found"


# Endpoint for deleting a record
@app.route('/member/<id>', methods=["DELETE"])
def guide_delete(id):
    member = HotMember.query.get(id)
    db.session.delete(member)
    db.session.commit()

    return "Guide was succesfully deleted!"

if __name__ == '__main__':
    app.run(debug=True, port=8000)
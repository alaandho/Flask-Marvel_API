from flask import Blueprint, json, request, jsonify
from marvel_api.helpers import token_required
from marvel_api.models import db, User, Marvel, marvel_schema, marvels_schema


api = Blueprint('api', __name__, url_prefix='/api')


@api.route('/getdata')
def getdata():
    return {'some_value': 52, 'another_value': 800}

#CREATE MARVEL API ENDPOINT
@api.route('/marvels', methods = ['POST'])
@token_required
def create_marvel(current_user_token):
    name = request.json['name']
    description = request.json['description']
    comics_appeared_in = request.json['comics_appeared_in']
    super_power = request.json['super_power']
    user_token = current_user_token.token

    print(f'TESTER: {current_user_token.token}')

    marvel = Marvel(name, description, comics_appeared_in, super_power, user_token = user_token)

    db.session.add(marvel)
    db.session.commit()

    response = marvel_schema.dump(marvel)
    return jsonify(response)

#Retrieve all marvel
@api.route('/marvels', methods = ['GET'])
@token_required
def get_marvels(current_user_token):
    owner = current_user_token.token
    marvels = Marvel.query.filter_by(user_token = owner).all()
    response = marvels_schema.dump(marvels)
    return jsonify(response)

#Retrieve single marvel endpoint
@api.route('/marvels/<id>', methods = ['GET'])
@token_required
def get_marvel(current_user_token, id):
    marvel = Marvel.query.get(id)
    response = marvel_schema.dump(marvel)
    return jsonify(response)


#Update a marvel by ID Enpoint
@api.route('/marvels/<id>', methods = ['POST'])
@token_required
def update_marvel(current_user_token, id):
    marvel = Marvel.query.get(id)
    print(marvel)
    if marvel:
        marvel.name = request.json['name']
        marvel.description = request.json['description']
        marvel.comics_appeared_in = request.json['comics_appeared_in']
        marvel.super_power = request.json['super_power']
        marvel.user_token = current_user_token.token
        db.session.commit()

        response = marvel_schema.dump(marvel)
        return jsonify(response)
    else:
        return jsonify({'Error': 'That Marvel does not exist!'})

#Delete marvel by ID
@api.route('/marvels/<id>', methods = ['DELETE'])
@token_required
def delete_marvel(current_user_token, id):
    marvel = Marvel.query.get(id)
    if marvel:
        db.session.delete(marvel)
        db.session.commit()

        response = marvel_schema.dump(marvel)
        return jsonify(response)
    else:
        return jsonify({'Error': 'That Marvel does not exist!'})
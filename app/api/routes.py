from flask import Blueprint, request, jsonify, render_template
from helpers import token_required
from models import db, User, Contact, contact_schema, contacts_schema

api = Blueprint('api',__name__, url_prefix='/api')

@api.route('/getdata')
def getdata():
    return{'test': 'test'}

@api.route('/contacts', methods = ['POST'])
@token_required
def create_contact(current_user_token):
    make = request.json['make']
    model = request.json['model']
    year = request.json['year']
    price = request.json['price']
    body_style = request.json['body_style']
    mileage = request.json['mileage']
    user_token = current_user_token.token

    print(f'BIG TESTER: {current_user_token.token}')

    contact = Contact(make, model, year, price, body_style, mileage, user_token = user_token )

    db.session.add(contact)
    db.session.commit()

    response = contact_schema.dump(contact)
    return jsonify(response)

@api.route('/contacts', methods = ['GET'])
@token_required
def get_contact(current_user_token):
    a_user = current_user_token.token
    contacts = Contact.query.filter_by(user_token = a_user).all()
    response = contacts_schema.dump(contacts)
    return jsonify(response)

@api.route('/contacts/,<id>', methods = ['GET'])
@token_required
def get_single_contact(current_user_token, id):
    contact = Contact.query.get(id)
    response = contact_schema.dump(contact)
    return jsonify(response)

@api.route('/contacts/<id>', methods = ['POST', 'PUT'])
@token_required
def update_contact(current_user_token, id):
    contact = Contact.query.get(id)
    contact.make = request.json['make']
    contact.model = request.json['model']
    contact.year = request.json['year']
    contact.price = request.json['price']
    contact.body_style = request.json['body_style']
    contact.mileage = request.json['mileage']
    contact.user_token = current_user_token.token

    db.session.commit()
    response = contact_schema.dump(contact)
    return jsonify(response)

@api.route('/contacts/<id>', methods = ['DELETE'])
@token_required
def delete_contact(current_user_token, id):
    contact = Contact.query.get(id)
    db.session.delete(contact)
    db.session.commit()
    response = contact_schema.dump(contact)
    return jsonify(response)

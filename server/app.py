#!/usr/bin/env python3

from flask import Flask, request, jsonify, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Plant

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)

# GET all plants
@app.route('/plants', methods=['GET'])
def get_plants():
    plants = Plant.query.all()
    plants_list = []
    for plant in plants:
        plant_dict = {
            'id': plant.id,
            'name': plant.name,
            'image': plant.image,
            'price': plant.price,
            'is_in_stock': plant.is_in_stock
        }
        plants_list.append(plant_dict)
    return jsonify(plants_list)

# GET single plant by ID
@app.route('/plants/<int:id>', methods=['GET'])
def get_plant_by_id(id):
    plant = db.session.get(Plant, id)
    if plant:
        plant_dict = {
            'id': plant.id,
            'name': plant.name,
            'image': plant.image,
            'price': plant.price,
            'is_in_stock': plant.is_in_stock
        }
        return jsonify(plant_dict)
    else:
        return jsonify({'error': 'Plant not found'}), 404

# PATCH route - Update a plant
@app.route('/plants/<int:id>', methods=['PATCH'])
def update_plant(id):
    plant = db.session.get(Plant, id)
    
    if not plant:
        return jsonify({'error': 'Plant not found'}), 404
    
    data = request.get_json()
    
    # Update plant attributes if they exist in the request data
    if 'name' in data:
        plant.name = data['name']
    if 'image' in data:
        plant.image = data['image']
    if 'price' in data:
        plant.price = data['price']
    if 'is_in_stock' in data:
        plant.is_in_stock = data['is_in_stock']
    
    # Commit changes to database
    db.session.commit()
    
    # Return updated plant as JSON
    response_data = {
        'id': plant.id,
        'name': plant.name,
        'image': plant.image,
        'price': plant.price,
        'is_in_stock': plant.is_in_stock
    }
    
    return jsonify(response_data)

# DELETE route - Delete a plant
@app.route('/plants/<int:id>', methods=['DELETE'])
def delete_plant(id):
    plant = db.session.get(Plant, id)
    
    if not plant:
        return jsonify({'error': 'Plant not found'}), 404
    
    # Delete plant from database
    db.session.delete(plant)
    db.session.commit()
    
    # Return empty response with 204 status code
    return make_response('', 204)

if __name__ == '__main__':
    app.run(port=5555, debug=True)
    
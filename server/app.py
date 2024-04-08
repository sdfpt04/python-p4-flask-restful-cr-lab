#!/usr/bin/env python3

from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Plant

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = True

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

class Plants(Resource):
    def get(self):
        plants = Plant.query.all()
        return jsonify([plant.serialize() for plant in plants])

    def post(self):
        data = request.json
        name = data.get('name')
        price = data.get('price')
        # Check if the 'name' and 'price' fields are provided
        if not name or not price:
            return jsonify({'error': 'Name and Price are required fields'}), 400
        # Set a default image if not provided
        image = data.get('image', 'default.jpg')
        new_plant = Plant(name=name, image=image, price=price)
        db.session.add(new_plant)
        db.session.commit()
        return jsonify(new_plant.serialize()), 201


class PlantByID(Resource):
    def get(self, id):
        plant = Plant.query.get(id)
        if plant:
            return jsonify(plant.serialize())
        else:
            return jsonify({'error': 'Plant not found'}), 404

api.add_resource(Plants, '/plants')
api.add_resource(PlantByID, '/plants/<int:id>')

if __name__ == '__main__':
    app.run(port=5555, debug=True)


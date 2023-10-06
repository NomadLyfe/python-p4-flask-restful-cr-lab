#!/usr/bin/env python3

from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource
import ipdb

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
        plants = []
        for plant in Plant.query.all():
            plants.append(plant.to_dict())
        response = make_response(plants, 200)
        return response
    
    def post(self):
        plant = Plant(
            name=request.get_json()['name'],
            image=request.get_json()['image'],
            price=request.get_json()['price']
        )
        db.session.add(plant)
        db.session.commit()
        response = make_response(plant.to_dict(), 201)
        return response
    
api.add_resource(Plants, '/plants')

class PlantByID(Resource):
    def get(self, id):
        plant = Plant.query.filter_by(id = id).first()
        response = make_response(plant.to_dict(), 200)
        return response
        
api.add_resource(PlantByID, '/plants/<int:id>')

if __name__ == '__main__':
    app.run(port=5555, debug=True)

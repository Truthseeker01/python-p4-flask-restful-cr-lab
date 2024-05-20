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

        return [p.to_dict() for p in Plant.query.all()], 200
    
    def post(self):
        plant = Plant(name=request.json['name'],
                    image=request.json['image'],
                    price=request.json['price'])
        db.session.add(plant)
        db.session.commit()
        return plant.to_dict(), 201
    
api.add_resource(Plants, '/plants')

class PlantByID(Resource):
    
    def get(self, id):

        p = Plant.query.filter_by(id=id).first()
        return p.to_dict(), 200
    
api.add_resource(PlantByID, '/plants/<int:id>')
        


if __name__ == '__main__':
    app.run(port=5555, debug=True)

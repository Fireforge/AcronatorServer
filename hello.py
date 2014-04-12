import os
from flask import Flask
from flask.ext import restful
from flask.ext.restful.utils import cors
from flask.ext.restful import reqparse

app = Flask(__name__)
api = restful.Api(app)

class HelloWorld(restful.Resource):
    @cors.crossdomain(origin='*')
    def get(self):
        return {'hello': 'world'}, 200
    @cors.crossdomain(origin='*')
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str)
        parser.add_argument('des', type=str)
        args = parser.parse_args()
        return {'name': args['name'], 'des': args['des']}, 200

api.add_resource(HelloWorld, '/')

api.add_resource(HelloWorld, '/api')
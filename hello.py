import os
from flask import Flask
from flask.ext import restful

app = Flask(__name__)
api = restful.Api(app)

class HelloWorld(restful.Resource):
    def get(self):
        return {'hello': 'world'}, 200, {'Access-Control-Allow-Origin': '*'}

api.add_resource(HelloWorld, '/')
@cross_origin()
import os
from flask import Flask
from flask.ext import restful

app = Flask(__name__)
api = restful.Api(app)

class HelloWorld(restful.Resource):
    def get(self):
        return flask.jsonify({'hello': 'world'})

api.add_resource(HelloWorld, '/')
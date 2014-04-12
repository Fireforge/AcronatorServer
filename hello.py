import os
from flask import Flask
from flask.ext import restful

app = Flask(__name__)
api = restful.Api(app)

class HelloWorld(restful.Resource):
    def get(self):
        f = {'hello': 'world'}
        return flask.jsonify(**f)

api.add_resource(HelloWorld, '/')
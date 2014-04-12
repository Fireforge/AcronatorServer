import os
from flask import Flask
from flask.ext import restful

app = Flask(__name__)
api = restful.Api(app)

class HelloWorld(restful.Resource):
    @cross_origin()
    def get(self):
        return {'hello': 'world'}

api.add_resource(HelloWorld, '/')
@cross_origin()
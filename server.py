import os
from flask import Flask
from flask.ext import restful
from flask.ext.restful.utils import cors
from flask.ext.restful import reqparse
import acronization

app = Flask(__name__)
api = restful.Api(app)

class HelloWorld(restful.Resource):
    def get(self):
        return {'API Docs': 'https://github.com/Fireforge/AcronatorServer'}, 200, {'Access-Control-Allow-Origin' : '*'}

class HelloWorld2(restful.Resource):
    def get(self, acronym, des):
        results = acronization.acronym_finder(acronym, des)

        return {'acronym': acronym, 'des': des, 'result': results}, 200, {'Access-Control-Allow-Origin' : '*'}

api.add_resource(HelloWorld, '/')
api.add_resource(HelloWorld2, '/<string:acronym>&<string:des>')

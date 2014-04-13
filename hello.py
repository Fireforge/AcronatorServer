import os
from flask import Flask
from flask.ext import restful
from flask.ext.restful.utils import cors
from flask.ext.restful import reqparse
import acronization

app = Flask(__name__)
api = restful.Api(app)
#api.decorators=[cors.crossdomain(origin='*')]

class HelloWorld(restful.Resource):
    def get(self):

        return {'hello': 'world'}, 200, {'Access-Control-Allow-Origin' : '*'}
    """
    @cors.crossdomain(origin='*')
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str)
        parser.add_argument('des', type=str)
        args = parser.parse_args()

        results = test.acronym_finder(args['name'],5,args['des'])

        return {'results': results.split("\n")}, 200, {'Access-Control-Allow-Origin' : '*'}
    """
class HelloWorld2(restful.Resource):
    def get(self, acronym, des):
        results = acronization.acronym_finder(acronym,5,des)
        return {'acronym': acronym, 'des': des, 'result': results}, 200, {'Access-Control-Allow-Origin' : '*'}

api.add_resource(HelloWorld, '/')
api.add_resource(HelloWorld2, '/<string:acronym>&<string:des>')
api.add_resource(HelloWorld, '/api')
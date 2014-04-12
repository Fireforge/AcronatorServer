import os
from flask import Flask
from flask.ext import restful
from flask.ext.restful.utils import cors
from flask.ext.restful import reqparse
import test

app = Flask(__name__)
api.decorators=[cors.crossdomain(origin='*')]
api = restful.Api(app)

class HelloWorld(restful.Resource):
    def get(self):
        return {'hello': 'world'}, 200

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str)
        parser.add_argument('des', type=str)
        args = parser.parse_args()

        results = test.acronym_finder(args['name'],5,args['des'])

        return {'results': results.split("\n")}, 200

api.add_resource(HelloWorld, '/')

api.add_resource(HelloWorld, '/api')

if __name__ == '__main__':
    app.run(debug=True)
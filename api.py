import json

from flask import Flask, request, jsonify
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)

with open('azure_geos.json') as file:
    app_json = json.loads(file.read())

        
class AzureRegions(Resource):
    def get(self, ):
        if request.method == 'GET':
            return jsonify(app_json)


class AzureSingleRegion(Resource):
     def get(self, location):
        request.data = location
        if request.method == 'GET':
            output_dict = [x for x in app_json if x['name'] == request.data]
            return output_dict
        else:
            return {'error': 'fetch error'}


api.add_resource(AzureRegions, '/list/azure/region/geography/')
api.add_resource(AzureSingleRegion, '/get/azure/region/geography/<string:location>')

if __name__ == '__main__': 
	app.run(debug=True)

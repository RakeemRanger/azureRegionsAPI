import json
import os

from flask import Flask, request
from flask_restful import Api, Resource
from azure.identity import DefaultAzureCredential
from azure.mgmt.subscription import SubscriptionClient

from CONSTANTS import AZURE_SUBSCRIPTION_ID


app = Flask(__name__)
api = Api(app)


def azure_sub_locations():
    '''
    In a production environment, this function may live in a separate file 
    (best practice is to store all of your client connections in a separate file and or folder.
    this way you enable source control, versioning, collaboration, and security best practices). 
    This function is used to get the Azure regions and their respective latitude and longitude.
    I am storing my subscription id in an CONSTANTS file which calls a env variable for security purposes.
    you can create an environment variable by running the below command in your terminal:
    linux: > export AZURE_SUBSCRIPTION_ID="your_subscription_id"
    windows: > $AZURE_SUBSCRIPTION_ID = "your_subscription_id"
    '''
    creds = DefaultAzureCredential()
    sub_client = SubscriptionClient(creds,)
    subscription = sub_client.subscriptions.list_locations(os.getenv('AZURE_SUBSCRIPTION_ID'))
    empty = []
    for location in subscription:
        empty.append({"name" : f'{location.name}', "latitude" : f'{location.latitude}', "longitude" : f'{location.longitude}'})
    api_json = json.loads(json.dumps(empty))
    return api_json
        
 
class AzureRegions(Resource):
    def get(self, ):
        '''
        returns a list of Azure regions and their respective latitude and longitude.
        '''
        if request.method == 'GET':
            app_json = azure_sub_locations()
            return app_json


class AzureSingleRegion(Resource):
     def get(self, location):
        '''
        returns a single Azure region and its respective latitude and longitude.
        '''
        request.data = location
        app_json = azure_sub_locations()
        if request.method == 'GET':
            output_dict = [x for x in app_json if x['name'] == request.data]
            return output_dict


api.add_resource(AzureRegions, '/list/azure/region/geography/')
api.add_resource(AzureSingleRegion, '/get/azure/region/geography/<string:location>')

if __name__ == '__main__': 
	app.run()

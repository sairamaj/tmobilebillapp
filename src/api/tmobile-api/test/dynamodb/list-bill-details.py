import boto3
import json
from boto3.dynamodb.conditions import Key

# Get the service resource.
dynamodb = boto3.resource(
    'dynamodb',
    endpoint_url='http://127.0.0.1:8000'
)

table = dynamodb.Table('TMobile')

class Primary:
    def __init__(self,primary):
        self.primary = primary


bills = table.query(
    KeyConditionExpression=Key('Name').eq('Bills') & Key('Type').begins_with('Details_Jan2020')
)

#print(users["Items"])
print(len(bills['Items']))
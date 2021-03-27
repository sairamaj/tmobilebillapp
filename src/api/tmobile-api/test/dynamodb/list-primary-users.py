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


users = table.query(
    KeyConditionExpression=Key('Name').eq('Users')
)

#print(users["Items"])
print(users["Items"][0]["Value"])
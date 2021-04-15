import boto3
import json
from boto3.dynamodb.conditions import Key

# Get the service resource.
dynamodb = boto3.resource(
    'dynamodb',
    endpoint_url='http://127.0.0.1:8000'
)
# dynamodb = boto3.resource(
#     'dynamodb'
# )

print(dynamodb)
table = dynamodb.Table('TMobile')

class Primary:
    def __init__(self,primary):
        self.primary = primary


users = table.query(
    KeyConditionExpression=Key('Name').eq('Users')& Key('Type').begins_with('Roles')
)

#print(users["Items"])
if len(users["Items"]) > 0:
    print(users["Items"][0]["Value"])
else:
    print('no roles found')
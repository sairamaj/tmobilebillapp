import boto3
from boto3.dynamodb.conditions import Key

# Get the service resource.
dynamodb = boto3.resource(
    'dynamodb',
    endpoint_url='http://localhost:8000'
)

table = dynamodb.Table('TMobile')

response = table.query(
    KeyConditionExpression=Key('Name').eq('PhoneNames')
)

print(response["Items"])

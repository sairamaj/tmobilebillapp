import boto3

table = boto3.resource(
    'dynamodb',
    endpoint_url='http://192.168.99.100:8000'
)

print(table)
import boto3
# Get the service resource.
dynamodb = boto3.resource(
    'dynamodb',
    endpoint_url='http://localhost:8000'
)

table = dynamodb.Table('TMobile')

with open ("sampleusers.json", "r") as f:
    data=f.read()
table.put_item(
   Item={
        'Name': 'Users',
        'Type': 'Details',
        'Value': data
    }
)
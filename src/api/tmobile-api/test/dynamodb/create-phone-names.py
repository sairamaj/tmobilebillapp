import boto3
# Get the service resource.
dynamodb = boto3.resource(
    'dynamodb',
    endpoint_url='http://localhost:8000'
)

table = dynamodb.Table('TMobile')

table.put_item(
   Item={
        'Name': 'PhoneNames',
        'Type': 'User1',
        'Phone': '503 111 1111'
    }
)

table.put_item(
   Item={
        'Name': 'PhoneNames',
        'Type': 'User2',
        'Phone': '503 222 2222'
    }
)
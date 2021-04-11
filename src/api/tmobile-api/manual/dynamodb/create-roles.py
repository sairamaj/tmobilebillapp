import boto3
# Get the service resource.
dynamodb = boto3.resource(
    'dynamodb',
    endpoint_url='http://localhost:8000'
)
#
#dynamodb = boto3.resource(
#    'dynamodb'
#)

table = dynamodb.Table('TMobile')

with open ("c:\\sai\\dev\\temp\\pdf\\tmobile\\userroles.json", "r") as f:
    data=f.read()
table.put_item(
   Item={
        'Name': 'Users',
        'Type': 'Roles',
        'Value': data
    }
)

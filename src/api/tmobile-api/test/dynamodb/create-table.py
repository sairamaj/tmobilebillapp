import boto3

# Get the service resource.
dynamodb = boto3.resource(
    'dynamodb',
    endpoint_url='http://localhost:8000'
)

# Create the DynamoDB table.
table = dynamodb.create_table(
    TableName='TMobile',
    KeySchema=[
        {
            'AttributeName': 'Name',
            'KeyType': 'HASH'
        },
        {
            'AttributeName': 'Type',
            'KeyType': 'RANGE'
        }
    ],
    AttributeDefinitions=[
        {
            'AttributeName': 'Name',
            'AttributeType': 'S'
        },
        {
            'AttributeName': 'Type',
            'AttributeType': 'S'
        },
    ],
    ProvisionedThroughput={
        'ReadCapacityUnits': 2,
        'WriteCapacityUnits': 2
    }
)

# Wait until the table exists.
table.meta.client.get_waiter('table_exists').wait(TableName='TMobile')

# Print out some data about the table.
print(table.item_count)

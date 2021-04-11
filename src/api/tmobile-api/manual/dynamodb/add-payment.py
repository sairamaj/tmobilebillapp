import boto3
from decimal import Decimal
def floatToDecimal(val):
    return Decimal(format(val, ".15g"))

# Get the service resource.
dynamodb = boto3.resource(
    'dynamodb',
    endpoint_url='http://localhost:8000'
)
# dynamodb = boto3.resource(
#     'dynamodb'
# )

table = dynamodb.Table('TMobile')

table.put_item(
   Item={
        'Name': 'Payments',
        'Type': 'Apr2020User1',
        'Amount': "{:.2f}".format(floatToDecimal(3.33)),
        'Date': '04/01/2020',
        'Method': 'PayPal'
    }
)

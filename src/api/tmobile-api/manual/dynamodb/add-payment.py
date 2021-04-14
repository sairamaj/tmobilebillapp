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
        'Type': 'Payment_User1',
        'Amount': "{:.2f}".format(floatToDecimal(233.10)),
        'Date': '04/12/2020',
        'Method': 'PayPal',
        'Comment': 'For 2020'
    }
)

yearMonths = ['Jan2020','Feb2020','Mar2020']
user = 'User1'
for y in yearMonths:
    print()
    table.put_item(
   Item={
        'Name': 'Payments',
        'Type': f'{user}_{y}'
    }
)



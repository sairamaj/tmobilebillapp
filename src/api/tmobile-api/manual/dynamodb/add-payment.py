import boto3
import sys
import uuid
from decimal import Decimal

# Get the service resource.
dynamodb = boto3.resource(
    'dynamodb',
    endpoint_url='http://127.0.0.1:8000'
)
# dynamodb = boto3.resource(
#     'dynamodb'
# )

table = dynamodb.Table('TMobile')

print(dynamodb)
class Payment:
    def __init__(self, line):
        parts = line.split('|')
        self.Name = parts[0]
        self.Amount = parts[1]
        self.Date = parts[2]
        self.Method = parts[3]
        self.Comment = parts[4]
        self.Id = str(uuid.uuid1())

paymentFile = sys.argv[1]
with open(paymentFile, "r") as f:
    for line in f:
        line = line.strip('\n')
        payment = Payment(line)
        print(f'adding :{payment.Name}:{payment.Id}')
        table.put_item(
            Item={
                'Name': 'Payments',
                'Type': f'Payment_{payment.Name}_{payment.Id}',
                'Amount': payment.Amount,
                'Date': payment.Date,
                'Method': payment.Method,
                'Comment': payment.Comment,
                'Id': payment.Id
            }
        )
        print('added!')




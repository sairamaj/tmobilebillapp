import boto3
from decimal import Decimal


def floatToDecimal(val):
    return Decimal(format(val, ".15g"))


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
        self.Id = parts[5]


paymentSkip = False
with open("c:\\sai\\dev\\temp\\pdf\\tmobile\\payments1.txt", "r") as f:
    for line in f:
        line = line.strip('\n')
        if paymentSkip == False:
            payment = Payment(line)
            print(f'adding :{payment.Name}:{payment.Id}')
            table.put_item(
                Item={
                    'Name': 'Payments',
                    'Type': f'Payment_{payment.Name}',
                    'Amount': payment.Amount,
                    'Date': payment.Date,
                    'Method': payment.Method,
                    'Comment': payment.Comment,
                    'Id': payment.Id
                }
            )
            print('added!')
            paymentSkip = True
        else:
            print('adding for months!')
            number,month = line.split('|')
            print(f'adding :{number}:{month}')
            table.put_item(
                Item={
                    'Name': 'Payments',
                    'Type': f'{month}_Payments',
                    'Number': number,
                    'Id': payment.Id
                }
            )
    

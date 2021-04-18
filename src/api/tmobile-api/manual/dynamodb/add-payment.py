import boto3
import sys
import uuid
from decimal import Decimal

# Get the service resource.
dynamodb = boto3.resource(
    'dynamodb',
    endpoint_url='http://127.0.0.1:8000'
)
dynamodb = boto3.resource(
     'dynamodb'
)

table = dynamodb.Table('TMobile')


class MonthlyPayment:
    def __init__(self, table, parts, id):
        self.Table = table
        self.Number = parts[0]
        self.YearMonth = parts[1]
        self.Id = id

    def add(self):
        table.put_item(
            Item={
                'Name': 'Payments',
                'Type': f'{self.YearMonth}_{self.Number}',
                'Number': self.Number,
                'Id': self.Id
            }
        )

    def display(self):
        print(f'{self.Number}|{self.YearMonth}|{self.Id}')


class Payment:
    def __init__(self, table, parts):
        self.Table = table
        self.Name = parts[0]
        self.Amount = parts[1]
        self.Date = parts[2]
        self.Method = parts[3]
        self.Comment = parts[4]
        self.Id = str(uuid.uuid1())

    def add(self):
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

    def display(self):
        print(f'{self.Name}|{self.Date}|{self.Amount}|{self.Comment}|{self.Id}')


class Factory:
    def __init__(self, table):
        self.Table = table

    def get_payment(self, line):
        parts = line.split('|')
        if parts[0] == 'Payment':
            self.LastPayment = Payment(self.Table, parts[1:])
            return self.LastPayment
        if parts[0] == 'Apply':
            if self.LastPayment == None:
                raise "PAYMENT record should have exists before APPLY"
            return MonthlyPayment(self.Table, parts[1:], self.LastPayment.Id)
        return None


paymentFile = sys.argv[1]
factory = Factory(table)
with open(paymentFile, "r") as f:
    for line in f:
        line = line.strip('\n')
        payment = factory.get_payment(line)
        if payment != None:
            payment.display()
            payment.add()

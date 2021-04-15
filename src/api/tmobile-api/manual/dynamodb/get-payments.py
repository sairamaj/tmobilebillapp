import json
import os
import boto3
from boto3.dynamodb.conditions import Key

def execute_query(pk, sk=None):
    table_name = os.environ.get('TABLE_NAME', 'TMobile')
    aws_environment_local = os.getenv('AWS_SAM_LOCAL')

    if aws_environment_local:
        print('local dynamodb')
        dynamodb = boto3.resource(
            'dynamodb',
            endpoint_url='http://127.0.0.1:8000'
        )
        table = dynamodb.Table('TMobile')
    else:
        print('aws dynamodb')
        dynamodb = boto3.resource(
            'dynamodb'
        )
        table = dynamodb.Table('TMobile')

    if sk == None:
        response = table.query(
            KeyConditionExpression=Key('Name').eq(pk)
        )
    else:
        response = table.query(
            KeyConditionExpression=Key('Name').eq(
                pk) & Key('Type').begins_with(sk)
        )

    return response["Items"]

payments = execute_query('Payments','Payment')
print(payments)
print('===================================')
payments = execute_query('Payments','Jan2020')
print(payments)
print('+++++++++++++++++++++')
payments = execute_query('Payments','Feb2020')
print(payments)

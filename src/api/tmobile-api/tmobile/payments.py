import json
import os
import boto3
from boto3.dynamodb.conditions import Key

def execute_query(pk, sk=None):
    table_name = os.environ.get('TABLE_NAME', 'TMobile')
    aws_environment_local = os.getenv('AWS_SAM_LOCAL')

    if aws_environment_local:
        dynamodb = boto3.resource(
            'dynamodb',
            endpoint_url='http://dynamodb-local:8000'
        )
        table = dynamodb.Table('TMobile')
    else:
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

def lambda_payments_handler(event, context):

    response = execute_query('Payments','Payment')

    if len(response) > 0:
        payments = response
    else:
        payments = []

    return {
        "statusCode": 200,
        'headers': {
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,GET'
        },
        "body": json.dumps(payments)
    }

def lambda_payments_by_yearMonth_handler(event, context):

    yearMonth = event['pathParameters']['yearMonth']
    response = execute_query('Payments', yearMonth)

    if len(response) > 0:
        payments = response
    else:
        payments = []

    return {
        "statusCode": 200,
        'headers': {
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,GET'
        },
        "body": json.dumps(payments)
    }

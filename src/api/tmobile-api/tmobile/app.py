import json
import os
import boto3
from boto3.dynamodb.conditions import Key


def lambda_users_handler(event, context):

    table_name = os.environ.get('TABLE_NAME', 'Test')
    aws_environment = os.getenv('AWS_SAM_LOCAL')

    user = 'non-local'
    print(f'aws_environment:{aws_environment}')
    if aws_environment:
        dynamodb = boto3.resource(
            'dynamodb',
            endpoint_url='http://dynamodb-local:8000'
        )
        table = dynamodb.Table('TMobile')

    response = table.query(
        KeyConditionExpression=Key('Name').eq('Users')
    )


    if len(response["Items"]) > 0:
        users = response["Items"][0]["Value"]
    else:
        users = []

    return {
        "statusCode": 200,
        "body": users
    }

def lambda_bills_handler(event, context):

    table_name = os.environ.get('TABLE_NAME', 'Test')
    aws_environment = os.getenv('AWS_SAM_LOCAL')

    user = 'non-local'
    print(f'aws_environment:{aws_environment}')
    if aws_environment:
        dynamodb = boto3.resource(
            'dynamodb',
            endpoint_url='http://dynamodb-local:8000'
        )
        table = dynamodb.Table('TMobile')

    response = table.query(
        KeyConditionExpression=Key('Name').eq('Bills') & Key('Type').begins_with('Summary')
    )


    if len(response["Items"]) > 0:
        bills = response["Items"]
    else:
        bills = []

    return {
        "statusCode": 200,
        "body": bills
    }

def lambda_bill_details_handler(event, context):

    table_name = os.environ.get('TABLE_NAME', 'Test')
    aws_environment = os.getenv('AWS_SAM_LOCAL')

    yearMonth = event['pathParameters']['yearMonth']

    user = 'non-local'
    print(f'aws_environment:{aws_environment}')
    if aws_environment:
        dynamodb = boto3.resource(
            'dynamodb',
            endpoint_url='http://dynamodb-local:8000'
        )
        table = dynamodb.Table('TMobile')

    response = table.query(
        KeyConditionExpression=Key('Name').eq('Bills') & Key('Type').begins_with(f'Details_{yearMonth}')
    )


    if len(response["Items"]) > 0:
        bills = response["Items"]
    else:
        bills = []

    return {
        "statusCode": 200,
        "body": bills
    }

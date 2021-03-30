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


def lambda_users_handler(event, context):

    response = execute_query('Users')
    if len(response) > 0:
        users = response[0]["Value"]
    else:
        users = []

    return {
        "statusCode": 200,
        'headers': {
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,GET'
        },
        "body": users
    }


def lambda_bills_handler(event, context):

    response = execute_query('Bills', 'Summary')

    if len(response) > 0:
        bills = response
    else:
        bills = []

    return {
        "statusCode": 200,
        'headers': {
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,GET'
        },
        "body": json.dumps(bills)
    }


def lambda_bill_details_handler(event, context):

    yearMonth = event['pathParameters']['yearMonth']
    response = execute_query('Bills', f'Details_{yearMonth}')

    if len(response) > 0:
        bill_details = response
    else:
        bill_details = []

    return {
        "statusCode": 200,
        'headers': {
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,GET'
        },
        "body": json.dumps(bill_details)
    }


def lambda_bill_get_download_url(event, context):

    yearMonth = event['pathParameters']['yearMonth']

    s3_client = boto3.client('s3')

    BUCKET = 'sairama-t-mobile'
    OBJECT = f'SummaryBill{yearMonth}.pdf'

    url = s3_client.generate_presigned_url(
        'get_object',
        Params={'Bucket': BUCKET, 'Key': OBJECT},
        ExpiresIn=3600)

    return {
        "statusCode": 200,
        'headers': {
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,GET'
        },
        "body": json.dumps({"url": url})
    }

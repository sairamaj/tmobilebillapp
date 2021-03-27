import json
import os
import boto3
from boto3.dynamodb.conditions import Key


def lambda_handler(event, context):

    # try:
    #     ip = requests.get("http://checkip.amazonaws.com/")
    # except requests.RequestException as e:
    #     # Send some context about this error to Lambda Logs
    #     print(e)

    #     raise e

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

    return {
        "statusCode": 200,
        "body":response["Items"][0]["Value"]
    }

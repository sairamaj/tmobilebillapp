import json
import os
import boto3
# import requests


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
        user = 'local'
        activities_table = boto3.resource(
            'dynamodb',
            endpoint_url='http://192.168.99.100:8000'
        )

    return {
        "statusCode": 200,
        "body": json.dumps(
            [
                {
                    "primary": table_name,
                    "users": [
                        {
                            "name": aws_environment,
                            "phone": "503 111 1111"
                        },
                        {
                            "name": "user2",
                            "phone": "503 222 2222"
                        }

                    ]
                }
            ]
        ),
    }

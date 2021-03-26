import json
import os

# import requests


def lambda_handler(event, context):

    # try:
    #     ip = requests.get("http://checkip.amazonaws.com/")
    # except requests.RequestException as e:
    #     # Send some context about this error to Lambda Logs
    #     print(e)

    #     raise e

    table_name = os.environ.get('TABLE_NAME', 'Test')
    return {
        "statusCode": 200,
        "body": json.dumps(
            [
                {
                    "primary": table_name,
                    "users": [
                        {
                            "name": "user1",
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

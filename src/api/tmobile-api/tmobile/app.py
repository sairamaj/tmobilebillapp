import json

# import requests


def lambda_handler(event, context):

    # try:
    #     ip = requests.get("http://checkip.amazonaws.com/")
    # except requests.RequestException as e:
    #     # Send some context about this error to Lambda Logs
    #     print(e)

    #     raise e

    return {
        "statusCode": 200,
        "body": json.dumps(
            [
                {
                    "primary": "contact_1",
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

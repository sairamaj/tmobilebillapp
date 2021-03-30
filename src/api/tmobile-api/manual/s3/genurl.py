import boto3
import json

s3_client = boto3.client('s3')

BUCKET = 'sairama-t-mobile'
OBJECT = 'SummaryBillApr2020.pdf'

# url = s3_client.generate_presigned_url(
#     'get_object',
#     Params={'Bucket': BUCKET, 'Key': OBJECT},
#     ExpiresIn=3600)

url = "this is url"
print(json.dumps({"url": url}))
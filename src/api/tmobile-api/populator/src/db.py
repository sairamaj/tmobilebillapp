import boto3
import os
from decimal import Decimal

numberOfLines = 12

def floatToDecimal(val):
    return Decimal(format(val, ".15g"))

def upload(bill_data):

    #dynamodb = boto3.resource(
    #     'dynamodb',
    #     endpoint_url='http://localhost:8000'
    # )
    dynamodb = boto3.resource(
       'dynamodb'
    )

    print("Uploading to DynamoDB...")
    print(bill_data)
    #print(f"Month: {month}, Final Bill: {finalBill}, Per Line: {perline}, Entries: {entries}")
    
    # table = dynamodb.Table('TMobile')
    # print(f'bill month:{month}')
    # print(f'perline: {perline} : {type(perline)}')
    # print(f'finalBill: {finalBill} : {type(finalBill)}')
    # table.put_item(
    #     Item={
    #         'Name': 'Bills',
    #         'Type': f'Summary_{month}',
    #         'Total': "{:.2f}".format(floatToDecimal(finalBill)),
    #         "PerLine":  "{:.2f}".format(floatToDecimal(perLine)),
    #     }
    # )

    # # add all entries
    # for entry in entries:
    #     table.put_item(
    #         Item={
    #             'Name': 'Bills',
    #             'Type': f'Details_{month}_{entry.number}',
    #             'Number': entry.number,
    #             "PlanAmount" : "{:.2f}".format(floatToDecimal(entry.amount)),
    #             "Equipment": "{:.2f}".format(floatToDecimal(entry.equipment)),
    #             "Services": "{:.2f}".format(floatToDecimal(entry.services)),
    #             "OneTimeCharge" : "{:.2f}".format(floatToDecimal(entry.onetime_charge)),
    #             "Total" : "{:.2f}".format(floatToDecimal(entry.total))
    #         }
    #     )

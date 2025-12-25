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

    # extract variables from bill_data
    summary = bill_data.get('bill_summary', {}) if isinstance(bill_data, dict) else {}
    month = summary.get('month')
    finalBill = float(summary.get('total_amount')) if summary.get('total_amount') is not None else 0.0
    perline = float(summary.get('per_line_plan_amount')) if summary.get('per_line_plan_amount') is not None else 0.0
    perLine = perline  # preserve variable name used elsewhere in the file

    print(f"Month: {month}, Final Bill: {finalBill}, Per Line: {perline}")
    
    table = dynamodb.Table('TMobile')
    print(f'bill month:{month}')
    print(f'perline: {perline} : {type(perline)}')
    print(f'finalBill: {finalBill} : {type(finalBill)}')
    table.put_item(
        Item={
            'Name': 'Bills',
            'Type': f'Summary_{month}',
            'Total': "{:.2f}".format(floatToDecimal(finalBill)),
            "PerLine":  "{:.2f}".format(floatToDecimal(perLine)),
        }
    )

    line_items = bill_data.get('line_items', {}) if isinstance(bill_data, dict) else {}

    for number, info in line_items.items():
        name = info.get('name')
        plan = float(info.get('plan', 0.0))
        equipment = float(info.get('equipment', 0.0))
        services = float(info.get('services', 0.0))
        total = float(info.get('total', 0.0))
        onetime_charge = float(info.get('one_time_charge', 0.0))
        print(f"Number: {number}, Name: {name}, Plan: {plan:.2f}, Equipment: {equipment:.2f}, Services: {services:.2f}, Total: {total:.2f}")
    # add all entries
        table.put_item(
            Item={
                'Name': 'Bills',
                'Type': f'Details_{month}_{number}',
                'Number': number,
                "PlanAmount" : "{:.2f}".format(floatToDecimal(plan)),
                "Equipment": "{:.2f}".format(floatToDecimal(equipment)),
                "Services": "{:.2f}".format(floatToDecimal(services)),
                "OneTimeCharge" : "{:.2f}".format(floatToDecimal(onetime_charge)),
                "Total" : "{:.2f}".format(floatToDecimal(total))
            }
        )

import boto3
from botocore.exceptions import ClientError

def lambda_handler(*_):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('BTC_PRICE_SAMPLE')
    try:
        response = table.scan()
        data = response['Items']
    except ClientError as e:
        print(e)
    else:
        return data

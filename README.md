# btc-sample-lambda

For this project there were two lambda functions.

## btc_data_extraction

In the handler function the it is requested and extracted the data from the CoinMarketCap API.

```python
def lambda_handler(*_):
    api_handler = ApiHandler()
    btc_data = api_handler.request_data()
    item = json.loads(json.dumps(btc_data), parse_float=Decimal)
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('BTC_PRICE_SAMPLE')
    response = table.put_item( 
       Item=item
    ) 
    return response
```

Then it is uploaded to the corresponding DynamoDB table using the AWS SDK.

## get_btc_stored_data

Using the AWS SDK to retrieve all entries stored in the corresponding DynamoDB table.

```python
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
```
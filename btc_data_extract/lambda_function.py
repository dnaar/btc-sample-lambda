import os
from requests import get
from datetime import datetime
import boto3
import json
from decimal import Decimal
from uuid import uuid4

def extract_data(data: dict):
        timestamp = datetime.fromisoformat(data['status']['timestamp']).timestamp() * 1000 or datetime.timestamp(datetime.now())
        data_array = data['data']
        for element in data_array:
            if element['id'] == 1:
                return element['quote']['USD'], timestamp
    
def format_btc_data(data_element: dict, ts: str):
    return {
        'timestamp':ts,
        'price':data_element['price'],
        'volume_24h':data_element['volume_24h'],
        'volume_change_24h':data_element['volume_change_24h'],
        'percent_change_1h':data_element['percent_change_1h'],
        'percent_change_24h':data_element['percent_change_24h'],
        'percent_change_7d':data_element['percent_change_7d'],
        'percent_change_30d':data_element['percent_change_30d'],
        'percent_change_60d':data_element['percent_change_60d'],
        'percent_change_90d':data_element['percent_change_90d'],
        'market_cap':data_element['market_cap'],
        'market_cap_dominance':data_element['market_cap_dominance'],
        'fully_diluted_market_cap':data_element['fully_diluted_market_cap'],
    }


class ApiHandler():
    def __init__(self):
        self.API_URL = os.environ['CMC_API_URL']
        self.API_KEY = os.environ['CMC_API_KEY']
        self.HEADERS = {
            'X-CMC_PRO_API_KEY':self.API_KEY
        }
    def request_data(self):
        while True:
            try:
                response = get(url=self.API_URL, headers=self.HEADERS)
                response.raise_for_status()
                btc_raw_data, timestamp = extract_data(response.json())
                btc_data = format_btc_data(btc_raw_data, timestamp)
                return btc_data
            except Exception:
                continue

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
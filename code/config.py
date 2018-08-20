'''
Contains the important variables needed across multiple python files


'''


import boto3

dynamodb = boto3.resource('dynamodb', endpoint_url = 'http://localhost:8000/')
dynamodb_client = boto3.client('dynamodb', endpoint_url = "http://localhost:8000")


possible_app_stores = ['Apple', 'Google', 'Tencent']

app_store_to_csv_dict = {
'Apple': '../apple_apps.csv',
'Google': '../google_apps.csv',
'Tencent': '../tencent_apps.csv'
}


store_keywords_dict =  {
'Google': ('title', 'market_url', 'website', 'package_name'),
'Apple': ('artistName', 'artistViewUrl', 'sellerUrl', 'bundleId')
}


MAX_BATCH_SIZE = 50
LINES_PER_LAMBDA = 150
NUMBER_ATTEMPTS = 5


"""
Contains the important variables needed across multiple python files
"""

import os



DATA_S3_BUCKET_NAME = 'external.42matters.com'
DATA_S3_PREFIX_APPLE = '1/42apps/v0.1/production/itunes/lookup-weekly/20'
DATA_S3_PREFIX_GOOGLE = '1/42apps/v0.1/production/playstore/lookup-weekly/20'

#draws from aws lambda environment variables
DATA_ACCESS_KEY = os.environ['data_access_key']
DATA_SECRET_ACCESS_KEY = os.environ['data_secret_access_key']
S3_BUCKET_NAME = os.environ['s3_bucket_name']
S3_REGION = os.environ['region']


possible_app_stores = ['Apple', 'Google', 'Tencent']


store_keywords_dict =  {
'Google': ('title', 'market_url', 'website', 'package_name'),
'Apple': ('artistName', 'artistViewUrl', 'sellerUrl', 'bundleId'),
'Tencent': ('title', 'market_url', '', 'package_name')
}

TABLE_READ_CAPACITY = 1000
TABLE_WRITE_CAPACITY = 1000
MAX_BATCH_SIZE = 50
LINES_PER_LAMBDA = 100 #raising this number should be done with caution, can lead to Lambda function timeout
NUMBER_ATTEMPTS = 3
MAX_LENGTH_KEY = 300
MAXIMUM_ADS_FILE_SIZE = 1024 * 100 #arbitrary max size to amount of bytes we will stream from webpage
BREAK_UP_TIME_LIMIT = 290 #4 minutes 50 seconds
STREAM_SIZE = 1024


#Dynamodb table names
APPLE_STORE_TABLE_NAME = 'AppStoreAdsTxt_IOS'
GOOGLE_PLAY_TABLE_NAME = 'AppStoreAdsTxt_GooglePlay'
APPLE_TEXT_FILE_KEY = 'AppStoreAdsTxt_IOS.txt'
GOOGLE_TEXT_FILE_KEY = 'AppStoreAdsTxt_GooglePlay.txt'

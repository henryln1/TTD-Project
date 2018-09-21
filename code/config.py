"""
Contains the important variables needed across multiple python files
"""

import os



DATA_S3_BUCKET_NAME = 'external.42matters.com'

#draws from aws lambda environment variables
DATA_ACCESS_KEY = os.environ['data_access_key']
DATA_SECRET_ACCESS_KEY = os.environ['data_secret_access_key']
S3_BUCKET_NAME = os.environ['s3_bucket_name']
S3_REGION = os.environ['region']

all_stores = {
	'Apple': {
		'identifyingString': 'itunes.apple.com',
		'tableName': 'AppStoreAdsTxt_IOS',
		'storageBucketKeyName':'AppStoreAdsTxt_IOS.txt',
		'S3_prefix': '1/42apps/v0.1/production/itunes/lookup-weekly/20', #prefix in 42matters bucket
		'keywords': ('artistName', 'artistViewUrl', 'sellerUrl', 'trackId')
	},
	'Google': {
		'identifyingString': 'play.google.com/store',
		'tableName': 'AppStoreAdsTxt_GooglePlay',
		'storageBucketKeyName': 'AppStoreAdsTxt_GooglePlay.txt',
		'S3_prefix': '1/42apps/v0.1/production/playstore/lookup-weekly/20', #prefix in 42matters bucket
		'keywords': ('title', 'market_url', 'website', 'package_name')
	},
	'Tencent': {
		'identifyingString': 'tencent',
		'tableName': 'AppStoreAdsTxt_Tencent',
		'storageBucketKeyName': 'AppStoreAdsTxt_Tencent.txt',
		'S3_prefix': '1/42apps/v0.1/production/tencent/lookup-weekly/20', #prefix in 42matters bucket
		'keywords': ('title', 'market_url', '', 'package_name')
	},
}

TABLE_READ_CAPACITY = 1000
TABLE_WRITE_CAPACITY = 1000
MAX_BATCH_SIZE = 50
LINES_PER_LAMBDA = 100 #raising this number should be done with caution, can lead to Lambda function timeout
NUMBER_ATTEMPTS = 2
MAX_LENGTH_KEY = 300
MAXIMUM_ADS_FILE_SIZE = 1024 * 200 #arbitrary max size to amount of bytes we will stream from webpage
BREAK_UP_TIME_LIMIT = 290 #4 minutes 50 seconds
STREAM_SIZE = 1024 * 5


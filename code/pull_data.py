import requests
from config import s3, S3_BUCKET_NAME



# def log_into_website(url, username, password):

# 	login_data = {
# 		'userName': username,
# 		'password': password
# 	}
# 	session = requests.Session()

# 	r = session.post(url, data = login_data)
# 	print(r.content)

def test_location_download(url):
	request = requests.get(url, timeout = 5)
	return request.content

def push_to_s3(bucket_name, data):
	bucket = s3.Bucket(Bucket = S3_BUCKET_NAME)
	exists = True
	try:
		s3.meta.client.head_bucket(Bucket = S3_BUCKET_NAME)
	except botocore.exceptions.ClientError as e:
		error_code = int(e.response['Error']['Code'])
		if error_code == 404:
			exists = False
	if not exists:
		print("Unable to access S3 bucket to store data. Exiting.")
		exit()
	



def download_data(location):
	'''
	should pull data from wherever it's located, then returns a 
	way to find that file
	'''
	print("Downloading data....")
	# download data into S3 bucket
	print("Data downloaded!")
	return

# def main(args):

# 	website = args[1]
# 	username = args[2]
# 	password = args[3]
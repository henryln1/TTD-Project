import requests




# def log_into_website(url, username, password):

# 	login_data = {
# 		'userName': username,
# 		'password': password
# 	}
# 	session = requests.Session()

# 	r = session.post(url, data = login_data)
# 	print(r.content)

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
import requests




def log_into_website(url, username, password):

	login_data = {
		'userName': username,
		'password': password
	}
	session = requests.Session()

	r = session.post(url, data = login_data)
	print(r.content)




def main(args):

	website = args[1]
	username = args[2]
	password = args[3]
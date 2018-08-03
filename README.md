# TTD-Project
Summer project at theTradeDesk. The goal is to generate a csv file that has a match between mobile app ids and a corresponding ads.txt location on the web.


The data will be stored in AWS and the code is being written in Python 3.7.0.


The necessary Python libraries aside from the standard are listed in relevant_python_libraries.txt. Please install these before running.


Overview of files in code/


config.py: A file to include globally used variables and or possibly also libraries


check_url.py: Contains functions that validate a url (checking whether or not it has an ads.txt file located there)


merge_results.py: Takes the changes found and merges them into the csv file, will create a new file if not csv file exists


parse_ads_txt_location.py: Functions to extract urls/locations to check for an ads.txt file - DEPRECATED


google_playstore_extraction.py: Functions to extract urls/locations for data from google playstore specifically - DEPRECATED


apple_store_extraction.py: Functions to extract urls/locations for data from apple store specifically - DEPRECATED


extractor.py: Extractor class that processes data file for information


query_dynamo.py: Functions to query ads.txt location from Dynamo DB 


write_to_dynamo.py: Functions to interact with local Dynamo DB using boto3.


dynamo_tests.py: Contains a few tests to make sure we are writing into the DynamoDB correctly and able to query


pull_data.py: Will write code to automatically log into 42matters and pull data to process.


tests.py: Functions to test everything above.


periodic_test.py: Using celery, attempts to automate the tests (precursor to automating everything in DynamoDB)


utils.py: misc file that contains generally useful functions 


main.py: Utilizes above functions to process a data file into csv form. 





TODO 08/03/18:


Consider how to scale this to full data file once it arrives. AWS Lambda has a limit of 5 minutes so the faster the code, the better it will be. Otherwise, look into chaining lambda functions together.


Look into zipping all the code into a file that we can push onto AWS Lambda for scheduled tasks.


Figure out how to log into 42matters from script and download data via automation.






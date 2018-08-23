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


utils.py: misc file that contains generally useful functions 


main.py: Utilizes above functions to process a data file into csv form. 


direct_write.py: Newer logic that uses dynamo batch write function to process a chunk of the data at a time and write it directly to dynamo, skipping the csv file. 


lambda_function.py: Contains handler functions when we upload code as a package up to AWS Lambda



TODO 08/20/18:


Consider how to scale this to full data file once it arrives. AWS Lambda has a limit of 5 minutes so the faster the code, the better it will be. Currently we are at about 0.9 seconds per data entry, and we will most likely break the data file into multiple smaller files that each trigger a lambda call.


Look into zipping all the code into a file that we can push onto AWS Lambda for scheduled tasks.


Figure out how to log into 42matters from script and download data via automation.


Always looking to clean up code and where to optimize


Get code to start being reviewed


Other Notes:


Use Cloudwatch on AWS Lambda to make a trigger for a regularly scheduled lambda task


Create an S3 trigger that calls lambda function whenever a file we want is created





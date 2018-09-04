# TTD-Project
Summer project at theTradeDesk. The goal is to generate a csv file that has a match between mobile app ids and a corresponding ads.txt location on the web.


The data will be stored in AWS and the code is being written in Python 3.7.0.


The necessary Python libraries aside from the standard are listed in relevant_python_libraries.txt. Please install these before running.


Overview of files in code/


check_url.py: Contains functions that validate a url (checking whether or not it has an ads.txt file located there)


direct_write.py: Processes data into Dynamo Table


divide_data.py: Splits a large data file into smaller files


extractor.py: Extractor class that processes data file for information


lambda_function.py: Contains handler functions when we upload code as a package up to AWS Lambda


pull_data.py: Downloads data into s3 bucket


query_dynamo.py: Functions to query ads.txt location from Dynamo DB 


unit_tests.py: Testing bits and pieces of code


utils.py: misc file that contains generally useful functions 


write_to_dynamo.py: Functions to interact with local Dynamo DB using boto3.




TODO 09/04/18:


Write lambda with cloudwatch trigger to regularly download file into s3 bucket


Code Review
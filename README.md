# TTD-Project
Summer project at theTradeDesk. The goal is to generate a csv file that has a match between mobile app ids and a corresponding ads.txt location on the web.


The data will be stored in AWS and the code is being written in Python 3.7.0.


The necessary Python libraries aside from the standard are listed in relevant_python_libraries.txt. Please install these before running.


Overview of files in code/


check_url.py: Contains functions that validate a url (checking whether or not it has an ads.txt file located there)


merge_results.py: Takes the changes found and merges them into the csv file, will create a new file if not csv file exists


parse_ads_txt_location.py: Functions to extract urls/locations to check for an ads.txt file


tests.py: Functions to test everything above.


periodic_test.py: Using celery, attempts to automate the tests (precursor to automating everything in DynamoDB)


utils.py: misc file that contains generally useful functions 


main.py: Utilizes above functions to process a data file into csv form. 





TODO 07/18/18:


Write regexes to extract information from data files.


Figure out how to automate process so that it runs periodically (whenever new data comes in)


How will it interact with DynamoDB?



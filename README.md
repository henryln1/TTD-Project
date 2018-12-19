# TTD-Project
Summer project at theTradeDesk. The goal is to generate a txt file that has a match between mobile app ids and a corresponding ads.txt location on the web. 


The data is stored in AWS and the code is being written in Python 3.7.0.


Note about Expected Scale:


With the current amount of data being processed, each weekly file is about 2-4GB compressed and 8-11GB uncompressed. The number of individual lines being processed ranges from 2 to 3.5 million for each file. To process this large amount of data using lambda, each weekly file is broken down into 100 line chunks that are processed individually. This leads to between 20k and 35k lambda invocations.


Lambda setup instructions
-------------------------

This code runs under three seperate lambda functions.

`file_split_lambda_handler`, runs once weekly and reads in the compressed file of 42matters data, splits it into 100 line files and uploads each one to the folder `adstxt` in a S3 bucket.

`process_into_dynamo_lambda_handler`, is triggered by file creation in the `adstxt` folder and reads in the 100 line file, builds the app-ads.txt url, checks if it exists and if so, writes out to dynamodb.

`text_file_write_lambda_handler`, also runs once weekly, a day or so after the first one and takes all the entries in dynamodb and writes them out to a text file.

Both the first and the third need seperate triggers weekly triggers for each app store.


All three lambdas need four enviorment variables defined.

`data_access_key` is the access key for the 42matters bucket

`data_secret_access_key` is the secret for the 42matters bucket

`region` is the region of the 42matters bucket

`s3_bucket_name` is the name of the bucket to store the 100 line files in and to export the final text file to


Python setup instructions
-------------------------


Make sure you have Python 3 installed


> py


should run python 3.7. if it doesn't, install python 3.7 from https://www.python.org/downloads/


cd into the project directory and make a virtual environment:


	> cd D:\src\henry-ttd-project\
	> py -m venv venv


Then activate that virtual environment:


    > . .\venv\Scripts\activate


"." works in bash and powershell. In plain command prompt, just execute the activate command directly:


	d:\src\henry-ttd-project> venv\Scripts\activate


Your prompt should now tell you that you are in the `(venv)` environment:


    (venv) D:\src\henry-ttd-project >


Make sure you have the latest version of `pip` (Pythons package manager) installed:


	(venv) D:\src\henry-ttd-project > python -m pip install --upgrade pip


Once the virtual environment is active, install all the required packages:


 	(venv) D:\src\henry-ttd-project > pip install -r .\requirements.txt
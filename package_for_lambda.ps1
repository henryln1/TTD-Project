# Packages up code along with relevant libraries to be uploaded to Amazon Lambda
# Works for Windows powershell


#removes pre-existing copies

mkdir package-project-dir
cp code/check_url.py package-project-dir
cp code/config.py package-project-dir
cp code/direct_write.py package-project-dir
cp code/divide_data.py package-project-dir
cp code/extractor.py package-project-dir
cp code/lambda_function.py package-project-dir
cp code/pull_data.py package-project-dir
cp code/lambda_function.py package-project-dir
cp code/query_dynamo.py package-project-dir
cp code/utils.py package-project-dir
cp code/write_to_dynamo.py package-project-dir

# copy modules into package
cp -r C:/Users/v-henry.lin/AppData/Local/Programs/Python/Python37/lib/site-packages/requests* package-project-dir
cp -r C:/Users/v-henry.lin/AppData/Local/Programs/Python/Python37/lib/site-packages/urllib3* package-project-dir
cp -r C:/Users/v-henry.lin/AppData/Local/Programs/Python/Python37/lib/site-packages/chardet* package-project-dir
cp -r C:/Users/v-henry.lin/AppData/Local/Programs/Python/Python37/lib/site-packages/certifi* package-project-dir
cp -r C:/Users/v-henry.lin/AppData/Local/Programs/Python/Python37/lib/site-packages/idna* package-project-dir
cp -r C:/Users/v-henry.lin/AppData/Local/Programs/Python/Python37/lib/site-packages/six* package-project-dir
cp -r C:/Users/v-henry.lin/AppData/Local/Programs/Python/Python37/lib/site-packages/python-dateutil* package-project-dir
cp -r C:/Users/v-henry.lin/AppData/Local/Programs/Python/Python37/lib/site-packages/jmespath* package-project-dir
cp -r C:/Users/v-henry.lin/AppData/Local/Programs/Python/Python37/lib/site-packages/docutils* package-project-dir
cp -r C:/Users/v-henry.lin/AppData/Local/Programs/Python/Python37/lib/site-packages/s3transfer* package-project-dir
cp -r C:/Users/v-henry.lin/AppData/Local/Programs/Python/Python37/lib/site-packages/pytz* package-project-dir

#removing unused packages
#rm -r package-project-dir/wheel*
#rm -r package-project-dir/easy-install*
#rm -r package-project-dir/setuptools*
#rm -r package-project-dir/celery*
#rm -r package-project-dir/*jango*

# module_location='C:\Users\v-henry.lin\AppData\Local\Programs\Python\Python37\lib\site-packages'

#add permissions to all the files
#./add_permission.sh


#zip -r project-lambda-package package-project-dir
Compress-Archive -Force -Path package-project-dir/* -CompressionLevel Optimal -DestinationPath project-lambda-package.zip

rm -r package-project-dir

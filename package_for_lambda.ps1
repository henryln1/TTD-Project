# Packages up code along with relevant libraries to be uploaded to Amazon Lambda
# Works for Windows powershell


#removes pre-existing copies
rm -r package-project-dir
rm project-lambda-package.zip


mkdir package-project-dir
rm -r code/*pycache*
cp code/* package-project-dir

# copy modules into package
cp C:/Users/v-henry.lin/AppData/Local/Programs/Python/Python37/lib/site-packages/* package-project-dir


#removing unused packages
rm -r package-project-dir/wheel*
rm -r package-project-dir/easy-install*
rm -r package-project-dir/setuptools*
rm -r package-project-dir/celery*
rm -r package-project-dir/*jango*

# module_location='C:\Users\v-henry.lin\AppData\Local\Programs\Python\Python37\lib\site-packages'

#add permissions to all the files
#./add_permission.sh


#zip -r project-lambda-package package-project-dir
Compress-Archive -Path package-project-dir/* -CompressionLevel Optimal -DestinationPath project-lambda-package.zip

#rm -r package-project-dir
#sleep 100

# TTD-Project
Summer project at theTradeDesk. The goal is to generate a txt file that has a match between mobile app ids and a corresponding ads.txt location on the web.


The data will be stored in AWS and the code is being written in Python 3.7.0.


TODO 09/17/18:


Add changes from CR

Python setup instructions
-------------------------

[To be included in Readme]


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
# Object Counter

The objective of this repository is to utilize FastAPI to retrieve a list of objects count data stored in a database after counting the number of objects in an image.

Note: In this script, object counting is performed using a predefined algorithm. If you wish to make predictions using a model, please refer to this repository and make the necessary modifications according to your requirements.
[arenan02/object-counter](https://github.com/arenan02/object-counter)


## Setup virtual environment

1. Create a virtual environment and install requirements.txt file

Example:

```
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```
Note: I used python 3.7.0



## Setup Mysql

1.Please refer to the following link for a reference on how to install and run mySQL.

[Example] https://www.learnpythonwithrune.org/how-to-setup-a-mysql-server-in-docker-for-your-python-project/
Please refer to the link and modify the schema.sql file based on your requirements.

2. Additionally, you can refer to the "db_connect" folder in the repository for database design and docker setup.

3. To finalize, host the SQL server and update the details in counter/config.py file.


## Run the application

### Using fast api
```
cd counter\entrypoints\

python webapp.py

or 
use  uvicorn comment 

uvicorn webapp:app --host 0.0.0.0 --port 5014
```
# Check service 

If the service has started without any errors, you can verify it by checking it in the browser. Use the following command in the browser to test it locally. If you need to change 'localhost' to an IP address, you can do so.
```
localhost:5014/swagger
```

Lastly, call the API and verify the predictions.
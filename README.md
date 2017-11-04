# Sigma: Financial Bot

Simple implementation of a financial bot in Google Cloud Platform.

## Setup

To run a local version or to contribute in the development,
follow these instructions:

1. Install the [google cloud sdk](https://cloud.google.com/sdk/docs/quickstart-linux) for python. 

2. Create configuration files.
    * `cp settings/client_secret.json.example settings/client_secret.json`
    * Change the values according to the project configuration (ask main developer).
      
3. Create a virtual environment.
    * `virtualenv -p /usr/bin/python2.7 venv`
    * `source activate venv`
    
4. Install requirements. 
    * `pip install --upgrade -t lib -r requirements.txt`
    
5. Run the local server:
    * `dev_appserver.py app.yaml`
    
You can now test the app at locahost.

## TODO

* Code data models and implement ndb for complex queries.
* Implement services.
* JSON Config data.
* Add functionality related to finance
    * Stock info
    * Stock plots
    * Recommendations

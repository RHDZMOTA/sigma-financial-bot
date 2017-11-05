# Sigma: Financial Bot

Simple implementation of a financial bot in Google Cloud Platform.

## Tech Stack 

This repo uses **python 2.7**.

The following tech and frameworks are used (among others):

* Google App Engine
* Google Cloud Storage
* Google Datastore
* Python Flask

## Setup

To run a local version or to contribute in the development,
follow these instructions:

1. Install the [google cloud sdk](https://cloud.google.com/sdk/docs/quickstart-linux) for python. 

2. Create configuration files. Ask the [main developer](https://github.com/rhdzmota) for keys.
    * `cp settings/client_secret.json.example settings/client_secret.json`
     
3. Create a virtual environment.
    * `virtualenv -p /usr/bin/python2.7 venv`
    * `source activate venv`
    
4. Install requirements. 
    * `pip install --upgrade -t lib -r requirements.txt`
    
5. Run the local server:
    * `dev_appserver.py app.yaml`
    
You can now test the app at locahost.

## Deployment

1. Exit the virtual environment.
    * `source deactivate`

2. Login. 
    * `gcloud auth login`

3. Run the following:
    * `gcloud app deploy --project sigma-financial-bot`

The app will be running at: https://sigma-financial-bot.appspot.com 

## How to contribute? 

Any desire to contribute must be discussed with the **main developer**. 

## Authors

Feel free to add yourself in this list when making your _pull request_. 

* **Rodrigo Hernández Mota**: [rhdzmota](https://github.com/rhdzmota) -- main developer.

**Contributions**
* Daniela Guerra Alcalá

## License

See `LICENSE.md` file for more details. 

## TODO

* Code data models and implement ndb for complex queries.
* Implement services.
* JSON Config data.
* Add functionality related to finance
    * Stock info
    * Stock plots
    * Recommendations
* Add tests

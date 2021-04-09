Python Port Scanner
=====================

## Table of contents
* [General info](#general-info)
* [Components](#components)
* [Technologies](#technologies)
* [Setup](#setup)

## General info
This project is a Python web application that scans a given IP/Hostname for open ports.

## Components
The Port Scanner Application is supported by the following components that serve important functions:
- **IP/Hostname Validator:** This component handles all the necessary checks to validate any input IP Address or Hostname. Throws a warning if invalid input is provided
- **Hostname to IP translation:** All Hostnames are resolved by this component. Erroneous or malicious inputs will not be accepted since every input requires a DNS lookup or IP validation, thus making it relatively secure. 
- **Scanner:** The main component of the application that handles the active scanning of ports running on a given host in a multithreaded fashion to speed up the process.
- **SQLite Database:** A backend database is used to store and retrieve information about the scans performed for every IP Address.
- **Scan History:** Every scan requires a lookup of the database to understand history of scans for the given host happened, and it also displays all the changes in states of open ports since the last scan, if any. These functions are served by the Scan History component. An added feature in this component allows for the user to check whether an IP Address (not hostname) has been previously scanned without performing any active scans. 
	
## Technologies
Project is created with:
* Python=3.9.2
* Flask=1.1.2
* SQLAlchemy=1.4.5, SQLite=3.35.3
	
## Setup
Instructions to run this project:

Install
-------

    # clone the repository (or download the zip and save it as "port-scanner-web-app.zip")
    $ git clone https://github.com/aparna-mahalingam/port-scanner-web-app.git
    # navigate to port-scanner-web-app directory
    $ cd port-scanner-web-app

Create a virtualenv and activate it:

* Using pip
```
    $ python3 -m venv venv
    $ . venv/bin/activate
```
* OR conda
```
    $ conda create --name venv
    $ conda activate venv
```
* OR on Windows cmd
```
    $ py -3 -m venv venv
    $ venv\Scripts\activate.bat
```
Install the following requirements:

* Using pip
```
    $ pip install flask
    $ pip install flask-sqlalchemy
```
* OR conda
```
    $ conda install flask
    $ conda install flask-sqlalchemy
```
Run
---

_WITH_ ENVIRONMENT VARIABLES:

* In the terminal
```
    $ export FLASK_APP=flaskscanner
    $ export FLASK_ENV=development
    $ flask run
```
* OR on Windows cmd
```
    > set FLASK_APP=flaskscanner
    > set FLASK_ENV=development
    > flask run
```
OR WITHOUT ENVIRONMENT VARIABLES::

    # still from within the port-scanner-web-app directory
    $ python run.py
    

Open http://127.0.0.1:5000 in a browser.

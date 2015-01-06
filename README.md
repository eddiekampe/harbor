# Harbor: Docker management

## About
Harbor is a tool that gives you a quick and clean overview for your Docker containers.

## Requirements
* Python 2.7
* Virtualenv
* Docker

## Usage
To setup Harbor:

1. Create new virtual environment 
```
virtualenv <env_name>; source <env_name>/bin/activate
```

2. Install requirements 
```
pip install -r requirements.txt
```
3. Run the application. 
```
python harbor.py
```

The application is now accessible on http://localhost:5000/

## Credits
Build using <a href="https://github.com/docker/docker-py">docker-py</a>.
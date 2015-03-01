# Harbor: Docker management

## About
Harbor is a tool that gives you a quick and clean overview for your Docker containers.

## Requirements
* Python 2.7
* Virtualenv
* Docker

## Usage
To setup Harbor:

**Create new virtual environment**
```bash
virtualenv <env_name>; source <env_name>/bin/activate
```
**Install requirements**
```bash
pip install -r requirements.txt
```
**Run the application**
```bash
python harbor.py
```

The application is now accessible on http://localhost:5000/

## Credits
Build using <a href="https://github.com/docker/docker-py">docker-py</a>.

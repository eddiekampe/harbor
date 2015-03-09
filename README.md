# Harbor: Docker management

## About
Harbor is a tool that gives you a quick and clean overview for your Docker containers.

## Requirements
* Docker

## Usage
To run Harbor, issue the following command:

```bash
docker run -p 5000:5000 -v /var/run/docker.sock:/var/run/docker.sock eddiekampe/harbor
```

The application is now accessible on http://<host_ip>:5000/

**Note that you can change the host port if required**

## Credits
Build using <a href="https://github.com/docker/docker-py">docker-py</a>.

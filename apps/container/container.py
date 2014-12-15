import json
from flask import Blueprint, render_template
from docker import Client

container = Blueprint("container", __name__)
docker_client = Client(base_url="unix://var/run/docker.sock")


# List containers
@container.route("/", methods=["GET"])
def list_containers():
    containers = docker_client.containers()
    return render_template("container/list.html", containers=containers)


# Show container by id
@container.route("/<container_id>", methods=["GET"])
def inspect_container(container_id):
    entry = docker_client.inspect_container(container_id)
    return render_template("container/entry.html", container=entry)
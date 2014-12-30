from flask import Blueprint, render_template, redirect, url_for, flash, request
from docker import Client

container = Blueprint("container", __name__)
docker_client = Client(base_url="unix://var/run/docker.sock")


# List containers
@container.route("/", methods=["GET"])
def list_containers():

    containers = docker_client.containers(all=True)
    images = docker_client.images()

    return render_template("container/list.html", containers=containers, images=images)


# Show container by id
@container.route("/<container_id>", methods=["GET"])
def inspect_container(container_id):
    entry = docker_client.inspect_container(container_id)
    return render_template("container/entry.html", container=entry)


# Delete container by id
@container.route("/<container_id>/delete", methods=["GET"])
def delete_container(container_id):
    feedback = docker_client.remove_container(container_id)
    print feedback
    return redirect(url_for("container.list_containers"))


# Start container by id
@container.route("/<container_id>/start", methods=["GET"])
def start_container(container_id):
    feedback = docker_client.start(container_id)
    print feedback
    return redirect(url_for("container.list_containers"))


# Create a container
@container.route("/", methods=["POST"])
def create_container():

    # TODO: Add more logic
    container_name = request.form["inputName"]
    image = request.form["image"]

    if None not in [image, container_name]:
        new_container = docker_client.create_container(image=image, name=container_name)
        print new_container

    return redirect(url_for("container.list_containers"))
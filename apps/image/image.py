from flask import Blueprint, render_template
from docker import Client

image = Blueprint("image", __name__)
docker_client = Client(base_url="unix://var/run/docker.sock")


# List images
@image.route("/", methods=["GET"])
def list_images():
    images = docker_client.images()
    return render_template("image/list.html", images=images)


# Show image by id
@image.route("/<image_id>", methods=["GET"])
def inspect_image(image_id):
    entry = docker_client.inspect_image(image_id)
    return render_template("image/entry.html", image=entry)
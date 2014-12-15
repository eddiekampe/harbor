import json
from flask import Blueprint, render_template
from docker import Client

image = Blueprint("image", __name__)
docker_client = Client(base_url="unix://var/run/docker.sock")


# List images
@image.route("/images", methods=["GET"])
def list_images():
    images = docker_client.images()
    return render_template("image/list.html", images=images)


# Show image by id
@image.route("/images/<image_id>", methods=["GET"])
def show_image(image_id):
    return 501


# Create a new image
@image.route("/images", methods=["POST"])
def create_image():
    return 501
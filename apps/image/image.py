import json
from flask import Blueprint, render_template, redirect, url_for, g, flash, request

image = Blueprint("image", __name__)

SUCCESS = "success"

# List images
@image.route("/", methods=["GET"])
def list_images():
    images = g.docker_client.images()
    return render_template("image/list.html", images=images)


# Delete image by id
@image.route("/<image_id>/delete", methods=["GET"])
def delete_image(image_id):
    feedback = g.docker_client.remove_image(image_id)
    flash(feedback, SUCCESS)
    return redirect(url_for("image.list_images"))


# Show image by id
@image.route("/<image_id>", methods=["GET"])
def inspect_image(image_id):
    entry = g.docker_client.inspect_image(image_id)
    return render_template("image/entry.html", image=entry)


# Search image
@image.route("/search", methods=["POST"])
def search_image():

    search_term = request.form["term"]
    # TODO: Validate input
    search_response = g.docker_client.search(search_term)
    return json.dumps(search_response)


# Pull image
@image.route("/pull", methods=["POST"])
def pull_image():

    image_name = request.form["image"]
    # TODO: Validate input
    image_stream = g.docker_client.pull(image_name, stream=True)
    # TODO: Stream the download, add progress bar

    return "Image download complete"
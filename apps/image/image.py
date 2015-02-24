import json
from docker.errors import APIError

from flask import Blueprint, render_template, redirect, url_for, g, flash, request, Response
from lib.notification import SUCCESS, ERROR, WARNING

image = Blueprint("image", __name__)


# List images
@image.route("/", methods=["GET"])
def list_images():
    """
    Lists user's local images
    """
    images = g.docker_client.images()
    return render_template("image/list.html", images=images)


# Delete image by id
@image.route("/<image_id>/delete", methods=["GET"])
def delete_image(image_id):
    """
    Delete image
    """
    try:
        feedback = g.docker_client.remove_image(image_id)

        if feedback is None:
            flash("Image {} was successfully deleted!".format(image_id), SUCCESS)
        else:
            flash(feedback, WARNING)

    except APIError as e:
        flash(e.explanation, ERROR)

    return redirect(url_for("image.list_images"))


# Show image by id
@image.route("/<image_id>", methods=["GET"])
def inspect_image(image_id):
    """
    View detailed information about the image
    """
    entry = g.docker_client.inspect_image(image_id)
    return render_template("image/entry.html", image=entry)


# Search image
@image.route("/search", methods=["GET"])
def search_image():
    """
    Search online images (registry.hub.docker.com)
    """
    search_term = request.args["term"]
    search_response = g.docker_client.search(search_term)
    return json.dumps(search_response)


# Pull image
@image.route("/pull", methods=["GET"])
def pull_image():
    """
    Method used to download an image and stream the process to the user

    @TODO
        Might consider converting this into a background job, so that the user won't
        have to stay on the same page during the download.
    """

    image_name = request.args["image"]
    print image_name

    def download_stream():

        # TODO: See if we can reuse other client
        from docker import Client
        docker_client = Client(base_url="unix://var/run/docker.sock")

        # Consume download stream
        for data in docker_client.pull(image_name, stream=True):
            yield "data: {}\n\n".format(json.dumps(data))

        # Send a STOP message
        yield "data: {}\n\n".format(json.dumps({"status": "COMPLETE"}))

    # Stream data to client
    return Response(download_stream(), mimetype="text/event-stream")
import json
from flask import Blueprint, render_template, redirect, url_for, g, flash, request, Response

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
@image.route("/pull", methods=["GET"])
def pull_image():

    # TODO: Validate input
    image_name = request.args["image"]
    print image_name

    def download_stream():

        # TODO: See if we can reuse other client
        from docker import Client
        docker_client = Client(base_url="unix://var/run/docker.sock")

        for data in docker_client.pull(image_name, stream=True):
            print data
            yield "data: {}\n\n".format(json.dumps(data))

        yield "data: {}\n\n".format(json.dumps({
            "status": "COMPLETE"
        }))

    return Response(download_stream(), mimetype="text/event-stream")
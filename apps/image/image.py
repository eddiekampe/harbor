from flask import Blueprint

image = Blueprint("image", __name__)


# List images
@image.route("/images", methods=["GET"])
def list_images():
    return 501


# Show image by id
@image.route("/images/<image_id>", methods=["GET"])
def show_image(image_id):
    return 501


# Create a new image
@image.route("/images", methods=["POST"])
def create_image():
    return 501
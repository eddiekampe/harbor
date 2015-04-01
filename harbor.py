import os
import traceback
import subprocess
import lib.notification as notification

from docker import Client
from flask import Flask, url_for, redirect, send_from_directory, render_template, g, request, flash
from apps.image.image import image
from apps.container.container import container
from lib import filters


# Setup application and config
app = Flask(__name__)
app.secret_key = "rPbY^+$EDU/:@3M"
# Register blueprints
app.register_blueprint(image, url_prefix="/images")
app.register_blueprint(container, url_prefix="/containers")
# Register filters
filters.register_all(app)


@app.before_request
def setup():
    g.docker_client_address = DOCKER_CLIENT_ADDRESS = "unix://var/run/docker.sock"
    g.docker_client = Client(base_url=DOCKER_CLIENT_ADDRESS)


@app.errorhandler(404)
def not_found(error):
    print error
    return redirect(url_for("overview"))


@app.errorhandler(500)
def server_error(error):
    print traceback.print_stack()
    print error
    return error  # redirect(url_for("home"))


@app.context_processor
def prepare_request():
    """
    Fetch number of images and containers
    """
    images = g.docker_client.images(quiet=True)
    containers = g.docker_client.containers(quiet=True, all=True)
    events = []

    def get_events():

        events_generator = g.docker_client.events()
        for event in events_generator:
            yield event

    # events = get_events()

    return dict(num_images=len(images), num_containers=len(containers), events=events, docker_client=g.docker_client_address)


@app.route("/", methods=["GET"])
def overview():
    """
    Landing page, display info about the host
    """
    version = g.docker_client.version()
    info = g.docker_client.info()
    return render_template("overview.html", version=version, info=info)


@app.route("/search", methods=["POST"])
def search():
    """
    Searches containers and images for a match.

    :todo: Improve matching comparison. Maybe Regex matching?
    """
    search_string = request.form["search_string"]
    containers = g.docker_client.containers(all=True)
    images = g.docker_client.images()

    images = [img for img in images if search_string in img.get("RepoTags")]
    containers = [cont for cont in containers if search_string in cont.get("Image")]

    return render_template("search.html", search_string=search_string, images=images, containers=containers)


@app.route("/update", methods=["GET"])
def update_project():
    """
    Pull the latest changes from GitHub
    """
    output = subprocess.check_output(["git", "pull"])
    # TODO: Need to parse the output to see what was the result
    flash(output, notification.SUCCESS)

    return redirect(url_for("settings"))


@app.route("/client", methods=["GET", "POST"])
def settings():
    """
    Display host settings.
    Also end-point for updates
    """
    if request.method == "POST":
        print "POST"

    docker_client_address = g.docker_client.base_url
    return render_template("settings.html", client_address=docker_client_address)


@app.route("/favicon.ico")
def favicon():
    return send_from_directory(os.path.join(app.root_path, "static"), "images/favicon.ico")


if __name__ == "__main__":

    config = {
        "host": "0.0.0.0",
        "debug": bool(os.environ.get("HARBOR_DEBUG", False)),
        "use_reloader": True,
        "threaded": True
    }

    app.run(**config)
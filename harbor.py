import traceback
from docker import Client
import os

from flask import Flask, url_for, redirect, send_from_directory, json, render_template, g, request

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
    g.docker_client = Client(base_url="unix://var/run/docker.sock")


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
    # Fetch number of images and containers
    images = g.docker_client.images(quiet=True)
    containers = g.docker_client.containers(quiet=True, all=True)
    return dict(num_images=len(images), num_containers=len(containers))


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


@app.route("/about")
def about():
    return 501


@app.route("/favicon.ico")
def favicon():
    return send_from_directory(os.path.join(app.root_path, "static"), "images/favicon.ico")


@app.route("/environment")
def get_environment():
    return json.dumps({"configuration": "dev"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", use_reloader=True, threaded=True)

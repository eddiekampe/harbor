import os

from flask import Flask, url_for, redirect, send_from_directory, json

from apps.image.image import image
from apps.container.container import container

# Setup application and config
application = app = Flask(__name__)
# Register blueprints
app.register_blueprint(image, url_prefix="/images")
app.register_blueprint(container, url_prefix="/containers")


@app.errorhandler(404)
def not_found(error):
    print error
    return redirect(url_for("home"))


@app.errorhandler(500)
def server_error(error):
    print error
    return error  # redirect(url_for("home"))


@app.route("/")
def home():
    return redirect(url_for("image.list_images"))


@app.route("/about")
def about():
    return 501


@app.route("/favicon.ico")
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'images/favicon.ico')


@app.route("/environment")
def get_environment():
    return json.dumps({"configuration": "dev"})


if __name__ == "__main__":
    app.run(use_reloader=True)
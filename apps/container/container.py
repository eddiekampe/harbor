from flask import Blueprint, render_template, redirect, url_for, flash, request, g

container = Blueprint("container", __name__)

SUCCESS = "success"
WARNING = "warning"


# List containers
@container.route("/", methods=["GET"])
def list_containers():

    containers = g.docker_client.containers(all=True)
    images = g.docker_client.images()

    return render_template("container/list.html", containers=containers, images=images)


# Show container by id
@container.route("/<container_id>", methods=["GET"])
def inspect_container(container_id):
    entry = g.docker_client.inspect_container(container_id)
    return render_template("container/entry.html", container=entry)


# Delete container by id
@container.route("/<container_id>/delete", methods=["GET"])
def delete_container(container_id):

    feedback = g.docker_client.remove_container(container_id)
    if feedback is None:
        flash("Container {} was successfully deleted!".format(container_id), SUCCESS)
    else:
        flash(feedback, WARNING)

    return redirect(url_for("container.list_containers"))


# Start container by id
@container.route("/<container_id>/start", methods=["GET"])
def start_container(container_id):

    feedback = g.docker_client.start(container_id)
    if feedback is None:
        flash("Container {} was successfully started".format(container_id), SUCCESS)
    else:
        flash(feedback, WARNING)

    return redirect(url_for("container.list_containers"))


# Stop container by id
@container.route("/<container_id>/stop", methods=["GET"])
def stop_container(container_id):

    feedback = g.docker_client.stop(container_id)
    if feedback is None:
        flash("Container {} was successfully stopped".format(container_id), SUCCESS)
    else:
        flash(feedback, WARNING)

    return redirect(url_for("container.list_containers"))


# Create a container
@container.route("/", methods=["POST"])
def create_container():

    # TODO: Add more logic
    container_name = request.form["inputName"]
    image = request.form["image"]

    if None not in [image, container_name]:
        new_container = g.docker_client.create_container(image=image, name=container_name)
        flash(new_container, SUCCESS)

    return redirect(url_for("container.list_containers"))
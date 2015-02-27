from docker.errors import APIError
from flask import Blueprint, render_template, redirect, url_for, flash, request, g
from lib.notification import SUCCESS, ERROR, WARNING

container = Blueprint("container", __name__)


@container.route("/", methods=["GET"])
def list_containers():
    """
    List containers
    """
    containers = []
    images = []

    try:
        containers = g.docker_client.containers(all=True)
        images = g.docker_client.images()

    except APIError as e:
        flash(e.explanation, ERROR)

    return render_template("container/list.html", containers=containers, images=images)


@container.route("/<container_id>", methods=["GET"])
def inspect_container(container_id):
    """
    View detailed information about the container
    """

    try:
        entry = g.docker_client.inspect_container(container_id)
        return render_template("container/entry.html", container=entry)

    except APIError as e:
        flash(e.explanation, ERROR)

    return redirect(url_for("container.list_containers"))


@container.route("/<container_id>/delete", methods=["GET"])
def delete_container(container_id):
    """
    Delete container

    force = True/true
        Let the user to force the delete action. Will not warn if container is running

    """
    force_delete = request.args.get("force", False) in ["True", "true"]

    try:
        feedback = g.docker_client.remove_container(container_id, force=force_delete)

        if feedback is None:
            flash("Container {} was successfully deleted!".format(container_id), SUCCESS)
        else:
            flash(feedback, WARNING)

    except APIError as e:
        flash(e.explanation, ERROR)

    return redirect(url_for("container.list_containers"))


@container.route("/<container_id>/start", methods=["GET"])
def start_container(container_id):
    """
    Start an idle container
    :param container_id: Id of the container to start
    :return:
    """
    try:
        feedback = g.docker_client.start(container_id)

        if feedback is None:
            flash("Container {} was successfully started".format(container_id), SUCCESS)
        else:
            flash(feedback, WARNING)

    except APIError as e:
        flash(e.explanation, ERROR)

    return redirect(url_for("container.list_containers"))


@container.route("/<container_id>/pause", methods=["GET"])
def pause_container(container_id):
    """
    Pause a running container
    :param container_id: Id of the container to pause
    :return:
    """
    try:
        feedback = g.docker_client.pause(container_id)

        if feedback is None:
            flash("Container {} was successfully paused".format(container_id), SUCCESS)
        else:
            flash(feedback, WARNING)

    except APIError as e:
        flash(e.explanation, ERROR)

    return redirect(url_for("container.list_containers"))


@container.route("/<container_id>/unpause", methods=["GET"])
def unpause_container(container_id):
    """
    Resume a paused container
    :param container_id: Id of the container to unpause
    :return:
    """
    try:
        feedback = g.docker_client.unpause(container_id)

        if feedback is None:
            flash("Container {} was successfully unpaused".format(container_id), SUCCESS)
        else:
            flash(feedback, WARNING)

    except APIError as e:
        flash(e.explanation, ERROR)

    return redirect(url_for("container.list_containers"))


@container.route("/<container_id>/stop", methods=["GET"])
def stop_container(container_id):
    """
    Stop container from running
    """
    try:
        feedback = g.docker_client.stop(container_id)
        if feedback is None:
            flash("Container {} was successfully stopped".format(container_id), SUCCESS)
        else:
            flash(feedback, WARNING)

    except APIError as e:
        flash(e.explanation, ERROR)

    return redirect(url_for("container.list_containers"))


@container.route("/", methods=["POST"])
def create_container():
    """
    Create a new container based on an image

    @TODO:
        Add more properties. Should atleast match the API

    """
    container_name = request.form["container_name"]
    image = request.form["image"]
    action = request.form["action"]
    scale = int(request.form["scale"])

    if None not in [image, container_name, scale]:

        for instance in range(scale):

            if scale > 1 and container_name != "":
                container_id = g.docker_client.create_container(image=image, name="{}-{}".format(container_name, instance + 1))
            else:
                container_id = g.docker_client.create_container(image=image)

            flash("Container {} was successfully created".format(container_id), SUCCESS)

            if action == "create_and_start":
                feedback = g.docker_client.start(container_id)
                if feedback is None:
                    flash("Container {} was successfully started".format(container_id), SUCCESS)
                else:
                    flash(feedback, WARNING)

    return redirect(url_for("container.list_containers"))
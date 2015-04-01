import json
from docker.errors import APIError
from flask import Blueprint, render_template, redirect, url_for, flash, request, g, Response
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
        for image in images:

            image_info = g.docker_client.inspect_image(image.get("Id"))
            exposed_ports = image_info.get("Config", {}).get("ExposedPorts")

            if exposed_ports:
                image["Port"], image["Protocol"] = tuple(exposed_ports.keys()[0].split("/"))

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
        return render_template("container/entry/_info.html", container=entry)

    except APIError as e:
        flash(e.explanation, ERROR)

    return redirect(url_for("container.list_containers"))


@container.route("/<container_id>/logs", methods=["GET"])
def container_logs(container_id):
    """
    View logs originating from the container
    """
    try:
        logs = g.docker_client.logs(container_id, stdout=True, stderr=True)
        container_entry = {"Id": container_id}
        return render_template("container/entry/_logs.html", logs=logs, container=container_entry)

    except APIError as e:
        flash(e.explanation, ERROR)

    return redirect(url_for("container.list_containers"))


@container.route("/<container_id>/processes", methods=["GET"])
def container_processes(container_id):
    """
    View top processes running inside the container
    """
    try:
        processes = g.docker_client.top(container_id)
        container_entry = {"Id": container_id}
        return render_template("container/entry/_processes.html", processes=processes, container=container_entry)

    except APIError as e:
        flash(e.explanation, ERROR)

    return redirect(url_for("contaienr.list_containers"))


@container.route("/<container_id>/stats", methods=["GET"])
def stats(container_id):
    """
    Display stats for the container
    """
    container_entry = {"Id": container_id}
    return render_template("container/entry/_stats.html", container=container_entry)


@container.route("/<container_id>/stats/feed")
def stats_feed(container_id):
    """
    Generator that continously report stats about a container
    """
    def stats_stream():

        from docker import Client
        docker_client = Client(base_url="unix://var/run/docker.sock")

        stats_generator = docker_client.stats(container_id)
        for stat in stats_generator:
            yield "data: {}\n\n".format(json.dumps(stat))

    return Response(stats_stream(), mimetype="text/event-stream")


@container.route("/<container_id>/delete", methods=["GET"])
def delete_container(container_id):
    """
    Delete a container
    :param container_id: Id of the container
    :argument force: Let the user to force the delete action. Will not warn if container is running
    :return:
    """
    force_delete = request.args.get("force", False) in ["True", "true"]
    action = g.docker_client.remove_container
    success_message = "Container {} was successfully deleted!".format(container_id)
    args = {
        "container": container_id,
        "force": force_delete
    }

    handle_action(action, args, success_message)
    return redirect(url_for("container.list_containers"))


@container.route("/<container_id>/start", methods=["GET"])
def start_container(container_id):
    """
    Start an idle container
    :param container_id: Id of the container to start
    :return:
    """
    action = g.docker_client.start
    success_message = "Container {} was successfully started!".format(container_id)
    args = {"container": container_id}

    handle_action(action, args, success_message)
    return redirect(url_for("container.list_containers"))


@container.route("/<container_id>/pause", methods=["GET"])
def pause_container(container_id):
    """
    Pause a running container
    :param container_id: Id of the container to pause
    :return:
    """
    action = g.docker_client.pause
    success_message = "Container {} was successfully paused!".format(container_id)
    args = {"container": container_id}

    handle_action(action, args, success_message)
    return redirect(url_for("container.list_containers"))


@container.route("/<container_id>/unpause", methods=["GET"])
def unpause_container(container_id):
    """
    Resume a paused container
    :param container_id: Id of the container to unpause
    :return:
    """
    action = g.docker_client.unpause
    success_message = "Container {} was successfully unpaused!".format(container_id)
    args = {"container": container_id}

    handle_action(action, args, success_message)
    return redirect(url_for("container.list_containers"))


@container.route("/<container_id>/restart", methods=["GET"])
def restart_container(container_id):
    """
    Restart a container
    :param container_id: Id of the container to restarted
    :return:
    """
    action = g.docker_client.restart
    success_message = "Container {} was successfully restarted!".format(container_id)
    args = {"container": container_id}

    handle_action(action, args, success_message)
    return redirect(url_for("container.list_containers"))


@container.route("/<container_id>/stop", methods=["GET"])
def stop_container(container_id):
    """
    Stop a running container
    :param container_id: Id of the container to stop
    :return:
    """
    action = g.docker_client.stop
    success_message = "Container {} was successfully stopped!".format(container_id)
    args = {"container": container_id}

    handle_action(action, args, success_message)
    return redirect(url_for("container.list_containers"))


@container.route("/<container_id>/kill", methods=["GET"])
def kill_container(container_id):
    """
    Kill a running container (SIGKILL signal).
    :param container_id: Id of the container to kill
    :return:
    """
    action = g.docker_client.kill
    success_message = "Container {} was successfully killed!".format(container_id)
    args = {"container": container_id}

    handle_action(action, args, success_message)
    return redirect(url_for("container.list_containers"))


@container.route("/", methods=["POST"])
def create_container():
    """
    Create a new container based on an image
    :todo: Add more properties. Should at least match the API
    :return:
    """
    container_name = request.form["container_name"]
    image = request.form["image"]
    action = request.form["action"]
    scale = int(request.form["scale"])
    # Ports
    protocol = request.form["protocol"]
    ip_address = request.form["ip_address"]
    host_port = request.form["host_port"]
    container_port = request.form["container_port"]
    privileged_mode = request.form.get("privileged_mode", False)

    port_bindings = {
        container_port: (ip_address, host_port)
    }

    if None not in [image, container_name, scale]:

        for instance in range(scale):

            if scale > 1 and container_name != "":
                container_id = g.docker_client.create_container(image=image,
                                                                name="{}-{}".format(container_name, instance + 1))
            else:
                container_id = g.docker_client.create_container(image=image)

            flash("Container {} was successfully created".format(container_id), SUCCESS)

            if action == "create_and_start":
                feedback = g.docker_client.start(container_id, port_bindings=port_bindings, privileged=privileged_mode)

                if feedback is None:
                    flash("Container {} was successfully started".format(container_id), SUCCESS)
                else:
                    flash(feedback, WARNING)

    return redirect(url_for("container.list_containers"))


def handle_action(func, args, success_message):
    """
    Apply the func with the given args.
    :param func: Function to run
    :param args: Arguments to function
    :param success_message: Success message
    :return:
    """
    try:
        feedback = func(**args)

        if feedback is None:
            flash(success_message, SUCCESS)
        else:
            flash(feedback, WARNING)

    except APIError as e:
        flash(e.explanation, ERROR)
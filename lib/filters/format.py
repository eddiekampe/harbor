from datetime import datetime


def register(app):
    app.jinja_env.filters["b_to_mb"] = b_to_mb
    app.jinja_env.filters["date_string"] = date_string
    app.jinja_env.filters["log_text"] = log_text
    app.jinja_env.filters["process_text"] = process_text


def b_to_mb(byte_string):
    """
    Convert bytes into megabytes
    """
    return "{}Mb".format(byte_string/1000000)


def date_string(timestamp):
    """
    Convert timestamp into a readable date string
    Example: 1414106559 -> 24-10-2014
    """
    return datetime.fromtimestamp(timestamp).strftime("%d-%m-%Y")


def log_text(logs):
    """
    Clean docker logs into a readable format
    :param logs: Log entries
    :return: Cleaned version of the logs
    """

    # Unsure why this is in the log output
    replacements = ("[32m", ""), \
                   ("[36m", ""), \
                   ("[38m", ""), \
                   ("[39m", ""), \
                   ("[90m", "")

    return reduce(lambda in_string, kv: in_string.replace(*kv), replacements, logs)


def process_text(processes):
    """
    Format docker process list into a readable format
    :param processes: Processes
    :return: Cleaned version of the processes
    """

    titles = processes.get("Titles", [])
    processes = processes.get("Processes", [])

    readable_titles = "\t\t\t".join(titles)
    readable_processes = []

    for process_attributes in processes:
        readable_process = "\t\t".join(process_attributes)
        readable_processes.append(readable_process)

    readable_processe = "\n".join(readable_processes)

    return readable_titles + "\n" + readable_processe
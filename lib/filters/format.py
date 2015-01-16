from datetime import datetime


def register(app):
    app.jinja_env.filters["b_to_mb"] = b_to_mb
    app.jinja_env.filters["date_string"] = date_string


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
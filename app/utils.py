import json

def pretty_print(data, **kwargs):
    print("\033[92m{}\033[00m".format(data), **kwargs)


def error_resp(message):
    return {
        'status': 'error',
        'message': message
    }


def success_resp(message):
    return {
        'status': 'success',
        'message': message
    }

def load_json(file_path: str) -> dict | list:
    """Loads the file located at the given path.

    Args:
        (str): Path of the file to be loaded

    Returns:
        (dict | list): Object with contents of the loaded JSON file
    """
    try:
        with open(file_path, "r") as json_file:
            return json.load(json_file)
    except FileNotFoundError:
        print(f"File {file_path} does not exist")
        exit(1)
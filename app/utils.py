from string import ascii_letters, digits


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

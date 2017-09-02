import os

import errors

def get_file(path):
    try:
        with open(path, 'r') as f:
            contents = f.read()
            error = False
    except FileNotFoundError:
        contents = errors.FILE_NOT_EXIST
        error = True
    return contents, error

def create_file(path, contents):
    if os.path.isfile(path):
        return errors.FILE_EXISTS, True
    parent_directory = os.path.dirname(path)
    os.makedirs(parent_directory, exist_ok=True)
    with open(path, 'w') as f:
        f.write(contents)
        error = False
    return contents, error

def update_file(path, contents):
    if not os.path.isfile(path):
        return errors.FILE_NOT_EXIST, True
    with open(path, 'w') as f:
        f.write(contents)
        error = False
    return contents, error

def delete_file(path):
    try:
        os.remove(path)
        contents = ''
        error = False
    except FileNotFoundError:
        contents = errors.FILE_NOT_EXIST
        error = True
    return contents, error

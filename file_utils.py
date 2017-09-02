import math
import os
import string

import errors

ALPHA_NUMERIC = string.ascii_letters + string.digits

def get_file(path):
    try:
        with open(path, 'r') as f:
            contents = f.read()
            error = False
    except FileNotFoundError:
        contents = errors.FILE_NOT_EXIST
        error = True
    except IsADirectoryError:
        contents = errors.IS_A_DIRECTORY
        error = True
    return contents, error

def create_file(path, contents):
    if os.path.isfile(path):
        return errors.FILE_EXISTS, True
    if os.path.isdir(path):
        return errors.IS_A_DIRECTORY, True
    parent_directory = os.path.dirname(path)
    os.makedirs(parent_directory, exist_ok=True)
    with open(path, 'w') as f:
        f.write(contents)
        error = False
    return contents, error

def update_file(path, contents):
    if os.path.isdir(path):
        return errors.IS_A_DIRECTORY, True
    if not os.path.isfile(path):
        return errors.FILE_NOT_EXIST, True
    with open(path, 'w') as f:
        f.write(contents)
        error = False
    return contents, error

def delete_file(path):
    if os.path.isdir(path):
        return errors.IS_A_DIRECTORY, True
    try:
        os.remove(path)
        contents = ''
        error = False
    except FileNotFoundError:
        contents = errors.FILE_NOT_EXIST
        error = True
    return contents, error


def num_files(path):
    if os.path.isfile(path):
        return 1
    total = 0
    children = os.listdir(path)
    for child in children:
        total += num_files(path + '/' + child)
    return total

def num_chars_in_file(filename):
    with open(filename, 'r') as f:
        return sum(1 for c in f.read() if c in ALPHA_NUMERIC)

def num_chars_in_dir(path):
    if os.path.isfile(path):
        return [num_chars_in_file(path)]
    num_chars = []
    children = os.listdir(path)
    for child in children:
        num_chars += num_chars_in_dir(path + '/' + child)
    return num_chars

def avg_num_chars(path):
    num_chars = num_chars_in_dir(path)
    N = len(num_chars)
    mean = sum(num_chars) / N
    sd = math.sqrt(sum(((num - mean) ** 2) for num in num_chars) / (N - 1))
    return {
        'mean': mean,
        'sd': sd,
    }

def total_bytes(path):
    if os.path.isfile(path):
        return os.stat(path).st_size
    total = 0
    children = os.listdir(path)
    for child in children:
        total += total_bytes(path + '/' + child)
    return total

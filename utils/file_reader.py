import json


def read_json_file(file_name):
    with open(file_name, "r") as file:
        file_content = json.loads(file.read())
    return file_content
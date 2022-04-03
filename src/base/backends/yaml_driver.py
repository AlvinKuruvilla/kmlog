# pylint: disable=C0114
# pylint: disable=C0301
# pylint: disable=E0401
# pylint: disable=E0401
# pylint: disable=R1710

# Copyright 2021 - 2022, Alvin Kuruvilla <alvineasokuruvilla@gmail.com>, Dr. Rajesh Kumar <Rajesh.Kumar@hofstra.edu>

# Use of this source code is governed by an MIT-style
# license that can be found in the LICENSE file or at
# https://opensource.org/licenses/MIT.

import os
import yaml
from prettytable import PrettyTable
from base.log import Logger


def path_is_valid(path: str) -> bool:
    """Given a path, return True if it is a valid file path"""
    log = Logger()
    is_file = os.path.isfile(path)
    if is_file:
        # Now check that the extension is YAML
        if path.lower().endswith(".yaml"):
            return True
        log.km_fatal("The provided path is not a YAML file")
        return False

    log.km_fatal("The provided path was not a file")
    return False


def get_value_from_key(filepath: str, key: str):
    """This function looks for the value associated with a provided key in a provided filepath"""
    if path_is_valid(filepath):
        with open(filepath, "r", encoding="utf8") as stream:
            try:
                data = yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                print(exc)
            if key in data:
                return data[key]
            # NOTE: Right now we are going to assume that every field in the yaml file is filled correctly, ie there are no empty fields, so that this would mean no result rather than potentially getting a value... Since we cannot guarantee correctness we should think of alternatives to empty string that would give the same indication
            return ""


def get_yaml_values_from_file(filepath) -> list:
    """From a path to a YAML file load the file and return its values as a list"""
    if path_is_valid(filepath):
        with open(filepath, "r", encoding="utf8") as stream:
            try:
                data = yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                print(exc)
        return list(data.values())


def get_yaml_keys_from_file(filepath) -> list:
    """From a path to a YAML file load the file and return its keys as a list"""
    if path_is_valid(filepath):
        with open(filepath, "r", encoding="utf8") as stream:
            try:
                data = yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                print(exc)
        return list(data.keys())


def get_all_associated_values(key: str):
    """A helper function to retrieve all values for a given key across all yaml files stored in the 'users' directory"""
    store = []
    directory = os.path.join(os.getcwd(), "users")
    for file in os.scandir(directory):
        if file.path.endswith(".yaml") and file.is_file():
            value = get_value_from_key(file.path, key)
            # Type cast is required here to make sure str to int comparisons don't fail
            store.append(str(value))
    return store


def write_to_yaml_file(filename: str, data: dict) -> None:
    """This function enables the YAMLParser to write a data dictionary as a
    YAML file
    Note: This function will always store resulting yaml files in
    the 'users' folder. A convention we may stick to is to use the first letter
    of their first and last name and their user_id (because that will be
    unique to each user) or just the user_id. If the file does not exist
    when calling thus function it will also create it
    """
    file_path = os.path.join(os.getcwd(), "users", filename + ".yaml")
    with open(file_path, "w+", encoding="utf8") as file:
        yaml.dump(data, file, sort_keys=False)


def print_as_table(filepath):
    """Take in a path to a YAML file and display its contents as a table"""
    keys = get_yaml_keys_from_file(filepath)
    values = get_yaml_values_from_file(filepath)
    assert len(keys) == len(
        values
    ), "Cannot create table if the number of rows (keys) != number of columns (values)!"
    out = PrettyTable()
    out.field_names = keys
    out.add_row(values)
    print(out)


def display_user_info_table():
    # ? This may need to be moved to the yaml_ops and sql_ops files respectively to replace our current PrettyTable
    # implementation
    pass

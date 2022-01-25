import yaml
import os
from base.log import Logger
from prettytable import PrettyTable


def path_is_valid(path: str) -> bool:
    log = Logger()
    is_file = os.path.isfile(path)
    if is_file:
        # Now check that the extension is YAML
        if path.lower().endswith(".yaml"):
            return True
        else:
            log.km_fatal("The provided path is not a YAML file")
            return False
    else:
        log.km_fatal("The provided path was not a file")
        return False


class YAMLDriver:
    def __init__(self) -> None:
        return

    def write_to_yaml_file(self, filename: str, data: dict) -> None:
        """This function enables the YAMLParser to write a data dictionary as a
        YAML file
        Note: This function will always store resulting yaml files in
        the 'users' folder. A convention we may stick to is to use the first letter
        of their first and last name and their user_id (because that will be
        unique to each user) or just the user_id. If the file does not exist
        when calling thus function it will also create it
        """
        file_path = os.path.join(os.getcwd(), "src", "users", filename + ".yaml")
        with open(file_path, "w+") as file:
            yaml.dump(data, file, sort_keys=False)

    def print_as_table(self, filepath):
        """Take in a path to a YAML file and display its contents as a table"""
        keys = self.get_yaml_keys_from_file(filepath)
        values = self.get_yaml_values_from_file(filepath)
        assert len(keys) == len(
            values
        ), "Cannot create table if the number of rows (keys) != number of columns (values)!"
        out = PrettyTable()
        out.field_names = keys
        out.add_row(values)
        print(out)

    def get_yaml_keys_from_file(self, filepath) -> list:
        """From a path to a YAML file load the file and return its keys as a list"""
        if path_is_valid(filepath):
            with open(filepath, "r") as stream:
                try:
                    data = yaml.safe_load(stream)
                except yaml.YAMLError as exc:
                    print(exc)
            return list(data.keys())

    def get_yaml_values_from_file(self, filepath) -> list:
        """From a path to a YAML file load the file and return its values as a list"""
        if path_is_valid(filepath):
            with open(filepath, "r") as stream:
                try:
                    data = yaml.safe_load(stream)
                except yaml.YAMLError as exc:
                    print(exc)
            return list(data.values())

    def get_value_from_key(self, filepath: str, key: str):
        """This function looks for the value associated with a provided key in a provided filepath"""
        if path_is_valid(filepath):
            with open(filepath, "r") as stream:
                try:
                    data = yaml.safe_load(stream)
                except yaml.YAMLError as exc:
                    print(exc)
                if key in data:
                    return data[key]
                else:
                    # Fix: Right now we are going to assume that every field in the yaml file is filled correctly, ie there are no empty fields, so that this would mean no result rather than potentially getting a value... Since we cannot guarantee correctness we should think of alternatives to empty string that would give the same indication
                    return ""

    def get_all_associated_values(self, key: str):
        """A helper function to retrieve all values for a given key across all yaml files stored in the 'users' directory"""
        store = []
        directory = os.path.join(os.getcwd(), "src", "users")
        for file in os.scandir(directory):
            if file.path.endswith(".yaml") and file.is_file():
                value = self.get_value_from_key(file.path, key)
                # Type cast is required here to make sure str to int comparisons don't fail
                store.append(str(value))
        return store

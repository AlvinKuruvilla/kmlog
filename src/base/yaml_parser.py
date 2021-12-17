class YAMLParser():
    def __init__(self) -> None:
        pass

    def write_as_yaml_file(self, data, filename=None) -> None:
        """This function enables the YAMLParser to write a data dictionary as a
        YAML file Note: If a filename is not provided this function will
        internally use the first and last initials of the user as part of the
        filename. If a file in the 'data' folder already exists with that name,
        the function will append a number to the filename to resolve the
        conflict
        """
        pass

    def print_as_table(self, filepath):
        """Take in a path to a YAML file and display its contents as a table"""
        pass

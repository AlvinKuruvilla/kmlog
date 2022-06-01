import os
import re
import yaml
import pprint
import enum

from rich.highlighter import RegexHighlighter
from rich.console import Console
from rich.theme import Theme
from rich.panel import Panel
from rich.table import Table

from base.log import Logger
from prettytable import PrettyTable


class OptionHighlighter(RegexHighlighter):
    highlights = [
        r"(?P<switch>\-\w)",
        r"(?P<option>\-\-[\w\-]+)",
    ]


class FileType(enum.Enum):
    CSV = 0
    YAML = 1
    NotAFile = 3


def is_csv_file(filename: str) -> bool:
    hlog = Logger()
    if filename.endswith(".csv") and os.path.exists(filename):
        return True
    hlog.km_error("Provided path is not a valid CSV file or does not exist")
    return False


def is_yaml_file(filename: str) -> bool:
    hlog = Logger()
    if filename.endswith(".yaml") and os.path.exists(filename):
        return True
    hlog.km_error("Provided path is not a valid YAML file or does not exist")
    return False


def render_csv(path):
    x = PrettyTable()
    x.field_names = ["Press or Release", "Key", "Times"]
    with open(path) as f:
        line = f.readline()
        while line:
            x.add_row(line.rstrip().split(","))
            line = f.readline()
    print(x)


def grab_args(cmd):
    chunks = re.split(" +", cmd)
    a = list(chunks[0:])
    return a[1]


def verify_file_path(path):
    log = Logger()
    # print(path)
    if os.path.exists(path):
        if is_csv_file(path):
            return FileType.CSV
        elif is_yaml_file(path):
            return FileType.YAML
        else:
            return FileType.NotAFile
    else:
        log.km_error("Provided path does not exist")
        return False


def render_yaml(filename):
    y = yaml.safe_load(open(filename, "r"))
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(y)


def colorize(d, key_format="\033[1;32m", value_format="\033[1;34m"):
    for key in d.keys():
        print(key_format, key + ":", value_format, d[key])


def command_table():
    highlighter = OptionHighlighter()
    console = Console(
        theme=Theme(
            {
                "option": "bold cyan",
                "switch": "bold green",
            }
        ),
        highlighter=highlighter,
    )
    command_dict = {
        "help": "Prints out the basic usage instructions to interact with kmshell",
        "render [PATH]": "Render either CSV or YAML files in the terminal by providing their absolute path",
    }
    table = Table(title="Commands")
    table.add_column("Command", style="cyan", no_wrap=True)
    table.add_column("Description", style="white")
    for key, value in command_dict.items():
        table.add_row(key, value)
    console.print(Panel(table, border_style="dim", title="Options", title_align="left"))

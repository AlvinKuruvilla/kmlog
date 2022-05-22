import os
import re
from rich.highlighter import RegexHighlighter

from base.log import Logger
from prettytable import PrettyTable


class OptionHighlighter(RegexHighlighter):
    highlights = [
        r"(?P<switch>\-\w)",
        r"(?P<option>\-\-[\w\-]+)",
    ]


def is_csv_file(filename: str) -> bool:
    hlog = Logger()
    if filename.endswith(".csv") and os.path.exists(filename):
        return True
    hlog.km_error("Provided path is not a valid CSV file or does not exist")
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
    if os.path.exists(path):
        if is_csv_file(path):
            return True
        else:
            log.km_error("Provided path is not a CSV file")
            return False
    else:
        log.km_error("Provided path does not exist")
        return False

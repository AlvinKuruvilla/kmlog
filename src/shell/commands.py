from rich.console import Console
from rich.theme import Theme
from base.log import Logger
from shell.utils import command_table, render_csv, OptionHighlighter, render_yaml
import sys


def exit():
    """Exit the shell and return to the main menu"""
    log = Logger()
    log.km_info("Exiting KMLogger")
    sys.exit(0)


def show_banner():
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
    console.print(
        f"[b]KMShell[/b] [magenta]v{1.0}[/] \n\n[dim]A shell version of KMLogger\n",
        justify="center",
    )


def cmd_help():
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
    console.print("Usage: [b][COMMAND][/b] [b cyan]<ARGUMENTS>\n")
    command_table()


def show_csv(filename):
    render_csv(filename)


def show_yaml(filename):
    render_yaml(filename)

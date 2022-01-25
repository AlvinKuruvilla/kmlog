from clint.textui import colored
from pyfiglet import Figlet
from colorama import Fore, Style
import os
import progressbar
import time

text_color = {
    "redBold": Style.BRIGHT + Fore.RED,
    "white": Style.NORMAL + Fore.WHITE,
    "whiteBold": Style.BRIGHT + Fore.WHITE,
}
background_colors = {"UNDERL": "\033[4m", "DARKCYAN": "\033[36m", "ENDC": "\033[0m"}


def banner(text) -> None:
    """
    Stylizes text reminiscent to a banner.

    Parameters
    ----------
    text: str
          The text to be made into a banner.
    Returns
    -------
    None
    """
    block_text(text)
    print(
        "\t"
        + text_color["redBold"]
        + "                |_|"
        + text_color["white"]
        + " 2021 by "
        + text_color["whiteBold"]
        + "Alvin Kuruvilla"
        + text_color["white"]
        + "\n"
    )
    print("A Keylogger and mouse tracker for research purposes ")


def block_text(text) -> None:
    """
    Block text.

    Parameters
    ----------
    text: str
          The text to be made into a banner.
    Returns
    -------
    None
    """
    result = Figlet()
    print(colored.cyan(result.renderText(text)))


def km_prompt(text):
    if text == "":
        return (
            background_colors["UNDERL"]
            + background_colors["DARKCYAN"]
            + "set"
            + background_colors["ENDC"]
            + "> "
        )
    else:
        return (
            background_colors["UNDERL"]
            + background_colors["DARKCYAN"]
            + "km"
            + background_colors["ENDC"]
            + "> "
            + text
        )


def clear_screen():
    if os.name == "posix":
        _ = os.system("clear")
    else:
        # for windows
        _ = os.system("cls")


def animated_marker(text: str):
    widgets = [text, progressbar.AnimatedMarker()]
    bar = progressbar.ProgressBar(widgets=widgets).start()

    for i in range(10):
        time.sleep(0.1)
        bar.update(i)

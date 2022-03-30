# pylint: disable=C0301
# pylint: disable=E0401
# pylint: disable=C0114

# Copyright 2021 - 2022, Alvin Kuruvilla <alvineasokuruvilla@gmail.com>, Dr. Rajesh Kumar <Rajesh.Kumar@hofstra.edu>

# Use of this source code is governed by an MIT-style
# license that can be found in the LICENSE file or at
# https://opensource.org/licenses/MIT.

import os
import time
import progressbar
from clint.textui import colored
from art import text2art
from colorama import Fore, Style


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
    print(colored.cyan(text2art(text)))


def km_prompt(text):
    """
    Create a custom user input prompt.

    Parameters
    ----------
    text: str
          The prompt text.
    Returns
    -------
    None
    """
    if text == "":
        return (
            background_colors["UNDERL"]
            + background_colors["DARKCYAN"]
            + "set"
            + background_colors["ENDC"]
            + "> "
        )

    return (
        background_colors["UNDERL"]
        + background_colors["DARKCYAN"]
        + "km"
        + background_colors["ENDC"]
        + "> "
        + text
    )


def clear_screen():
    """
    Platform specific clear screen function.

    Parameters
    ----------
    None

    Returns
    -------
    None
    """
    if os.name == "posix":
        _ = os.system("clear")
    else:
        # for windows
        _ = os.system("cls")


def animated_marker(text: str):
    """
    Create an animated progress bar marker.

    Parameters
    ----------
    text: str
          The text to be used in the progress bar.
    Returns
    -------
    None
    """
    widgets = [text, progressbar.AnimatedMarker()]
    progress_bar = progressbar.ProgressBar(widgets=widgets).start()

    for i in range(10):
        time.sleep(0.1)
        progress_bar.update(i)

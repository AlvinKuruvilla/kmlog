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
from enum import Enum


class CredentialType(Enum):
    FACEBOOK = 0
    INSTAGRAM = 1
    TWITTER = 2


class DisplayColors(Enum):
    BLUE = "\033[1;32m"
    YELLOW = "\033[1;34m"


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


def dprint(d, key_format="\033[1;32m", value_format="\033[1;34m"):
    for key in d.keys():
        print(key_format, key + ":", value_format, d[key])


def start_menu():
    print("\nChoose service you want to use : ")
    print(
        """
            1:  Start KMLogger
            2:  Exit
            """
    )


def display_credentials(cred_type: CredentialType):
    if cred_type == CredentialType.FACEBOOK:
        facebook_credentials = {
            "Username": "fpd1social@gmail.com",
            "Password": "Social@2022",
        }
        dprint(facebook_credentials)
        return
    elif cred_type == CredentialType.INSTAGRAM:
        print("Instagram Unimplemented")
        return
    elif cred_type == CredentialType.TWITTER:
        print("Twitter Unimplemented")
        return

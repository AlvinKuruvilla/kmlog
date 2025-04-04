# pylint: disable=C0301
# pylint: disable=E0401
# pylint: disable=C0114

# Copyright 2021 - 2022, Alvin Kuruvilla <alvineasokuruvilla@gmail.com>, Dr. Rajesh Kumar <Rajesh.Kumar@hofstra.edu>

# Use of this source code is governed by an MIT-style
# license that can be found in the LICENSE file or at
# https://opensource.org/licenses/MIT.

import os
import time
import sys
from enum import Enum
from typing import Dict
from clint.textui import colored
from art import text2art
from colorama import Fore, Style
from rich.progress import track
from base.log import Logger


class CredentialType(Enum):
    FACEBOOK = 0
    INSTAGRAM = 1
    TWITTER = 2

    def __str__(self) -> str:
        return "%s" % self.name


class DisplayColors(Enum):
    BLACK = "\033[0;30m"
    RED = "\033[0;31m"
    GREEN = "\033[0;32m"
    BROWN = "\033[0;33m"
    BLUE = "\033[0;34m"
    PURPLE = "\033[0;35m"
    CYAN = "\033[0;36m"
    LIGHT_GRAY = "\033[0;37m"
    DARK_GRAY = "\033[1;30m"
    LIGHT_RED = "\033[1;31m"
    LIGHT_GREEN = "\033[1;32m"
    YELLOW = "\033[1;33m"
    LIGHT_BLUE = "\033[1;34m"
    LIGHT_PURPLE = "\033[1;35m"
    LIGHT_CYAN = "\033[1;36m"


text_color = {
    "redBold": Style.BRIGHT + Fore.RED,
    "white": Style.NORMAL + Fore.WHITE,
    "whiteBold": Style.BRIGHT + Fore.WHITE,
}
background_colors = {"UNDERL": "\033[4m", "DARKCYAN": "\033[36m", "ENDC": "\033[0m"}


def banner(text: str) -> None:
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


def block_text(text: str) -> None:
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


def km_prompt(text: str) -> str:
    """
    Create a custom user input prompt.

    Parameters
    ----------
    text: str
          The prompt text.
    Returns
    -------
    str
    """
    if text == "":
        return (
            background_colors["UNDERL"]
            + background_colors["DARKCYAN"]
            + "km"
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


def clear_screen() -> None:
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


def animated_marker(text: str) -> None:
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
    for _ in track(range(100), description="[green]%s" % (text)):
        time.sleep(0.02)


def dprint(
    d: Dict[str, str], key_format: str = "\033[1;32m", value_format: str = "\033[1;34m"
) -> None:
    for key in d.keys():
        print(key_format, key + ":", value_format, d[key])


def display_menu(options):
    for index, option in enumerate(options, start=1):
        print(f"{index}:. {option}")


def get_user_choice(options):
    max_choice = len(options)
    choice = 0
    log = Logger()
    while True:
        display_menu(options)
        try:
            choice_input = input(
                km_prompt("Enter your choice (number) and press Enter: ")
            )
            choice = int(choice_input)
            if 1 <= choice <= max_choice:
                break
            else:
                log.km_error(f"Please enter a number between 1 and {max_choice}.\n")
        except ValueError:
            log.km_error("Invalid input. Please enter a number.\n")
    return choice - 1  # Adjust for 0-indexing


def start_menu():
    options = ["Start KMLogger", "Exit"]
    choice = get_user_choice(options)
    return choice


def windows_only_platform_menu():
    options = ["Facebook", "Instagram", "Twitter"]
    choice = get_user_choice(options)
    return choice


def display_account(account_number: int) -> None:
    if account_number == 1:
        acct = {
            "Name": "Jake Smith",
            "Email": "fpd1social@gmail.com",
            "Password": "Social@2022",
        }
        dprint(acct)
    if account_number == 2:
        acct = {
            "Name": "Jessica Coleman",
            "Email": "fpd2social@gmail.com",
            "Password": "Social@2022!",
        }
        dprint(acct)
    if account_number == 3:
        acct = {
            "Name": "Liam Williams",
            "Email": "fpd3social@gmail.com",
            "Password": "Social@2022!",
        }
        dprint(acct)


def display_credentials(cred_type: CredentialType, account_number: int) -> None:
    # display_account(account_number)
    # FIXME: A lot of this duplicated conditional code can be trimed down if we just do an update on the username key depending on the account number
    if account_number == 1:
        if cred_type == CredentialType.FACEBOOK:
            facebook_credentials = {
                "Username": "fpd1social@gmail.com",
                "Password": "Social@2022",
            }
            dprint(facebook_credentials)
            return
        elif cred_type == CredentialType.INSTAGRAM:
            insta_credentials = {
                "Username": "fpd1social@gmail.com",
                "Password": "Social@2022",
            }
            dprint(insta_credentials)
            return
        elif cred_type == CredentialType.TWITTER:
            twitter_credentials = {
                "Username": "fpd1social@gmail.com",
                "Password": "Social@2022",
            }
            dprint(twitter_credentials)
            return

    elif account_number == 3:
        if cred_type == CredentialType.FACEBOOK:
            facebook_credentials = {
                "Username": "fpd3social@gmail.com",
                "Password": "Social@2022",
            }
            dprint(facebook_credentials)
            return
        elif cred_type == CredentialType.INSTAGRAM:
            insta_credentials = {
                "Username": "fpd3social@gmail.com",
                "Password": "Social@2022",
            }
            dprint(insta_credentials)
            return
        elif cred_type == CredentialType.TWITTER:
            twitter_credentials = {
                "Username": "fpd3social@gmail.com",
                "Password": "Social@2022",
            }
            dprint(twitter_credentials)
            return


def select_account() -> None:
    print("Which account do you want to use: ")
    print("""1:  fpd1social@gmail.com""")


def account_number_to_email_fragment(account_number: int) -> str:
    if account_number == 1:
        frag = "fpd1"
        return frag
    elif account_number == 2:
        frag = "fpd2"
        return frag
    elif account_number == 3:
        frag = "fpd3"
        return frag
    else:
        raise ValueError("Invalid account number" + str(account_number))


def graceful_exit() -> None:
    hlog = Logger()
    hlog.km_info("Exiting KMLogger")
    sys.exit(0)

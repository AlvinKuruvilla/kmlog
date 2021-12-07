from clint.textui import colored
from pyfiglet import Figlet
from colorama import Fore, Style
import os
from dotenv import dotenv_values
import os

text_color = {
    "redBold": Style.BRIGHT+Fore.RED,
    "white": Style.NORMAL+Fore.WHITE,
    "whiteBold": Style.BRIGHT+Fore.WHITE,
}
background_colors = {
    "UNDERL": '\033[4m',
    "DARKCYAN": '\033[36m',
    "ENDC": '\033[0m'
}


def banner(text):
    block_text(text)
    print("\t" + text_color['redBold'] + "                |_|" + text_color['white'] +
          " 2021 by " + text_color['whiteBold'] + "Alvin Kuruvilla" + text_color['white']+"\n")
    print("A Keylogger and mouse tracker for research purposes ")


def block_text(text):
    result = Figlet()
    print(colored.cyan(result.renderText(text)))


def km_prompt(text):
    if text == "":
        return background_colors["UNDERL"] + background_colors["DARKCYAN"] + "set" + background_colors["ENDC"] + "> "
    else:
        return background_colors["UNDERL"] + background_colors["DARKCYAN"] + "km" + background_colors["ENDC"] + "> " + text


def clear_screen():
    if os.name == 'posix':
        _ = os.system('clear')
    else:
        # for windows
        _ = os.system('cls')

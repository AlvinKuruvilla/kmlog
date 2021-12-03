from clint.textui import colored
from pyfiglet import Figlet
from colorama import Fore, Style
import os
Color = {
    "redBold": Style.BRIGHT+Fore.RED,
    "white": Style.NORMAL+Fore.WHITE,
    "whiteBold": Style.BRIGHT+Fore.WHITE,
}


def banner(text):
    block_text(text)
    print("\t" + Color['redBold'] + "                |_|" + Color['white'] +
          " 2021 by " + Color['whiteBold'] + "Alvin Kuruvilla" + Color['white']+"\n")
    print("A Keylogger and mouse tracker for research purposes ")


def block_text(text):
    result = Figlet()
    print(colored.cyan(result.renderText(text)))


def clear_screen():
    if os.name == 'posix':
        _ = os.system('clear')
    else:
        # for windows
        _ = os.system('cls')

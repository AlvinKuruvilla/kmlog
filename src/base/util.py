from clint.textui import colored
from pyfiglet import Figlet
from colorama import Fore
import os


def welcome(text):
    result = Figlet()
    return colored.cyan(result.renderText(text))


def clear_screen():
    if os.name == 'posix':
        _ = os.system('clear')
    else:
        # for windows
        _ = os.system('cls')

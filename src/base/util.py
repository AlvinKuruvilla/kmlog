from clint.textui import colored
from pyfiglet import Figlet
from colorama import Fore


def welcome(text):
    result = Figlet()
    return colored.cyan(result.renderText(text))

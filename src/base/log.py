# Check this link for more details: https://stackoverflow.com/a/23964880
from colorlog import ColoredFormatter
import logging
from colorama import Fore, Style


class Logger():
    """A wrapper around python's native logging module to allow for prettier and more expressive logging output"""

    def __init__(self, name) -> None:
        LOG_LEVEL = logging.DEBUG
        LOGFORMAT = "  %(log_color)s%(levelname)-8s%(reset)s | %(log_color)s%(message)s%(reset)s"
        logging.root.setLevel(LOG_LEVEL)
        formatter = ColoredFormatter(LOGFORMAT)
        stream = logging.StreamHandler()
        stream.setLevel(LOG_LEVEL)
        stream.setFormatter(formatter)
        self.log = logging.getLogger(name)
        self.log.propagate = False
        self.log.setLevel(LOG_LEVEL)
        self.log.addHandler(stream)

    def km_info(self, msg: str) -> None:
        """Displays a information level message to the user"""
        self.log.info(msg)

    def km_warn(self, msg: str) -> None:
        """Displays a warning level message to the user """
        self.log.warn(msg)

    def km_error(self, msg: str) -> None:
        """Displays an error level message to the user """
        self.log.error(msg)

    def km_fatal(self, msg: str) -> None:
        """Displays a fatal level message to the user """
        self.log.critical(msg)

    def km_log_color(self, msg: str) -> None:
        """Display messages with a color (right now the only supported color is red)"""
        # FIXME: Right now this will only print red, we have to expand this to allow the user to pass in a color to the function
        print(Fore.RED + msg)
        print(Style.RESET_ALL)

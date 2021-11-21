# Check this link for more details: https://stackoverflow.com/a/23964880
from colorlog import ColoredFormatter
import logging


class Logger():
    def __init__(self) -> None:
        LOG_LEVEL = logging.DEBUG
        LOGFORMAT = "  %(log_color)s%(levelname)-8s%(reset)s | %(log_color)s%(message)s%(reset)s"
        logging.root.setLevel(LOG_LEVEL)
        formatter = ColoredFormatter(LOGFORMAT)
        stream = logging.StreamHandler()
        stream.setLevel(LOG_LEVEL)
        stream.setFormatter(formatter)
        self.log = logging.getLogger('pythonConfig')
        self.log.setLevel(LOG_LEVEL)
        self.log.addHandler(stream)

    def km_info(self, msg):
        self.log.info(msg)

    def km_warn(self, msg):
        self.log.warn(msg)

    def km_error(self, msg):
        self.log.error(msg)

    def km_fatal(self, msg):
        self.log.critical(msg)

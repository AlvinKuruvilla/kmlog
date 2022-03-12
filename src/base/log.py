# pylint: disable=R0201
# pylint: disable=C0301
# pylint: disable=C0114
# pylint: disable=W0622

# Copyright 2021 - 2022, Alvin Kuruvilla <alvineasokuruvilla@gmail.com>, Dr. Rajesh Kumar <Rajesh.Kumar@hofstra.edu>

# Use of this source code is governed by an MIT-style
# license that can be found in the LICENSE file or at
# https://opensource.org/licenses/MIT.

import sys
from functools import partialmethod
from loguru import logger


class Logger:
    """A wrapper around python's native logging module to allow for prettier and more expressive logging output"""

    def __init__(self) -> None:
        format = "<level>{level: <8}</level> | <level>{message}</level>"
        logger.remove()
        logger.add(sys.stderr, format=format)

    def km_info(self, msg: str) -> None:
        """Displays a information level message to the user"""
        logger.info(msg)

    def km_warn(self, msg: str) -> None:
        """Displays a warning level message to the user"""
        logger.warning(msg)

    def km_error(self, msg: str) -> None:
        """Displays an error level message to the user"""
        logger.error(msg)

    def km_fatal(self, msg: str) -> None:
        """Displays a fatal level message to the user"""
        logger.level("FATAL", no=33, color="<fg #FFA500>")
        logger.__class__.km_fatal = partialmethod(logger.__class__.log, "FATAL")
        logger.km_fatal(msg)

    def km_custom(self, msg: str, markup_tag: str, heading: str = "CUSTOM") -> None:
        """Display messages simply in red"""
        logger.level(heading, no=34, color=markup_tag)
        logger.__class__.km_custom = partialmethod(logger.__class__.log, heading)
        logger.km_custom(msg)

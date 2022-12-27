# Copyright 2021 - 2022, Alvin Kuruvilla <alvineasokuruvilla@gmail.com>, Dr. Rajesh Kumar <Rajesh.Kumar@hofstra.edu>

# Use of this source code is governed by an MIT-style
# license that can be found in the LICENSE file or at
# https://opensource.org/licenses/MIT.

# This is a small utility to help a user determine whether the environment
# variable name(s) they provide in their .env file conflict with existing
# variables

from base.log import *
from base.displayer import block_text
import os
from dotenv import dotenv_values

log = Logger()


def verify_env_values():
    block_text("ENV")
    c = []
    c2 = []
    config = dotenv_values(".env")
    for k in config.keys():
        c.append(k)
    if len(c) == 0:
        log.km_warn("No env file found")
        exit()
    current_env = os.environ
    for key, _ in current_env.items():
        c2.append(key)
    for check in c:
        if check in c2:
            log.km_fatal("Environment variable " + check + "is already used")
            exit()
    log.km_info("Environment variable verification successful")

# This is a small utility to help a user determine whether the environment
# variable name(s) they provide in their .env file conflict with existing
# variables
from base.log import *
import os
from dotenv import dotenv_values

log = Logger("env")


def verify_env_values():
    c = []
    c2 = []
    config = dotenv_values(".env")
    for k in config.keys():
        c.append(k)
    current_env = os.environ
    for key, _ in current_env.items():
        c2.append(key)
    for check in c:
        if check in c2:
            log.km_fatal("Environment variable " + check + "is already used")
            exit()
    log.km_info("Environment variable verification successful")

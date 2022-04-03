# Copyright 2022, Alvin Kuruvilla <alvineasokuruvilla@gmail.com>, Dr. Rajesh Kumar <Rajesh.Kumar@hofstra.edu>

# Use of this source code is governed by an MIT-style
# license that can be found in the LICENSE file or at
# https://opensource.org/licenses/MIT.

import sys
import os


def is_debug():
    gettrace = getattr(sys, "gettrace", None)
    if gettrace is None:
        print("No sys.gettrace")
        return
    elif gettrace():
        print("Debug build")
        return True
    else:
        print("Release build")
        return False


def make_logs_directory():
    if not os.path.isdir(os.path.join(os.getcwd(), "logs")):
        os.makedirs(os.path.join(os.getcwd(), "logs"))


def make_user_directory():
    if not os.path.isdir(os.path.join(os.getcwd(), "users")):
        os.makedirs(os.path.join(os.getcwd(), "users"))


USERS_DIR = os.path.join(os.getcwd(), "users")
LOGS_DIR = os.path.join(os.getcwd(), "logs")

# Copyright 2022, Alvin Kuruvilla <alvineasokuruvilla@gmail.com>, Dr. Rajesh Kumar <Rajesh.Kumar@hofstra.edu>

# Use of this source code is governed by an MIT-style
# license that can be found in the LICENSE file or at
# https://opensource.org/licenses/MIT.

import os

USERS_DIR = os.path.join(os.getcwd(), "users")
LOGS_DIR = os.path.join(os.getcwd(), "logs")


def make_logs_directory() -> None:
    if not os.path.isdir(os.path.join(os.getcwd(), "logs")):
        os.makedirs(os.path.join(os.getcwd(), "logs"))


def make_user_directory() -> None:
    if not os.path.isdir(os.path.join(os.getcwd(), "users")):
        os.makedirs(os.path.join(os.getcwd(), "users"))


def make_user_data_folder(user_id: str) -> None:
    path = os.path.join(LOGS_DIR, user_id)
    if not os.path.isdir(path):
        os.mkdir(path)

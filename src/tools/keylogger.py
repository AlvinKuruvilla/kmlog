# pylint: disable=C0412
# pylint: disable=C0301
# pylint: disable=E0401
# pylint: disable=C0114
# pylint: disable=W0511
# pylint: disable=C0103


# Copyright 2021 - 2022, Alvin Kuruvilla <alvineasokuruvilla@gmail.com>, Dr. Rajesh Kumar <Rajesh.Kumar@hofstra.edu>

# Use of this source code is governed by an MIT-style
# license that can be found in the LICENSE file or at
# https://opensource.org/licenses/MIT.

import os
import time
import sys
from dotenv import load_dotenv
from pynput.keyboard import Listener
from pynput import keyboard
from base.backends.yaml_driver import get_value_from_key
from base.user_ops.yml_ops import user_id_to_yaml_file_path
from base.backends.sql import SQLDriver, check_mysql_installed
from base.log import Logger
from base.displayer import (
    account_number_to_email_fragment,
    animated_marker,
    display_credentials,
    CredentialType,
)
from base.csv_writer import CSVWriter
from initalizer import LOGS_DIR
from pathlib import Path
from rich.traceback import install

install()
# TODO: Write csv headers to each generated file
SHUTDOWN = [
    {keyboard.Key.ctrl, keyboard.KeyCode(char="a")},
    {keyboard.Key.ctrl, keyboard.KeyCode(char="A")},
]
current = set()


def override_key(key) -> str:
    """Handles the fn key for macs"""
    if str(key) == "<179>" or str(key) == "<63>":
        return "Key.fn"
    if str(key) == "'\\\\'":
        return "'\\'"
    return str(key)


class Keylogger:
    """This keylogger stores the keys pressed by the user. It stores the keys pressed by the user to a named file, along with their names."""

    def __init__(self, _user_id: str) -> None:
        self.user_id = _user_id
        self.csv_writer = CSVWriter()
        self.buffer = []
        self.log_file_path = os.path.join(
            LOGS_DIR, self.user_id, self.user_id + ".log"
        )  # Create a global log file
        self.csv_writer.write_header(
            os.path.join(os.path.join(LOGS_DIR, self.user_id, self.user_id + ".csv"))
        )
        self.platform_count = 1

    def get_platform_count(self):
        return self.platform_count

    def update_platform_count(self):
        self.platform_count = self.platform_count + 1

    def check_platform_file(self, platform_type: CredentialType):
        if platform_type == CredentialType.FACEBOOK:
            f = Path(self.log_file_path)
            if f.is_fifo():
                return True
            new_file = open(self.log_file_path, "x")
            new_file.close()
            return None

    def __hotkey_shutdown(self):
        hlog = Logger()
        hlog.km_info("Hotkey activated, shutting down keylogger")
        self.graceful_shutdown()
        sys.exit(0)

    # We need this function to account for the edge case that there are stored key strings in the buffer when the keylogger is quit, so right before we quit we must write at the buffer and clear it
    def graceful_shutdown(self, platform_type=None) -> None:
        """This function only runs when a KeyboardInterupt exception is
        received. This function will then write everything stored in the key
        string buffer to the file and then clear the buffer before exiting

        Parameters
        ----------
        None

        Returns
        ----------
        None

        """
        if len(self.buffer) != 0:
            with open(self.log_file_path, "a", encoding="utf8") as _:
                for string in self.buffer:
                    self.buffer_write(
                        f"R,{override_key(string)}, {time.time()}", platform_type
                    )

    def buffer_write(self, to_add: str, platform_type=None) -> None:
        """This function writes to the buffer and if it exceeds the size it
        takes everything from the buffer to the file and clears it"""
        if (
            len(self.buffer) >= 80
        ):  # 80 is the number of letters people type in one line, in general
            if platform_type is None:
                with open(self.log_file_path, "a", encoding="utf8") as file:
                    for string in self.buffer:
                        file.write(string + "\n")
                self.buffer.clear()
            elif platform_type == CredentialType.FACEBOOK:
                _social_platform_path = os.path.join(
                    LOGS_DIR, self.user_id, "f" + self.user_id + ".log"
                )
                with open(_social_platform_path, "a", encoding="utf8") as file:
                    for string in self.buffer:
                        file.write(string + "\n")
                self.buffer.clear()
            elif platform_type == CredentialType.TWITTER:
                _social_platform_path = os.path.join(
                    LOGS_DIR, self.user_id, "t" + self.user_id + ".log"
                )
                with open(_social_platform_path, "a", encoding="utf8") as file:
                    for string in self.buffer:
                        file.write(string + "\n")
                self.buffer.clear()
            elif platform_type == CredentialType.INSTAGRAM:
                _social_platform_path = os.path.join(
                    LOGS_DIR, self.user_id, "i" + self.user_id + ".log"
                )
                with open(_social_platform_path, "a", encoding="utf8") as file:
                    for string in self.buffer:
                        file.write(string + "\n")
                self.buffer.clear()
        else:
            self.buffer.append(to_add)

    def get_and_write_user_info(self, platform_type=None) -> None:
        """Query the database for the first and last name associated with a
        particular user ID and write those to the log file with the that
        particular user ID in the name"""
        if check_mysql_installed():
            load_dotenv()
            driver = SQLDriver()
            driver.try_connect()
            cursor = driver.query(
                "SELECT first_name, last_name FROM "
                + os.getenv("TABLE")
                + " WHERE user_id = "
                + str(self.user_id),
                (),
            )
            first, last = cursor.fetchone()

            if first is None:
                first = "Unknown"
            if last is None:
                last = "Unknown"
            if platform_type is None:
                with open(self.log_file_path, "a", encoding="utf8") as file:
                    file.write("\n" + first + " " + last + "\n")
                    file.write("**********************************" + "\n")
            elif platform_type == CredentialType.FACEBOOK:
                _social_platform_path = os.path.join(
                    LOGS_DIR, self.user_id, "f" + self.user_id + ".log"
                )
                with open(_social_platform_path, "a", encoding="utf8") as file:
                    file.write("\n" + first + " " + last + "\n")
                    file.write(platform_type + "\n")
                    file.write("**********************************" + "\n")
            elif platform_type == CredentialType.TWITTER:
                _social_platform_path = os.path.join(
                    LOGS_DIR, self.user_id, "t" + self.user_id + ".log"
                )
                with open(_social_platform_path, "a", encoding="utf8") as file:
                    file.write("\n" + first + " " + last + "\n")
                    file.write(platform_type + "\n")
                    file.write("**********************************" + "\n")
            elif platform_type == CredentialType.INSTAGRAM:
                _social_platform_path = os.path.join(
                    LOGS_DIR, self.user_id, "i" + self.user_id + ".log"
                )
                with open(_social_platform_path, "a", encoding="utf8") as file:
                    file.write("\n" + first + " " + last + "\n")
                    file.write(platform_type + "\n")
                    file.write("**********************************" + "\n")

        else:
            path = user_id_to_yaml_file_path(self.user_id)
            first = get_value_from_key(path, "first_name")
            last = get_value_from_key(path, "last_name")
            if first is None:
                first = "Unknown"
            if last is None:
                last = "Unknown"
            if platform_type is None:
                with open(self.log_file_path, "a", encoding="utf8") as file:
                    file.write("\n" + first + " " + last + "\n")
                    file.write("**********************************" + "\n")
            elif platform_type == CredentialType.FACEBOOK:
                _social_platform_path = os.path.join(
                    LOGS_DIR, self.user_id, "f" + self.user_id + ".log"
                )
                with open(_social_platform_path, "a", encoding="utf8") as file:
                    file.write("\n" + first + " " + last + "\n")
                    file.write(platform_type.to_str() + "\n")
                    file.write("**********************************" + "\n")
            elif platform_type == CredentialType.TWITTER:
                _social_platform_path = os.path.join(
                    LOGS_DIR, self.user_id, "t" + self.user_id + ".log"
                )
                with open(_social_platform_path, "a", encoding="utf8") as file:
                    file.write("\n" + first + " " + last + "\n")
                    file.write(platform_type.to_str() + "\n")
                    file.write("**********************************" + "\n")
            elif platform_type == CredentialType.INSTAGRAM:
                _social_platform_path = os.path.join(
                    LOGS_DIR, self.user_id, "i" + self.user_id + ".log"
                )
                with open(_social_platform_path, "a", encoding="utf8") as file:
                    file.write("\n" + first + " " + last + "\n")
                    file.write(platform_type.to_str() + "\n")
                    file.write("**********************************" + "\n")

    def start_recording(self, platform_type=None, account_number: int = None) -> None:
        """This function reccords all the key presses to the file and the
        buffer. See also :func: `~tools.Keylogger.buffer_write`"""
        try:
            # input("Check platform")
            # print(platform_type)
            self.get_and_write_user_info()
            self.get_and_write_user_info(platform_type)
            klog = Logger()
            animated_marker("Initializing keylogger....")
            if self.get_platform_count() == 1:
                klog.km_custom(
                    "WARNING! Anything you will type shall be recorded until you terminate this app manually!",
                    "<red>",
                    "KEYLOGGER",
                )
            elif self.get_platform_count() > 1:
                print(
                    "\033[0;31m KEYLOGGER | WARNING! Anything you will type shall be recorded until you terminate this app manually\033[00m"
                )

            def on_press(key) -> None:
                # print(platform_type)
                # input("Check platform")
                if platform_type is None or account_number is None:
                    self.buffer_write(f"P,{override_key(key)}, {time.time()}")
                    data = ["P", override_key(key), time.time()]
                    self.csv_writer.write_data_to_csv(
                        os.path.join(LOGS_DIR, self.user_id, self.user_id + ".csv"),
                        data,
                    )

                elif platform_type == CredentialType.FACEBOOK:
                    # input("Hit here - Facebook")
                    account_email_fragment = account_number_to_email_fragment(
                        account_number
                    )
                    _social_platform_path = os.path.join(
                        LOGS_DIR,
                        self.user_id,
                        "f_" + self.user_id + "_" + account_email_fragment + ".csv",
                    )
                    self.buffer_write(
                        f"P,{override_key(key)}, {time.time()}", platform_type
                    )
                    data = ["P", override_key(key), time.time()]
                    self.csv_writer.write_data_to_csv(
                        _social_platform_path,
                        data,
                    )
                elif platform_type == CredentialType.TWITTER:
                    # input("Hit here - Twitter")
                    account_email_fragment = account_number_to_email_fragment(
                        account_number
                    )
                    _social_platform_path = os.path.join(
                        LOGS_DIR,
                        self.user_id,
                        "t_" + self.user_id + "_" + account_email_fragment + ".csv",
                    )
                    self.buffer_write(
                        f"P,{override_key(key)}, {time.time()}", platform_type
                    )
                    data = ["P", override_key(key), time.time()]
                    self.csv_writer.write_data_to_csv(
                        _social_platform_path,
                        data,
                    )
                elif platform_type == CredentialType.INSTAGRAM:
                    # input("Hit here - Instagram")
                    account_email_fragment = account_number_to_email_fragment(
                        account_number
                    )
                    _social_platform_path = os.path.join(
                        LOGS_DIR,
                        self.user_id,
                        "i_" + self.user_id + "_" + account_email_fragment + ".csv",
                    )
                    self.buffer_write(
                        f"P,{override_key(key)}, {time.time()}", platform_type
                    )
                    data = ["P", override_key(key), time.time()]
                    self.csv_writer.write_data_to_csv(
                        _social_platform_path,
                        data,
                    )
                # See hotkey todo above
                # if any([key in COMBO for COMBO in SHUTDOWN]):
                #     current.add(key)
                #     if any(all(k in current for k in COMBO) for COMBO in SHUTDOWN):
                # _        self.__hotkey_shutdown()

            def on_release(key) -> None:
                # print(platform_type)
                # input("Check platform")

                if platform_type is None or account_number is None:
                    self.buffer_write(f"R,{override_key(key)}, {time.time()}")
                    data = ["R", override_key(key), time.time()]
                    self.csv_writer.write_data_to_csv(
                        os.path.join(LOGS_DIR, self.user_id, self.user_id + ".csv"),
                        data,
                    )
                elif platform_type == CredentialType.FACEBOOK:
                    account_email_fragment = account_number_to_email_fragment(
                        account_number
                    )
                    _social_platform_path = os.path.join(
                        LOGS_DIR,
                        self.user_id,
                        "f_" + self.user_id + "_" + account_email_fragment + ".csv",
                    )
                    self.buffer_write(
                        f"R,{override_key(key)}, {time.time()}", platform_type
                    )
                    data = ["R", override_key(key), time.time()]
                    self.csv_writer.write_data_to_csv(
                        _social_platform_path,
                        data,
                    )
                elif platform_type == CredentialType.TWITTER:
                    # input("Hit here - Twitter")
                    account_email_fragment = account_number_to_email_fragment(
                        account_number
                    )
                    _social_platform_path = os.path.join(
                        LOGS_DIR,
                        self.user_id,
                        "t_" + self.user_id + "_" + account_email_fragment + ".csv",
                    )
                    self.buffer_write(
                        f"R,{override_key(key)}, {time.time()}", platform_type
                    )
                    data = ["R", override_key(key), time.time()]
                    self.csv_writer.write_data_to_csv(
                        _social_platform_path,
                        data,
                    )
                elif platform_type == CredentialType.INSTAGRAM:
                    # input("Hit here - Instagram")
                    account_email_fragment = account_number_to_email_fragment(
                        account_number
                    )
                    _social_platform_path = os.path.join(
                        LOGS_DIR,
                        self.user_id,
                        "i_" + self.user_id + "_" + account_email_fragment + ".csv",
                    )
                    self.buffer_write(
                        f"R,{override_key(key)}, {time.time()}", platform_type
                    )
                    data = ["R", override_key(key), time.time()]
                    self.csv_writer.write_data_to_csv(
                        _social_platform_path,
                        data,
                    )

                # See hotkey todo above
                # if any([key in COMBO for COMBO in SHUTDOWN]):
                #     current.remove(key)

            with Listener(on_press=on_press, on_release=on_release) as listener:
                listener.join()
        except KeyboardInterrupt:
            self.graceful_shutdown()
            if platform_type is None:
                self.__hotkey_shutdown()
            if self.get_platform_count() == 1:
                print("Please sign in to Instagram using the following credentials:")
                display_credentials(CredentialType.INSTAGRAM)
                self.update_platform_count()
                self.start_recording(CredentialType.INSTAGRAM)
            elif self.get_platform_count() == 2:
                print("Please sign in to Twitter using the following credentials:")
                display_credentials(CredentialType.TWITTER)
                self.update_platform_count()
                self.start_recording(CredentialType.TWITTER)
            elif self.get_platform_count() > 2:
                self.__hotkey_shutdown()


if __name__ == "__main__":

    user_id = input("Enter the user id to start data collection:")
    NewUser = Keylogger(user_id)
    NewUser.start_recording()

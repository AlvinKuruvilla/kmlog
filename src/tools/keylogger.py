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
from base.backends.sql import SQLDriver, check_mysql_installed_and_env_configured_correctly
from base.log import Logger
from base.displayer import (
    account_number_to_email_fragment,
    animated_marker,
    display_credentials,
    CredentialType,
    windows_only_platform_menu,
)
from base.csv_writer import CSVWriter
from initializer import LOGS_DIR
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
        # HOT FIX: use the timestamp to distinguish between user sessions and automate session ID assignment
        #           For example, session id 1,2,3 have the same filename but with earlier timestamps
        self.timestamp = time.time_ns()
        self.log_file_path = os.path.join(
            LOGS_DIR, self.user_id, self.user_id + "_" + str(self.timestamp) + ".log"
        )  # Create a global log file
        self.csv_writer.write_header(
            os.path.join(
                os.path.join(
                    LOGS_DIR, self.user_id, self.user_id + "_" + str(self.timestamp) + ".csv"
                )
            )
        )
        self.platform_count = 1
        self.account_number = 1

    def get_platform_count(self):
        return self.platform_count

    def set_account_number(self, account_number: int):
        self.account_number = account_number

    def get_account_number(self):
        return self.account_number

    def update_platform_count(self):
        self.platform_count = self.platform_count + 1

    def __hotkey_shutdown(self):
        hlog = Logger()
        hlog.km_info("Hotkey activated, shutting down keylogger")
        self.graceful_shutdown()
        sys.exit(0)

    # We need this function to account for the edge case that there are stored key strings in the buffer when the keylogger is quit, so right before we quit we must write at the buffer and clear it
    def graceful_shutdown(self) -> None:
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
                    self.buffer_write(f"R,{override_key(string)}, {time.time_ns()}")

    def buffer_write(self, to_add: str) -> None:
        """This function writes to the buffer and if it exceeds the size it
        takes everything from the buffer to the file and clears it"""
        # 80 is the number of letters people type in one line, in general
        if len(self.buffer) >= 80:
            with open(self.log_file_path, "a", encoding="utf8") as file:
                for string in self.buffer:
                    file.write(string + "\n")
            self.buffer.clear()
        else:
            self.buffer.append(to_add)

    def get_and_write_user_info(self) -> None:
        """Query the database for the first and last name associated with a
        particular user ID and write those to the log file with the that
        particular user ID in the name"""
        if check_mysql_installed_and_env_configured_correctly():
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
            with open(self.log_file_path, "a", encoding="utf8") as file:
                file.write("\n" + first + " " + last + "\n")
                file.write("**********************************" + "\n")
        else:
            path = user_id_to_yaml_file_path(self.user_id)
            first = get_value_from_key(path, "first_name")
            last = get_value_from_key(path, "last_name")
            if first is None:
                first = "Unknown"
            if last is None:
                last = "Unknown"
            with open(self.log_file_path, "a", encoding="utf8") as file:
                file.write("\n" + first + " " + last + "\n")
                file.write("**********************************" + "\n")

    def start_recording(self, platform_type=None, account_number: int = None) -> None:
        """This function reccords all the key presses to the file and the
        buffer. See also :func: `~tools.Keylogger.buffer_write`"""
        print("Started the recording function")
        try:
            # input("Check platform")
            # print(platform_type)
            self.get_and_write_user_info()
            klog = Logger()
            # animated_marker("Initializing keylogger....")
            if self.get_platform_count() == 1:
                klog.km_warn(
                    "WARNING! Anything you will type shall be recorded until you terminate this app manually!"
                )
            elif self.get_platform_count() > 1:
                print(
                    "\033[0;31m KEYLOGGER | WARNING! Anything you will type shall be recorded until you terminate this app manually\033[00m"
                )

            def on_press(key) -> None:
                # print(platform_type)
                # input("Check platform")
                if platform_type is None or account_number is None:
                    self.buffer_write(f"P,{override_key(key)}, {time.time_ns()}")
                    data = ["P", override_key(key), time.time_ns()]
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
                    self.buffer_write(f"P,{override_key(key)}, {time.time_ns()}")
                    data = ["P", override_key(key), time.time_ns()]
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
                    self.buffer_write(f"P,{override_key(key)}, {time.time_ns()}")
                    data = ["P", override_key(key), time.time_ns()]
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
                    self.buffer_write(f"P,{override_key(key)}, {time.time_ns()}")
                    data = ["P", override_key(key), time.time_ns()]
                    self.csv_writer.write_data_to_csv(
                        _social_platform_path,
                        data,
                    )

            def on_release(key) -> None:
                # print(platform_type)
                # input("Check platform")

                if platform_type is None or account_number is None:
                    self.buffer_write(f"R,{override_key(key)}, {time.time_ns()}")
                    data = ["R", override_key(key), time.time_ns()]
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
                    self.buffer_write(f"R,{override_key(key)}, {time.time_ns()}")
                    data = ["R", override_key(key), time.time_ns()]
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
                    self.buffer_write(f"R,{override_key(key)}, {time.time_ns()}")
                    data = ["R", override_key(key), time.time_ns()]
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
                    self.buffer_write(f"R,{override_key(key)}, {time.time_ns()}")
                    data = ["R", override_key(key), time.time_ns()]
                    self.csv_writer.write_data_to_csv(
                        _social_platform_path,
                        data,
                    )

                # See hotkey todo above
                # if any([key in COMBO for COMBO in SHUTDOWN]):
                #     current.remove(key)
            print("Before join")
            with Listener(on_press=on_press, on_release=on_release) as listener:
                print("Inside join")
                listener.join()
            print("After join")
        except KeyboardInterrupt:
            self.graceful_shutdown()
            if platform_type is None:
                self.__hotkey_shutdown()
            if self.get_platform_count() == 1:
                print("Please sign in to Instagram using the following credentials:")
                display_credentials(CredentialType.INSTAGRAM, self.get_account_number())
                self.update_platform_count()
                self.start_recording(
                    CredentialType.INSTAGRAM, self.get_account_number()
                )
            elif self.get_platform_count() == 2:
                print("Please sign in to Twitter using the following credentials:")
                display_credentials(CredentialType.TWITTER, self.get_account_number())
                self.update_platform_count()
                self.start_recording(CredentialType.TWITTER, self.get_account_number())
            elif self.get_platform_count() > 2:
                self.__hotkey_shutdown()
        except KeyError:
            print("Probably hit the weird KeyError: 'CGEventKeyboardGetUnicodeString', error that started showing up recently. Could it be because of some update to one of our dependencies like pynput")
            pass
        except Exception as e:
            print("Hitting except:", e)
    def windows_start_recording(self, account_number: int = None) -> None:
        """This function reccords all the key presses to the file and the
        buffer. See also :func: `~tools.Keylogger.buffer_write`"""
        # XXX: When the user is done they must physically exit the terminal
        self.get_and_write_user_info()
        klog = Logger()
        choice = windows_only_platform_menu()
        while True:
            if choice in (0, 1, 2):
                break
            else:
                klog.km_error("Invalid selection: choose 1, 2, 3")
                choice = windows_only_platform_menu()
                continue
        print(choice)
        if choice == 0:

            def on_press(key) -> None:
                # input("Hit here - Facebook")
                account_email_fragment = account_number_to_email_fragment(
                    account_number
                )
                _social_platform_path = os.path.join(
                    LOGS_DIR,
                    self.user_id,
                    "f_" + self.user_id + "_" + account_email_fragment + ".csv",
                )
                self.buffer_write(f"P,{override_key(key)}, {time.time_ns()}")
                data = ["P", override_key(key), time.time_ns()]
                self.csv_writer.write_data_to_csv(
                    _social_platform_path,
                    data,
                )

            def on_release(key) -> None:
                account_email_fragment = account_number_to_email_fragment(
                    account_number
                )
                _social_platform_path = os.path.join(
                    LOGS_DIR,
                    self.user_id,
                    "f_" + self.user_id + "_" + account_email_fragment + ".csv",
                )
                self.buffer_write(f"R,{override_key(key)}, {time.time_ns()}")
                data = ["R", override_key(key), time.time_ns()]
                self.csv_writer.write_data_to_csv(
                    _social_platform_path,
                    data,
                )

            with Listener(on_press=on_press, on_release=on_release) as listener:
                listener.join()
        if choice == 1:

            def on_press(key):
                account_email_fragment = account_number_to_email_fragment(
                    account_number
                )
                _social_platform_path = os.path.join(
                    LOGS_DIR,
                    self.user_id,
                    "i_" + self.user_id + "_" + account_email_fragment + ".csv",
                )
                self.buffer_write(f"P,{override_key(key)}, {time.time_ns()}")
                data = ["P", override_key(key), time.time_ns()]
                self.csv_writer.write_data_to_csv(
                    _social_platform_path,
                    data,
                )

            def on_release(key):
                account_email_fragment = account_number_to_email_fragment(
                    account_number
                )
                _social_platform_path = os.path.join(
                    LOGS_DIR,
                    self.user_id,
                    "i_" + self.user_id + "_" + account_email_fragment + ".csv",
                )
                self.buffer_write(f"R,{override_key(key)}, {time.time_ns()}")
                data = ["R", override_key(key), time.time_ns()]
                self.csv_writer.write_data_to_csv(
                    _social_platform_path,
                    data,
                )

            with Listener(on_press=on_press, on_release=on_release) as listener:
                listener.join()

        if choice == 2:

            def on_press(key):
                account_email_fragment = account_number_to_email_fragment(
                    account_number
                )
                _social_platform_path = os.path.join(
                    LOGS_DIR,
                    self.user_id,
                    "t_" + self.user_id + "_" + account_email_fragment + ".csv",
                )
                self.buffer_write(f"P,{override_key(key)}, {time.time_ns()}")
                data = ["P", override_key(key), time.time_ns()]
                self.csv_writer.write_data_to_csv(
                    _social_platform_path,
                    data,
                )

            def on_release(key):
                account_email_fragment = account_number_to_email_fragment(
                    account_number
                )
                _social_platform_path = os.path.join(
                    LOGS_DIR,
                    self.user_id,
                    "t_" + self.user_id + "_" + account_email_fragment + ".csv",
                )
                self.buffer_write(f"R,{override_key(key)}, {time.time_ns()}")
                data = ["R", override_key(key), time.time_ns()]
                self.csv_writer.write_data_to_csv(
                    _social_platform_path,
                    data,
                )

            with Listener(on_press=on_press, on_release=on_release) as listener:
                listener.join()


if __name__ == "__main__":
    user_id = input("Enter the user id to start data collection:")
    NewUser = Keylogger(user_id)
    NewUser.start_recording()

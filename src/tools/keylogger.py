# TODO: Simplify file writing but just having columns P/R, Key, Time
# TODO: Maybe we should have a keyboard shortcut to stop program execution rather than ctrl + c?
# NOTE: Eventually we may also want to have the shutdown method remove the interupt shortcut used to terminate the program and remove them from the file.... we may also want to extend this to personally identifiable information eventually
from pynput.keyboard import Listener
import time
from .util import override_key
from base.sql import SQLDriver
from base.log import Logger
from dotenv import load_dotenv
import os


class Keylogger:
    """This keylogger stores the keys pressed by the user. It stores the keys pressed by the user to a named file, along with their names. """

    def __init__(self, user_id: str) -> None:
        self.user_id = user_id
        self.buffer = []
    # We need this function to account for the edge case that there are stored key strings in the buffer when the keylogger is quit, so right before we quit we must write at the buffer and clear it

    def graceful_shutdown(self) -> None:
        """This function only runs when a KeyboardInterupt exception is
        received. This function will then write everything stored in the key
        string buffer to the file and then clear the buffer before exiting"""
        if len(self.buffer) != 0:
            with open("src/logs/"+self.user_id+".log", "a") as file:
                for string in self.buffer:
                    self.buffer_write(
                        f"R,{override_key(string)}, {time.time()}")

    def buffer_write(self, to_add: str) -> None:
        """This function writes to the buffer and if it exceeds the size it
        takes everything from the buffer to the file and clears it"""
        if len(self.buffer) >= 80:  # 80 is the number of letters people type in one line, in general
            with open("src/logs/"+self.user_id+".log", "a") as file:
                for string in self.buffer:
                    file.write(string)
            self.buffer.clear()
        else:
            self.buffer.append(to_add)

    def get_and_write_user_info(self) -> None:
        """Query the database for the first and last name associated with a
        particular user ID and write those to the log file with the that
        particular user ID in the name"""
        load_dotenv()
        driver = SQLDriver()
        driver.try_connect()
        cursor = driver.query("SELECT first_name, last_name FROM " +
                              os.getenv("TABLE") + " WHERE user_id = " + str(self.user_id), ())
        first, last = cursor.fetchone()
        if first == None:
            first = "Unknown"
        if last == None:
            last = "Unknown"
        with open("src/logs/"+self.user_id+".log", "a") as file:
            file.write("\n"+first + " " + last + "\n")
            file.write("**********************************" + "\n")

    def start_recording(self) -> None:
        """This function reccords all the key presses to the file and the
        buffer. See also :func: `~tools.Keylogger.buffer_write`"""
        try:
            self.get_and_write_user_info()
            klog = Logger("klog")
            klog.km_info("Initializing keylogger....")
            klog.km_log_color(
                "WARNING! Anything you will type shall be recorded until you terminate this app manually!")

            def on_press(key) -> None:
                self.buffer_write(f"P,{override_key(key)}, {time.time()}")

            def on_release(key) -> None:
                self.buffer_write(f"R,{override_key(key)}, {time.time()}")
            with Listener(on_press=on_press, on_release=on_release) as listener:
                listener.join()
        except KeyboardInterrupt:
            self.graceful_shutdown()


if __name__ == "__main__":

    user_id = input("Enter the user id to start data collection:")
    NewUser = Keylogger(user_id)
    NewUser.start_recording()

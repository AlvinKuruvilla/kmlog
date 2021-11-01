# TODO: Simplify file writing but just haaving columns P/R, Key, Time
# Todo: write to file after buffer exceeds certain capacity
# TODO: Overide unrecognized keycodes with readable text versions

from pynput.keyboard import Listener
import time

from util import override_key


def get_and_write_user_info():
    first = input("Please enter your first name: ")
    last = input("Please enter your last name: ")
    file = open("keylog.log", "a")
    file.write(first + " " + last + "\n")
    file.write("**********************************" + "\n")
    file.close()


class KeyLogger():
    get_and_write_user_info()
    print("Initalizing keylogger")

    def on_press(key):
        file = open("keylog.log", "a")
        file.write("Pressed key: " + override_key(key) +
                   " at time " + str(time.time()) + "\n")
        file.close()

    def on_release(key):
        file = open("keylog.log", "a")
        file.write("Released key: " + override_key(key) +
                   " at time " + str(time.time()) + "\n")
        file.close()

    with Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()


if __name__ == "__main__":
    KeyLogger()

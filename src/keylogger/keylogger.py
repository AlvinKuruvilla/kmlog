# TODO: Simplify file writing but just having columns P/R, Key, Time
# TODO: Maybe we should have a keyboard shortcut to stop program execution rather than ctrl + c?

# NOTE: Eventually we may also want to have the shutdown method remove the interupt shortcut used to terminate the program and remove them from the file.... we may also want to extend this to personally identifiable information eventually

from pynput.keyboard import Listener
import time

from util import override_key

buffer = []


def graceful_shutdown():
    global buffer
    if len(buffer) != 0:
        file = open("keylog.log", "a")
        for string in buffer:
            file.write(string)
        buffer.clear()
        file.close()


def buffer_write(to_add: str):
    global buffer
    if len(buffer) >= 10:
        file = open("keylog.log", "a")
        for string in buffer:
            print("Buffer length:", len(buffer))
            file.write(string)
        file.close()
        buffer.clear()
    buffer.append(to_add)


def get_and_write_user_info():
    first = input("Please enter your first name: ")
    last = input("Please enter your last name: ")
    file = open("keylog.log", "a")
    file.write(first + " " + last + "\n")
    file.write("**********************************" + "\n")
    file.close()


try:
    class KeyLogger():
        get_and_write_user_info()
        print("Initalizing keylogger")

        def on_press(key):
            buffer_write("Pressed key: " + override_key(key) +
                         " at time " + str(time.time()) + "\n")

        def on_release(key):
            buffer_write("Released key: " + override_key(key) +
                         " at time " + str(time.time()) + "\n")

        with Listener(on_press=on_press, on_release=on_release) as listener:
            listener.join()
except KeyboardInterrupt:
    graceful_shutdown()

if __name__ == "__main__":
    KeyLogger()

# TODO: Simplify file writing but just having columns P/R, Key, Time
# TODO: Maybe we should have a keyboard shortcut to stop program execution rather than ctrl + c?
# NOTE: Eventually we may also want to have the shutdown method remove the interupt shortcut used to terminate the program and remove them from the file.... we may also want to extend this to personally identifiable information eventually
from pynput.keyboard import Listener
import time
from util import override_key

class LoggingUserActivities:
  def __init__(self, user_id):
      self.user_id = user_id
      #Search in the database and if user_id is found, populate all the fields
      #Otherwise prompt the user to enter these details one by one and the insert into the database.
      gender = input("Gender (enter m for male, f for female, o: other): ")
      self.gender = gender
      handedness = input("dominant hand: (enter l for left, r for right): ")
      self.handedness = handedness

      age = input("age (whole number): ")
      self.age = age

      education_level= input("education level?: (b for bachelor, m for master, d for doctor): ")
      self.education_level = education_level

      social_platform = input("what social media platform you are going to use, f for facebook, i for insta, t for twitter?")
      self.social_platform = social_platform
      self.buffer = []

  def graceful_shutdown(self):
      if len(self.buffer) != 0:
          file = open(self.user_id+".log", "a")
          for string in self.buffer:
            file.write(string)
            self.buffer.clear()
            file.close()


  def buffer_write(self, to_add: str):
    if len(self.buffer) >= 80: # 80 is the number of letters people type in one line, in general
        file = open(self.user_id+".log", "a")
        for string in self.buffer:
            # print("Buffer length:", len(self.buffer))
            file.write(string)
        file.close()
        self.buffer.clear()
    self.buffer.append(to_add)


  def get_and_write_user_info(self):
    first = input("Please enter your first name: ")
    last = input("Please enter your last name: ")
    file = open(self.user_id+".log", "a")
    file.write(first + " " + last + "\n")
    file.write("**********************************" + "\n")
    file.close()

  def start_recording(self):
    try:
        self.get_and_write_user_info()
        print("Initializing keylogger....")
        print("WARNING! Anything you will type shall be recorded until you terminate this app manually!")
        def on_press(key):
            self.buffer_write(f"P,{override_key(key)}, {time.time()}")

        def on_release(key):
            self.buffer_write(f"R,{override_key(key)}, {time.time()}")
        with Listener(on_press=on_press, on_release=on_release) as listener:
            listener.join()
    except KeyboardInterrupt:
        self.graceful_shutdown()

class create_database:
    # this class would create a database with a table that can be queried using a unique user id
    # the table will mainly consists of user details
    # during enrollment i.e. the first time the following details of the participant shall be collected
    # The following participation would just require the user user to enter their user_id
    # The user_id shall be used to fetch and display the details of the user
    pass
if __name__ == "__main__":

    # Create the database and table for the first time
    # Find resources on how to create and manage a database in Python
    # This resource could be helpful https://gist.github.com/Xeoncross/494947640a7dcfe8d91496988a5bf325
    user_id = input("Enter the user id to start data collection:")
    NewUser = LoggingUserActivities(user_id)
    NewUser.start_recording()

import os
from base.sql import *
from base.user import add_user
from base.util import *
from tools.keylogger import *
from dotenv import load_dotenv

if __name__ == '__main__':
    os.system("clear")
    print(welcome("KMLogger"))
    load_dotenv()
    print("A Keylogger and mouse tracker for research purposes")
    print("\nChoose service you want to use : ")
    print("""
        1: Start KMLogger
        2:  Exit
        """)
    choice = int(input("Enter a choice: "))
    if choice == 1:
        driver = SQLDriver()
        driver.try_connect()
        user_id = input("Enter your user_id: ")
        # NOTE: To understand this api look in the mysql package's cursor.py file...According to that api the params argument as they have named it defaults to an empty tuple
        # Step through of the reasoning behind the lines below:
        #   - Make the driver query the table for the user_id table
        #   - Fetch and store the result of that call
        #   - Iterate through the results to see if any match the id the user entered
        #   - If that id is not in the table create a new user, add them to the table and start the keylogger
        #   - If they are in the table, let them know that, and then start the keylogger

        cursor = driver.query("SELECT user_id FROM " + os.getenv("TABLE"), ())
        # NOTE: Here it should be okay to use fetchone rather fetchmany or fetchall because we are assuming that each user_id will be unique... so there will only ever be at most 1 row in the result
        result = cursor.fetchone()
        if user_id in result:
            print("User ID: " + user_id + " found")
            km = Keylogger(user_id)
            km.start_recording()
        else:

            print("ID not found")
            km = Keylogger(user_id)
            add_user(user_id)
            km.start_recording()

    if choice == 2:
        exit()
    # TODO: Prompt for user input again until valid input is given

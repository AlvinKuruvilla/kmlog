import os
from base.sql import SQLDriver
from base.user import add_user, display_profile
from base.util import *
from base.log import Logger
from tools.keylogger import *
from dotenv import load_dotenv

if __name__ == '__main__':
    log = Logger("cli")
    clear_screen()
    banner("KMLogger")
    load_dotenv()
    print("\nChoose service you want to use : ")
    print("""
        1: Start KMLogger
        2:  Exit
        """)
    # clear_screen()
    while True:
        choice = int(input("Enter a choice: "))
        if choice == 1 or choice == 2:
            break
        else:
            log.km_error("Invalid selection: choose 1 or 2")
            continue
    if choice == 1:
        clear_screen()
        block_text("Keylogger")
        driver = SQLDriver()
        driver.try_connect()
        user_id = input("""
        Enter your user_id: """)
        # NOTE: To understand this api look in the mysql package's cursor.py
        # file...According to that api the params argument as they have named it
        # defaults to an empty tuple
        # Step through of the reasoning behind the lines below:
        #   - Make the driver query the table for the user_id table
        #   - Fetch and store the result of that call
        #   - Iterate through the results to see if any match the id the user
        #     entered
        #   - If that id is not in the table create a new user, add them to the
        #     table and start the keylogger
        #   - If they are in the table, let them know that, and then start the
        #     keylogger

        cursor = driver.query("SELECT user_id FROM " + os.getenv("TABLE"), ())
        # NOTE: Here it should be okay to use fetchone rather fetchmany or fetchall because we are assuming that each user_id will be unique, so there will only ever be at most 1 row in the result
        result = cursor.fetchone()
        if user_id in result:
            log.km_info("User ID: " + user_id + " found")
            display_profile(user_id)
            info_correct = input("Is all of this information correct? y/n: ")
            if(info_correct.lower() == "y" or info_correct.lower() == "yes"):
                km = Keylogger(user_id)
                km.start_recording()
            elif info_correct.lower() == "n" or info_correct.lower() == "no":
                log.km_fatal(
                    "Please let the researchers know that this information is incorrect and it will be addressed")
            else:
                log.km_fatal("Invalid Input")
        else:
            log.km_warn("ID not found")
            km = Keylogger(user_id)
            add_user(user_id)
            km.start_recording()

    if choice == 2:
        log.km_info("Exiting KMLogger")
        exit()

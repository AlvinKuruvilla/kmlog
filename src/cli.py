import os
from base.backends.sql import SQLDriver, check_mysql_installed
from base.backends.yaml_driver import YAMLDriver
from base.user_ops.sql_ops import add_user_to_db, display_profile_from_db
from base.user_ops.yml_ops import *
from base.util import *
from base.log import Logger
from tools.keylogger import *
from tools.env_verifier import verify_env_values
from dotenv import load_dotenv

if __name__ == '__main__':
    log = Logger("cli")
    clear_screen()
    if(check_mysql_installed() == True):
        verify_env_values()
        input("Press any key to continue ")
        clear_screen()
    banner("KMLogger")
    load_dotenv()
    print("\nChoose service you want to use : ")
    print("""
        1:  Start KMLogger
        2:  Exit
        """)
    while True:
        choice = int(input(km_prompt("Enter a choice: ")))
        if choice == 1 or choice == 2:
            break
        else:
            log.km_error("Invalid selection: choose 1 or 2")
            continue
    if choice == 1:
        clear_screen()
        block_text("Keylogger")
        if(check_mysql_installed() == True):
            driver = SQLDriver()
            driver.try_connect()
        else:
            ydriver = YAMLDriver()
        user_id = input(km_prompt("Enter your user_id: "))
        # Step through of the reasoning behind the lines below:
        #   - Make the driver query the table for the user_id table
        #   - Fetch and store the result of that call
        #   - Iterate through the results to see if any match the id the user
        #     entered
        #   - If that id is not in the table create a new user, add them to the
        #     table and start the keylogger
        #   - If they are in the table, let them know that, and then start the
        #     keylogger
        if(check_mysql_installed() == True):
            # NOTE: To understand this api look in the mysql package's cursor.py
            # file...According to that api the params argument as they have named it
            # defaults to an empty tuple
            cursor = driver.query(
                "SELECT user_id FROM " + os.getenv("TABLE"), ())
            # NOTE: Here it should be okay to use fetchone rather fetchmany or fetchall because we are assuming that each user_id will be unique, so there will only ever be at most 1 row in the result
            result = cursor.fetchone()
            if result is not None and user_id in result:
                log.km_info("User ID: " + user_id + " found")
                display_profile_from_db(user_id)
                info_correct = input(
                    "Is all of this information correct? y/n: ")
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
                add_user_to_db(user_id)
                km.start_recording()
        else:
            # The yaml version of the above code
            comp = ydriver.get_all_associated_values("user_id")
            if user_id in comp:
                log.km_info("User ID: " + user_id + " found")
                ydriver.print_as_table(
                    user_id_to_yaml_file_path(user_id))
                # TODO: Add a loop for input validation
                info_correct = input(
                    "Is all of this information correct? y/n: ")
                if(info_correct.lower() == "y" or info_correct.lower() == "yes"):
                    km = Keylogger(user_id)
                    km.start_recording()
                elif info_correct.lower() == "n" or info_correct.lower() == "no":
                    log.km_fatal(
                        "Please let the researchers know that this information is incorrect and it will be addressed")
                else:
                    log.km_fatal("Invalid Input")
            else:
                print("The result is empty")
                create_user(user_id)

    if choice == 2:
        log.km_info("Exiting KMLogger")
        exit()

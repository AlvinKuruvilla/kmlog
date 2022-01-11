from base.backends.sql import SQLDriver
import os
from dotenv import load_dotenv
from prettytable import PrettyTable
from base.log import Logger
from base.user_ops.generic_ops import *


def add_user_to_db(user_defined_id: str) -> None:
    """A function which takes a user ID as input and appends it to the database
    along with information about the user such as their gender, their age, etc.
    This function should only be called during the initial enrollment phase,
    i.e. the user is not in the database yet"""

    load_dotenv()

    driver = SQLDriver()
    first, last, handedness, gender, age, education_level, social_platform = generic_create_user()
    expand_user_data(gender, handedness, education_level, social_platform)
    driver.try_connect()
    driver.insert("INSERT INTO " + os.getenv("TABLE")+" VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                  (user_defined_id, first, last, handedness, gender, age, education_level, social_platform))


def query_profile_info_from_db(user_id: str) -> list:
    """Grab all the information stored on a particular user by their user ID"""
    load_dotenv()
    res = []
    driver = SQLDriver()
    driver.try_connect()
    cursor = driver.query("SELECT * FROM " +
                          os.getenv("TABLE") + " WHERE user_id = " + str(user_id), ())
    result = cursor.fetchone()
    for row in result:
        res.append(row)
    return res


def get_profile_info_as_dict(user_id: str):
    driver = SQLDriver()
    driver.try_connect()
    keys = driver.fields_from_table_name(os.getenv("TABLE"))
    values = query_profile_info_from_db(user_id)
    return dict(zip(keys, values))


def display_profile_from_db(user_id: str) -> None:
    # TODO: We need to figure out a way to not rely on a specific number of fields or a specific ordering of them
    """Cleanly display user information in a table"""
    dlog = Logger()
    driver = SQLDriver()
    driver.try_connect()
    profile_info = query_profile_info_from_db(user_id)
    print("Your user profile:")
    if profile_info[0] != None:
        uid = profile_info[0]
    else:
        # We should probably crash and error out if we reach any part where we get "None"
        uid = "None"
        dlog.km_warn("User ID not found")
    if profile_info[1] != None:
        fname = profile_info[1]
    else:
        fname = "None"
        dlog.km_warn("First name not found")
    if profile_info[2] != None:
        lname = profile_info[2]
    else:
        lname = "None"
        dlog.km_warn("Last name not found")

    if profile_info[3] == None:
        hand = "None"
        dlog.km_warn("Handedness not found")
    elif profile_info[3] == "l":
        hand = "Left"
    elif profile_info[3] == "r":
        hand = "Right"

    if profile_info[4] == None:
        gender = "None"
        dlog.km_warn("Gender not found")
    elif profile_info[4] == "m":
        gender = "Male"
    elif profile_info[4] == "f":
        gender = "Female"

    if profile_info[5] == None:
        age = "None"
        dlog.km_warn("Age not found")
    else:
        age = profile_info[5]

    if profile_info[6] == None:
        education_level = "None"
        dlog.km_warn("Education not found")
    elif profile_info[6] == "b":
        education_level = "Bachelors"
    elif profile_info[6] == "m":
        education_level = "Masters"
    elif profile_info[6] == "d":
        education_level = "Doctorate"

    if profile_info[7] == None:
        platform = "None"
        dlog.km_warn("Social Media Platform not found")
    elif profile_info[7] == "f":
        platform = "Facebook"
    elif profile_info[7] == "i":
        platform = "Instagram"
    elif profile_info[7] == "t":
        platform = "Twitter"

    out = PrettyTable()
# Old field names ["User ID", "First Name", "Last Name",
    # "Handedness", "Gender", "Age", "Education", "Social Media Platform"]
    out.field_names = driver.fields_from_table_name(os.getenv("TABLE"))

    out.add_row([uid, fname, lname, hand, gender,
                 age, education_level, platform])
    print(out)

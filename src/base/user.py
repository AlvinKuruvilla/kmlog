from .sql import SQLDriver
import os
from dotenv import load_dotenv
from prettytable import PrettyTable
from base.log import Logger


def add_user(user_id):
    load_dotenv()
    """A utility function which takes user input and appends it to the database. This function should only be called during the initial enrollment phase, ie the user is not in the database yet"""
    driver = SQLDriver()

    first = input("Please enter your first name: ")
    last = input("Please enter your last name: ")
    gender = input("Gender (enter m for male, f for female, o: other): ")
    handedness = input("dominant hand: (enter l for left, r for right): ")
    age = input("age (whole number): ")
    education_level = input(
        "education level?: (b for bachelor, m for master, d for doctor): ")
    social_platform = input(
        "what social media platform you are going to use? (f for facebook, i for instagram, t for twitter) ")
    driver.try_connect()
    driver.insert("INSERT INTO " + os.getenv("TABLE")+" VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                  (user_id, first, last, handedness, gender, age, education_level, social_platform))


def get_profile_info(user_id):
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


def display_profile(user_id):
    log = Logger()
    profile_info = get_profile_info(user_id)
    print("Your user profile:")
    if profile_info[0] != None:
        uid = profile_info[0]
    else:
        # We should probably crash and error out if we reach any part where we get "None"
        uid = "None"
        print("User ID not found")
    if profile_info[1] != None:
        fname = profile_info[1]
    else:
        fname = "None"
        print("First name not found")
    if profile_info[2] != None:
        lname = profile_info[2]
    else:
        lname = "None"
        print("Last name not found")

    if profile_info[3] == None:
        hand = "None"
        print("Handedness not found")
    elif profile_info[3] == "l":
        hand = "Left"
    elif profile_info[3] == "r":
        hand = "Right"

    if profile_info[4] == None:
        gender = "None"
        print("Gender not found")
    elif profile_info[4] == "m":
        gender = "Male"
    elif profile_info[4] == "f":
        gender = "Female"

    if profile_info[5] == None:
        age = "None"
        print("Age not found")
    else:
        age = profile_info[5]

    if profile_info[6] == None:
        education_level = "None"
        print("Education not found")
    elif profile_info[6] == "b":
        education_level = "Bachelors"
    elif profile_info[6] == "m":
        education_level = "Masters"
    elif profile_info[6] == "d":
        education_level = "Doctorate"

    if profile_info[7] == None:
        platform = "None"
        print("Social Media Platform not found")
    elif profile_info[7] == "f":
        platform = "Facebook"
    elif profile_info[7] == "i":
        platform = "Instagram"
    elif profile_info[7] == "t":
        platform = "Twitter"

    out = PrettyTable()

    out.field_names = ["User ID", "First Name", "Last Name",
                       "Handedness", "Gender", "Age", "Education", "Social Media Platform"]

    out.add_row([uid, lname, fname, hand, gender,
                 age, education_level, platform])

    print(out)

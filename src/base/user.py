from base.sql import SQLDriver
import os
from base.util import km_prompt
from dotenv import load_dotenv
from prettytable import PrettyTable
from base.log import Logger


def verify_gender(gender_input: str) -> bool:
    """A helper function to make verifying gender strings easier"""

    if gender_input.lower() == "m" or gender_input.lower() == "f" or gender_input.lower() == "o":
        return True
    else:
        return False


def verify_handedness(hand_input: str) -> bool:
    """A helper function to make verifying handedness strings easier"""

    if hand_input.lower() == "l" or hand_input.lower() == "r" or hand_input.lower() == "a":
        return True
    else:
        return False


def verify_age(age_str: str) -> bool:
    """A helper function to make verifying age strings easier"""

    age = int(age_str)
    # Check if the age is negative or has a decimal in it
    if age < 0 or age_str.isdigit() == False:
        user_log = Logger("user")
        user_log.km_warn("Age is negative or not a whole number")
        return False
    else:
        return True


def verify_education(education_str: str) -> bool:
    """A helper function to make verifying education strings easier"""

    if education_str.lower() == "b" or education_str.lower() == "m" or education_str.lower() == "d":
        return True
    else:
        return False


def verify_social_media_platform(platform_name: str) -> bool:
    """A helper function to make verifying social media platform strings easier"""

    if platform_name.lower() == "f" or platform_name.lower() == "t" or platform_name.lower == "i":
        return True
    else:
        return False


def expand_user_data(gender: str, handedness: str, education: str, platform: str) -> tuple:
    """A function to expand specific user data before it gets committed to the database to make it easier to read
    For example, for gender this function would transform 'm' to 'Male'
    """

    if gender.lower() == "m":
        expanded_gender = "Male"
    elif gender.lower() == "f":
        expanded_gender = "Female"
    if handedness.lower() == "l":
        expanded_handedness = "Left"
    elif handedness.lower() == "r":
        expanded_handedness = "Reft"
    elif handedness.lower() == "a":
        expanded_handedness = "Ambidextrous"
    if education.lower() == "b":
        expanded_education = "Bachelors"
    elif education.lower() == "m":
        expanded_education = "Masters"
    elif education.lower() == "d":
        expanded_education = "Doctorate"
    if platform.lower() == "f":
        expanded_platform_name = "Facebook"
    elif platform.lower() == "i":
        expanded_platform_name = "Instagram"
    elif platform.lower() == "t":
        expanded_platform_name = "Twitter"
    return (expanded_gender, expanded_handedness, expanded_education, expanded_platform_name)


def add_user(user_defined_id: str) -> None:
    """A function which takes a user ID as input and appends it to the database
    along with information about the user such as their gender, their age, etc.
    This function should only be called during the initial enrollment phase,
    i.e. the user is not in the database yet"""

    vlog = Logger("add")
    load_dotenv()

    driver = SQLDriver()

    first = input(km_prompt("Please enter your first name: "))
    last = input(km_prompt("Please enter your last name: "))
    gender = input(
        km_prompt("Gender (enter m for male, f for female, o for other): "))
    while True:
        if verify_gender(gender) == False:
            vlog.km_warn("Please enter a valid gender")
            gender = input(
                km_prompt("Gender (enter m for male, f for female, o for other): "))
        else:
            break

    handedness = input(
        km_prompt("dominant hand: (enter l for left, r for right, or a for ambidextrous): "))
    while True:
        if verify_handedness(handedness) == False:
            vlog.km_warn("Please enter a valid handedness")
            handedness = input(
                km_prompt("dominant hand: (enter l for left, r for right, or a for ambidextrous): "))
        else:
            break

    age = input(km_prompt("What is your age (whole number): "))
    while True:
        if verify_age(age) == False:
            age = input(km_prompt("What is your age (whole number): "))
        else:
            break
    education_level = input(
        km_prompt("education level?: (b for bachelor, m for master, d for doctor): "))
    while True:
        if verify_education(education_level) == False:
            vlog.km_warn("Please enter a valid education level")
            education_level = input(
                km_prompt("education level?: (b for bachelor, m for master, d for doctor): "))
        else:
            break
    social_platform = input(
        km_prompt("what social media platform you are going to use? (f for facebook, i for instagram, t for twitter): "))
    while True:
        if verify_social_media_platform(social_platform) == False:
            social_platform = input(
                km_prompt("what social media platform you are going to use? (f for facebook, i for instagram, t for twitter): "))
            vlog.km_warn("Please enter a valid social media platform")
        else:
            break
    expand_user_data(gender, handedness, education_level, social_platform)
    driver.try_connect()
    driver.insert("INSERT INTO " + os.getenv("TABLE")+" VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                  (first, last, handedness, gender, age, education_level, social_platform, user_defined_id))


def get_profile_info(user_id: str) -> list:
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


def display_profile(user_id: str) -> None:
    """Cleanly display user information in a tabular format"""
    dlog = Logger("display")
    profile_info = get_profile_info(user_id)
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

    out.field_names = ["User ID", "First Name", "Last Name",
                       "Handedness", "Gender", "Age", "Education", "Social Media Platform"]

    out.add_row([uid, fname, lname, hand, gender,
                 age, education_level, platform])
    print(out)

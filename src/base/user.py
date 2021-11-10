from .sql import SQLDriver
import os
from dotenv import load_dotenv


def add_user(user_id):
    load_dotenv()
    """A small utility function which takes user input and appends it to the database. This function should only be called during the initial enrollment phase, ie the user is not in the database yet"""
    driver = SQLDriver()

    gender = input("Gender (enter m for male, f for female, o: other): ")
    handedness = input("dominant hand: (enter l for left, r for right): ")
    age = input("age (whole number): ")
    education_level = input(
        "education level?: (b for bachelor, m for master, d for doctor): ")
    social_platform = input(
        "what social media platform you are going to use? (f for facebook, i for instagram, t for twitter) ")
    driver.try_connect()
    driver.insert("INSERT INTO " + os.getenv("TABLE")+" VALUES (%s, %s, %s, %s, %s, %s)",
                  (user_id, handedness, gender, age, education_level, social_platform))

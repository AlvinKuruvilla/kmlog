from base.yaml_driver import YAMLDriver
from base.log import Logger
import os
from base.util import km_prompt
from base.user_ops.generic_ops import *


def user_id_to_yaml_file_path(user_id: str) -> str:
    # NOTE: We have to deal with the edge case where part of a user_id can exist in another (eg the user_id 123 is in the user_id 1234)
    directory = os.path.join(os.getcwd(), "src", "users")
    for file in os.scandir(directory):
        if (file.path.endswith(".yaml") and file.is_file):
            # Trim the extension from the file path and see if it matches the user_id given
            file_with_ext = os.path.basename(file.path)
            file_name = os.path.splitext(file_with_ext)[0]
            if(file_name == user_id):
                return os.path.join(directory, file_with_ext)


def tuple_to_dict(data: tuple, labels: list):
    assert(len(data) == len(labels),
           "Cannot create a dictionary from a tuple if the length of the tuple != length of the labels")
    data_list = list(data)
    data_dict = {}
    for i in range(len(data_list)):
        print(labels[i] + ":" + data_list[i])
        data_dict[labels[i]] = data_list[i]
    return data_dict


def create_user(user_id: str):
    vlog = Logger("add")
    yml = YAMLDriver()
    first = input(km_prompt("Please enter your first name: "))
    last = input(km_prompt("Please enter your last name: "))
    gender = input(
        km_prompt("Please enter your gender (m for male, f for female, o for other): "))
    while True:
        if verify_gender(gender) == False:
            vlog.km_warn("Please enter a valid gender")
            gender = input(
                km_prompt("Please enter your gender (m for male, f for female, o for other):"))
        else:
            break

    handedness = input(
        km_prompt("What is your dominant hand: (enter l for left, r for right, or a for ambidextrous): "))
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
        km_prompt("What is your current or maximum education level?: (b for bachelor, m for master, d for doctor): "))
    while True:
        if verify_education(education_level) == False:
            vlog.km_warn("Please enter a valid education level")
            education_level = input(
                km_prompt("education level?: (b for bachelor, m for master, d for doctor): "))
        else:
            break
    social_platform = input(
        km_prompt("Which social media platform are you using? (f for facebook, i for instagram, t for twitter): "))
    while True:
        if verify_social_media_platform(social_platform) == False:
            social_platform = input(
                km_prompt("what social media platform you are going to use? (f for facebook, i for instagram, t for twitter): "))
            vlog.km_warn("Please enter a valid social media platform")
        else:
            break
    part = expand_user_data(
        gender, handedness, education_level, social_platform)
    # FIXME: We have to make sure to cast some of the fields to str so it look correct when it gets translated to yaml
    pl = list(part)
    pl.insert(0, last)
    pl.insert(0, first)
    pl.insert(0, user_id)
    pl.insert(4, age)
    t = tuple(pl)
    labels = ["user_id", "first_name", "last_name", "gender",
              "age", "handedness", "education", "platform"]

    data = tuple_to_dict(t, labels)
    yml.write_to_yaml_file(user_id, data)

# pylint: disable=C0301
# pylint: disable=C0114
# pylint: disable=E0401
# pylint: disable=R1705
# pylint: disable=R0912
# pylint: disable=R0915

# Copyright 2021 - 2022, Alvin Kuruvilla <alvineasokuruvilla@gmail.com>, Dr. Rajesh Kumar <Rajesh.Kumar@hofstra.edu>
# Use of this source code is governed by an MIT-style
# license that can be found in the LICENSE file or at
# https://opensource.org/licenses/MIT.

from typing import Tuple
from base.log import Logger
from base.displayer import km_prompt
from base.backends.sql import check_mysql_installed


def verify_gender(gender_input: str) -> bool:
    """
    A helper function to make verifying gender strings easier

    Parameters
    ----------
    gender_input: str
        The single letter gender string to be verified.
        Valid inputs are: 'm', 'f', 'o'

    Returns
    ----------
    bool: Returns true if the gender string is a valid gender
    """
    return bool(
        gender_input.lower() == "m"
        or gender_input.lower() == "f"
        or gender_input.lower() == "o"
    )


def verify_handedness(hand_input: str) -> bool:
    """
    A helper function to make verifying handedness strings easier

    Parameters
    ----------
    hand_input: str
        The single letter handedness string to be verified.
        Valid inputs are: 'l', 'r', 'a'

    Returns
    ----------
    bool: Returns true if the handedness string is a valid handedness

    """

    return bool(
        hand_input.lower() == "l"
        or hand_input.lower() == "r"
        or hand_input.lower() == "a"
    )


def verify_age(age_str: str) -> bool:
    """A helper function to make verifying age strings easier

    Parameters
    ----------
    age: str
        The string representation of an age.

    Returns
    ----------
    bool: Returns true if the age string is a valid age
    """
    user_log = Logger()

    # Check if the age is negative, has a decimal in it, or contains letters or some other invalid chars

    if not age_str.isdecimal():
        user_log.km_warn("Age contains letters or invalid characters")
        return False
    elif not age_str.isdigit():
        user_log.km_warn("Age cannot be a decimal")
        return False
    age = int(age_str)
    if age < 0:
        user_log.km_warn("Age cannot be negative")
        return False
    return True


def verify_education(education_str: str) -> bool:
    """
    A helper function to make verifying education strings easier

    Parameters
    ----------
    education_str: str
        The single letter education string to be verified.
        Valid inputs are: 'b', 'm', 'd'

    Returns
    ----------
    bool: Returns true if the education string is a valid education
    """
    return bool(
        education_str.lower() == "b"
        or education_str.lower() == "m"
        or education_str.lower() == "d"
    )


def verify_social_media_platform(platform_name: str) -> bool:
    """
    A helper function to make verifying social media platform strings easier

    Parameters
    ----------
    platform_name: str
        The name of the social media platform to be verified.
        Valid inputs are: 'f', 't', 'i', 'a'

    Returns
    ----------
    bool: Returns true if the provided social media platform is a valid social media platform

    """
    return bool(
        platform_name.lower() == "f"
        or platform_name.lower() == "t"
        or platform_name.lower() == "i"
        or platform_name.lower() == "a"
    )


def expand_user_data(
    gender: str, handedness: str, education: str, platform: str
) -> Tuple[str, str, str, str]:
    """
    A function to expand specific user data before it gets committed to the database,
    written to file or displayed on screen to make it easier to read

    For example, for gender this function would transform 'm' to 'Male'

    Parameters
    ----------
    gender: str
        The shortened data string to be expanded
        Valid inputs are: 'm', 'f', 'o'
    handedness: str
        The single letter handedness string to be expanded.
        Valid inputs are: 'l', 'r', 'a'
    education: str
        The single letter education string to be expanded.
        Valid inputs are: 'b', 'm', 'd'
    platform: str
        The name of the social media platform to be expanded.
        Valid inputs are: 'f', 't', 'i', 'a'


    Returns
    ----------
    Tuple[str, str, str, str]: Returns a tuple of all the expanded forms of the inputted parameters

    """
    if check_mysql_installed:
        if gender.lower() == "m":
            expanded_gender = "Male"
        elif gender.lower() == "f":
            expanded_gender = "Female"
        elif gender.lower() == "o":
            expanded_gender = "Other"
        if handedness.lower() == "l":
            expanded_handedness = "Left"
        elif handedness.lower() == "r":
            expanded_handedness = "Right"
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
        elif platform.lower() == "a":
            expanded_platform_name = "All"
        return (
            expanded_gender,
            expanded_handedness,
            expanded_education,
            expanded_platform_name,
        )
    else:
        if gender.lower() == "m":
            expanded_gender = f'{"Male"}'
        elif gender.lower() == "f":
            expanded_gender = f'{"Female"}'
        elif gender.lower() == "o":
            expanded_gender = f'{"Other"}'
        if handedness.lower() == "l":
            expanded_handedness = f'{"Left"}'
        elif handedness.lower() == "r":
            expanded_handedness = f'{"Right"}'
        elif handedness.lower() == "a":
            expanded_handedness = f'{"Ambidextrous"}'
        if education.lower() == "b":
            expanded_education = f'{"Bachelors"}'
        elif education.lower() == "m":
            expanded_education = f'{"Masters"}'
        elif education.lower() == "d":
            expanded_education = f'{"Doctorate"}'
        if platform.lower() == "f":
            expanded_platform_name = f'{"Facebook"}'
        elif platform.lower() == "i":
            expanded_platform_name = f'{"Instagram"}'
        elif platform.lower() == "t":
            expanded_platform_name = f'{"Twitter"}'
        elif platform.lower() == "a":
            expanded_platform_name = f'{"All"}'
        return (
            expanded_gender,
            expanded_handedness,
            expanded_education,
            expanded_platform_name,
        )


def generic_create_user() -> Tuple[str, str, str, str, str, str, str]:
    """
    Function for users to input their information

    Parameters
    ----------
    None

    Returns
    ----------
    Tuple[str, str, str, str, str, str, str]
    """
    vlog = Logger()
    first = str(input(km_prompt("Please enter your first name: ")))
    last = str(input(km_prompt("Please enter your last name: ")))
    gender = str(
        input(km_prompt("Gender (enter m for Male, f for Female, o for Other): "))
    )
    while True:
        if verify_gender(gender) is False:
            vlog.km_warn("Please enter a valid gender")
            gender = str(
                input(
                    km_prompt("Gender (enter m for Male, f for Female, o for Other): ")
                )
            )
        else:
            break

    handedness = input(
        km_prompt(
            "What is your dominant hand: (enter l for Left, r for Right, or a for Ambidextrous): "
        )
    )
    while True:
        if verify_handedness(handedness) is False:
            vlog.km_warn("Please enter a valid handedness")
            handedness = input(
                km_prompt(
                    "What is your dominant hand: (enter l for Left, r for Right, or a for Ambidextrous): "
                )
            )
        else:
            break

    age = input(km_prompt("What is your age (whole number): "))
    while True:
        if verify_age(age) is False:
            age = input(km_prompt("What is your age (whole number): "))
        else:
            break
    education_level = input(
        km_prompt(
            "What is your education level?: (b for Bachelor, m for Master, d for Doctorate): "
        )
    )
    while True:
        if verify_education(education_level) is False:
            vlog.km_warn("Please enter a valid education level")
            education_level = input(
                km_prompt(
                    "What is your education level?: (b for Bachelor, m for Master, d for Doctorate): "
                )
            )
        else:
            break
    social_platform = input(
        km_prompt(
            "What social media platform you are going to use? (f for Facebook, i for Instagram, t for Twitter, or a for All of them): "
        )
    )
    while True:
        if verify_social_media_platform(social_platform) is False:
            vlog.km_warn("Please enter a valid social media platform")
            social_platform = input(
                km_prompt(
                    "What social media platform are you going to use? (f for Facebook, i for Instagram, t for Twitter, or a for All): "
                )
            )
        else:
            break
    return (first, last, handedness, gender, age, education_level, social_platform)

from base.log import Logger
from base.util import km_prompt
from base.backends.sql import check_mysql_installed


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
    user_log = Logger()

    # Check if the age is negative, has a decimal in it, or contains letters or some other invalid chars

    if age_str.isdecimal() == False:
        user_log.km_warn("Age contains letters or invalid characters")
        return False
    elif age_str.isdigit() == False:
        user_log.km_warn("Age cannot be a decimal")
        return False
    age = int(age_str)
    if age < 0:
        user_log.km_warn("Age cannot be negative")
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
    print("The platform you inputted is", platform_name.lower())
    if platform_name.lower() == "f" or platform_name.lower() == "t" or platform_name.lower() == "i":
        return True
    else:
        return False


def expand_user_data(gender: str, handedness: str, education: str, platform: str) -> tuple:
    """A function to expand specific user data before it gets committed to the database to make it easier to read
    For example, for gender this function would transform 'm' to 'Male'
    """
    if check_mysql_installed == True:
        if gender.lower() == "m":
            expanded_gender = "Male"
        elif gender.lower() == "f":
            expanded_gender = "Female"
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
        return (expanded_gender, expanded_handedness, expanded_education, expanded_platform_name)
    else:
        if gender.lower() == "m":
            expanded_gender = f'{"Male"}'
        elif gender.lower() == "f":
            expanded_gender = f'{"Female"}'
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
        return (expanded_gender, expanded_handedness, expanded_education, expanded_platform_name)


def generic_create_user():
    vlog = Logger()
    first = str(input(km_prompt("Please enter your first name: ")))
    last = str(input(km_prompt("Please enter your last name: ")))
    gender = str(input(
        km_prompt("Gender (enter m for male, f for female, o for other): ")))
    while True:
        if verify_gender(gender) == False:
            vlog.km_warn("Please enter a valid gender")
            gender = str(input(
                km_prompt("Gender (enter m for male, f for female, o for other): ")))
        else:
            break

    handedness = input(
        km_prompt("What is your dominant hand: (enter l for left, r for right, or a for ambidextrous): "))
    while True:
        if verify_handedness(handedness) == False:
            vlog.km_warn("Please enter a valid handedness")
            handedness = input(
                km_prompt("What is your dominant hand: (enter l for left, r for right, or a for ambidextrous): "))
        else:
            break

    age = input(km_prompt("What is your age (whole number): "))
    while True:
        if verify_age(age) == False:
            age = input(km_prompt("What is your age (whole number): "))
        else:
            break
    education_level = input(
        km_prompt("What is your education level?: (b for bachelor, m for master, d for doctor): "))
    while True:
        if verify_education(education_level) == False:
            vlog.km_warn("Please enter a valid education level")
            education_level = input(
                km_prompt("What is your education level?: (b for bachelor, m for master, d for doctor): "))
        else:
            break
    social_platform = input(
        km_prompt("What social media platform you are going to use? (f for facebook, i for instagram, t for twitter): "))
    while True:
        if verify_social_media_platform(social_platform) == False:
            vlog.km_warn("Please enter a valid social media platform")
            social_platform = input(
                km_prompt("What social media platform are you going to use? (f for facebook, i for instagram, t for twitter): "))
        else:
            break
    return(first, last, handedness, gender, age, education_level, social_platform)

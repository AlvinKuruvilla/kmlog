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

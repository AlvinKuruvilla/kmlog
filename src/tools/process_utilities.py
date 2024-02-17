# Copyright 2021 - 2023, Alvin Kuruvilla <alvineasokuruvilla@gmail.com>, Dr. Rajesh Kumar <Rajesh.Kumar@hofstra.edu>

# Use of this source code is governed by an MIT-style
# license that can be found in the LICENSE file or at
# https://opensource.org/licenses/MIT.

# This is a small debug utility to print the pid KMLogger is
# running on to help with profiling
import os
from setproctitle import setproctitle, getproctitle
import psutil
from base.displayer import block_text


def set_process_title(title: str):
    setproctitle(title)


def get_process_title():
    getproctitle()


def print_pid():
    """
    Print the PID of the currently executing version of KMLog.

    Parameters
    ----------
    None

    Returns
    -------
    None
    """
    block_text("PID")
    print("The pid is:", os.getpid())


def check_if_process_running(processName):
    """
    Check if there is any running process that contains the given name processName.
    """
    # Iterate over the all the running process
    for proc in psutil.process_iter():
        try:
            # Check if process name contains the given name string.
            if processName.lower() in proc.name().lower():
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False


def find_pid_by_name(processName):
    """
    Get a list of all the PIDs of a all the running process whose name contains
    the given string processName
    """
    listOfProcessObjects = []
    # Iterate over the all the running process
    for proc in psutil.process_iter():
        try:
            pinfo = proc.as_dict(attrs=["pid", "name", "create_time"])
            # Check if process name contains the given name string.
            if processName.lower() in pinfo["name"].lower():
                listOfProcessObjects.append(pinfo)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return listOfProcessObjects

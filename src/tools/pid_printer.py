# Copyright 2021 - 2022, Alvin Kuruvilla <alvineasokuruvilla@gmail.com>, Dr. Rajesh Kumar <Rajesh.Kumar@hofstra.edu>

# Use of this source code is governed by an MIT-style
# license that can be found in the LICENSE file or at
# https://opensource.org/licenses/MIT.

# This is a small debug utility to print the pid KMLogger is
# running on to help with profiling
import os
from base.util import block_text


def print_pid():
    block_text("PID")
    print(os.getpid())

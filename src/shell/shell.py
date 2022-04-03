# Copyright 2022, Alvin Kuruvilla <alvineasokuruvilla@gmail.com>, Dr. Rajesh Kumar <Rajesh.Kumar@hofstra.edu>

# Use of this source code is governed by an MIT-style
# license that can be found in the LICENSE file or at
# https://opensource.org/licenses/MIT.

import readline
from base.displayer import km_prompt

from shell.completer import CommandCompleter


class Shell:
    def __init__(self):
        self.completer = CommandCompleter(
            ["hello", "hi", "how are you", "goodbye", "great"]
        )

    def start(self):
        while True:
            readline.set_completer(self.completer.complete)
            readline.parse_and_bind("tab: complete")
            typed = input(km_prompt(""))
            print("You entered", typed)

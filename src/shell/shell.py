# Copyright 2022, Alvin Kuruvilla <alvineasokuruvilla@gmail.com>, Dr. Rajesh Kumar <Rajesh.Kumar@hofstra.edu>

# Use of this source code is governed by an MIT-style
# license that can be found in the LICENSE file or at
# https://opensource.org/licenses/MIT.

from base.displayer import km_prompt
import cmd
import sys


class Shell(cmd.Cmd):
    FRIENDS = ["Alice", "Adam", "Barbara", "Bob"]
    prompt = km_prompt("")

    def do_greet(self, person):
        "Greet the person"
        if person and person in self.FRIENDS:
            greeting = "hi, %s!" % person
        elif person:
            greeting = "hello, " + person
        else:
            greeting = "hello"
        print(greeting)

    def do_exit(self):
        """Exit the shell and return to the main menu"""
        sys.exit(0)


if __name__ == "__main__":
    pass

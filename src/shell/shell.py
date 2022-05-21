# Copyright 2022, Alvin Kuruvilla <alvineasokuruvilla@gmail.com>, Dr. Rajesh Kumar <Rajesh.Kumar@hofstra.edu>

# Use of this source code is governed by an MIT-style
# license that can be found in the LICENSE file or at
# https://opensource.org/licenses/MIT.

from base.displayer import km_prompt
import sys

from base.log import Logger


class Shell:
    def run(self):
        while True:
            prompt = input(km_prompt(""))
            if prompt == "exit":
                exit()

    def exit(self):
        """Exit the shell and return to the main menu"""
        log = Logger()
        log.km_info("Exiting KMLogger")
        sys.exit(0)


if __name__ == "__main__":
    pass

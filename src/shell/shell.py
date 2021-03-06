# Copyright 2022, Alvin Kuruvilla <alvineasokuruvilla@gmail.com>, Dr. Rajesh Kumar <Rajesh.Kumar@hofstra.edu>

# Use of this source code is governed by an MIT-style
# license that can be found in the LICENSE file or at
# https://opensource.org/licenses/MIT.

from base.displayer import km_prompt
from base.log import Logger
from shell.commands import show_banner, cmd_help, show_csv, show_yaml, exit
from shell.utils import FileType, grab_args, verify_file_path


class Shell:
    def run(self):
        log = Logger()
        show_banner()
        log.km_warn(
            "NOTE: This is still a Work in Progress. There is still a lot of functionality missing"
        )
        while True:
            prompt = input(km_prompt(""))
            if prompt == "exit":
                exit()
            elif prompt == "help" or prompt == "?":
                cmd_help()
            elif prompt.__contains__("render"):
                parameters = grab_args(prompt)
                # print(parameters)
                if parameters == None or parameters == "":
                    log.km_error("Invalid number of parameters")
                    continue
                if verify_file_path(parameters) == FileType.NotAFile:
                    continue
                elif verify_file_path(parameters) == FileType.CSV:
                    show_csv(parameters)
                elif verify_file_path(parameters) == FileType.YAML:
                    show_yaml(parameters)
            else:
                log.km_error("Invalid command %s" % prompt)


if __name__ == "__main__":
    pass

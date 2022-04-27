# Copyright 2022, Alvin Kuruvilla <alvineasokuruvilla@gmail.com>, Dr. Rajesh Kumar <Rajesh.Kumar@hofstra.edu>

# Use of this source code is governed by an MIT-style
# license that can be found in the LICENSE file or at
# https://opensource.org/licenses/MIT.

import subprocess
import os


class CommandExecutor:
    def __init__(self, executable_path: str):
        self.executable_path = executable_path
        pass

    def set_executable_path(self, path):
        self.executable_path = path

    def get_executable_path(self):
        return self.executable_path

    def run_executable(self):
        popen = subprocess.Popen([self.executable_path])
        popen.wait()
        # output = popen.stdout.read()
        # print(output)


if __name__ == "__main__":
    path = os.path.join(os.getcwd(), "dist", "kmlog")
    command_executor = CommandExecutor(path)
    command_executor.run_executable()

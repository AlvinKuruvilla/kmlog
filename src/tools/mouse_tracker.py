# Copyright 2021 - 2022, Alvin Kuruvilla <alvineasokuruvilla@gmail.com>, Dr. Rajesh Kumar <Rajesh.Kumar@hofstra.edu>

# Use of this source code is governed by an MIT-style
# license that can be found in the LICENSE file or at
# https://opensource.org/licenses/MIT.

import pyautogui

if __name__ == "__main__":
    """
    A simple program to constantly track current mouse position and store coordinates to file
    """
    buf = []
    while True:
        print(pyautogui.position())
        buf.append(pyautogui.position())
        with open("mouse_data_file.log", "w", encoding="utf8") as file:
            for elem in buf:
                file.write(str(elem) + "\n")

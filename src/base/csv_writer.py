# Copyright 2021 - 2022, Alvin Kuruvilla <alvineasokuruvilla@gmail.com>, Dr. Rajesh Kumar <Rajesh.Kumar@hofstra.edu>

# Use of this source code is governed by an MIT-style
# license that can be found in the LICENSE file or at
# https://opensource.org/licenses/MIT.

import csv


class CSVWriter:
    def __init__(self) -> None:
        self.headers = ["Press or Release", "Key", "Time"]
        return

    def write_header(self, file_path):
        with open(file_path, "a") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=self.headers)
            writer.writeheader()
            # print("Wrote header to file: ", file_path)

    def write_data_to_csv(self, file_path, data: list):
        with open(file_path, "a") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(data)
            # print("Wrote data to file: ", file_path)

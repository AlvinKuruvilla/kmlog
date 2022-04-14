# pylint: disable=C0301
# pylint: disable=C0114
# pylint: disable=C0115
# pylint: disable=R0201

# Copyright 2021 - 2022, Alvin Kuruvilla <alvineasokuruvilla@gmail.com>, Dr. Rajesh Kumar <Rajesh.Kumar@hofstra.edu>
# Use of this source code is governed by an MIT-style
# license that can be found in the LICENSE file or at
# https://opensource.org/licenses/MIT.

import csv


class CSVWriter:
    def __init__(self) -> None:
        self.headers = ["Press or Release", "Key", "Time"]

    def write_header(self, file_path: str):
        """
        Write a header to a csv file.

        Parameters
        ----------
        text: str
              The csv file path to write the header to.
        Returns
        -------
        None
        """
        with open(file_path, "a+", encoding="utf8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=self.headers)
            writer.writeheader()
            # print("Wrote header to file: ", file_path)

    def write_data_to_csv(self, file_path: str, data: list):
        """
        Write data to a csv file.

        Parameters
        ----------
        file_path: str
              The csv file path to write the data to.
        data: list
              The data to write to the file.
        Returns
        -------
        None
        """
        with open(file_path, "a+", encoding="utf8") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(data)
            # print("Wrote data to file: ", file_path)

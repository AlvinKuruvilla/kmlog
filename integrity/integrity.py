# Copyright 2022, Alvin Kuruvilla <alvineasokuruvilla@gmail.com>, Dr. Rajesh Kumar <Rajesh.Kumar@hofstra.edu>

# Use of this source code is governed by an MIT-style
# license that can be found in the LICENSE file or at
# https://opensource.org/licenses/MIT.
import os
from renderer import dump_invalid_time_frame
from logger import Logger
import pandas as pd


def is_csv_file(filename: str) -> bool:
    hlog = Logger()
    if filename.endswith(".csv") and os.path.exists(filename):
        return True
    hlog.km_error("Provided path is not a valid CSV file or does not exist")
    return False


class IntegrityChecker:
    def __init__(self):
        pass

    def get_file_path(self):
        return self.file_path

    def set_file_path(self, new_file_path: str):
        self.file_path = new_file_path

    def check_integrity(self, file_path: str):
        if not is_csv_file(file_path):
            return
        df = pd.read_csv(file_path)
        print(df.columns)
        # FIXME: We should only increment once if the csv file has a header, otherwise don't increment
        df.index += 1
        return df


if __name__ == "__main__":
    integrity = IntegrityChecker()
    path = os.path.join(os.getcwd(), "integrity", "test.csv")
    data = integrity.check_integrity(path)
    dump_invalid_time_frame(data, 2)

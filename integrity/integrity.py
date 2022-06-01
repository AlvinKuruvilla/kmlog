# Copyright 2022, Alvin Kuruvilla <alvineasokuruvilla@gmail.com>, Dr. Rajesh Kumar <Rajesh.Kumar@hofstra.edu>

# Use of this source code is governed by an MIT-style
# license that can be found in the LICENSE file or at
# https://opensource.org/licenses/MIT.
import os
import argparse
from renderer import *
from logger import Logger
import pandas as pd
from pathlib import Path
from rich.traceback import install

install()
parser = argparse.ArgumentParser()


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
        # FIXME: We should only increment once if the csv file has a header, otherwise don't increment
        # previous = df.loc[1, "Time"]
        # print(previous)
        # display_duplicate_events(df)
        dump_invalid_time_frame(df)


if __name__ == "__main__":
    integrity = IntegrityChecker()
    log = Logger()
    parser.add_argument(
        "path", help="path to the CSV file (Can be absolute or relative)"
    )
    args = parser.parse_args()
    if not os.path.exists(args.path):
        log.km_error("Cannot find path: ", args.path)
    path = str(Path(args.path))
    data = integrity.check_integrity(path)
    # dump_invalid_time_frame(data, 2)

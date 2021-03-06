# Copyright 2022, Alvin Kuruvilla <alvineasokuruvilla@gmail.com>, Dr. Rajesh Kumar <Rajesh.Kumar@hofstra.edu>

# Use of this source code is governed by an MIT-style
# license that can be found in the LICENSE file or at
# https://opensource.org/licenses/MIT.

import pandas as pd
from colorama import init, Fore

from processor import duplicate_events, find_invalid_time_indices


def print_csv(path: str):
    df = pd.read_csv(path)
    print(df)


# TODO: Verify that the value for invalid_frame_index is the correct row index
def dump_invalid_time_frame(data: pd.DataFrame):
    init(autoreset=True)
    invalids = find_invalid_time_indices(data)
    for invalid_frame_index in invalids:
        print((Fore.RED + str(data.iloc[[invalid_frame_index]])))


def display_duplicate_events(data):
    init(autoreset=True)
    event_indices = duplicate_events(data)
    for index in event_indices:
        print((Fore.RED + str(data.loc[index].values.tolist())))

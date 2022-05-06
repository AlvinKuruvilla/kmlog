# Copyright 2022, Alvin Kuruvilla <alvineasokuruvilla@gmail.com>, Dr. Rajesh Kumar <Rajesh.Kumar@hofstra.edu>

# Use of this source code is governed by an MIT-style
# license that can be found in the LICENSE file or at
# https://opensource.org/licenses/MIT.

import pandas as pd
from colorama import init, Fore


def print_csv(path: str):
    # path = os.path.join(os.getcwd(), "logs", "123.csv")
    df = pd.read_csv(path)
    print(df)


#! FIXME: Crashes
def find_invalid_time_indices(df):
    try:
        data = df["Time"].tolist()
    except KeyError:
        data = df.iloc[:, 2].tolist()
    # print(data)
    # input("HOLD")
    current_max = data[0]
    invalids = [current_max]
    for k in range(0, len(data) - 2):
        current_max = data[k]
        if data[k] < current_max:
            invalids.append(k)
        current_max = data[k]
    return invalids


def duplicate_events(df):
    try:
        data = df["Time"].tolist()
    except KeyError:
        data = df.iloc[:, 0].tolist()
    indices = []
    for i in range(0, len(data) - 2):
        if (data[i] == "P" and data[i + 1] == "P") or (
            data[i] == "R" and data[i + 1] == "R"
        ):
            indices.append(i)
    return indices


# TODO: Verify that the value for invalid_frame_index is the correct row index
def dump_invalid_time_frame(data: pd.DataFrame):
    init(autoreset=True)
    invalids = find_invalid_time_indices(data)
    print(invalids)
    input("HOLD")
    for invalid_frame_index in invalids:
        print((str(data.iloc[[invalid_frame_index - 1]])))
        print((Fore.RED + str(data.iloc[[invalid_frame_index]])))
        print((str(data.iloc[[invalid_frame_index + 1]])))

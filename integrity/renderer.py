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


# TODO: Verify that the value for invalid_frame_index is the correct row index
def dump_invalid_time_frame(data: pd.DataFrame, invalid_frame_index: int):
    init(autoreset=True)
    print((str(data.iloc[[invalid_frame_index - 1]])))
    print((Fore.RED + str(data.iloc[[invalid_frame_index]])))
    print((str(data.iloc[[invalid_frame_index + 1]])))

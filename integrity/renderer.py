# Copyright 2022, Alvin Kuruvilla <alvineasokuruvilla@gmail.com>, Dr. Rajesh Kumar <Rajesh.Kumar@hofstra.edu>

# Use of this source code is governed by an MIT-style
# license that can be found in the LICENSE file or at
# https://opensource.org/licenses/MIT.

import pandas as pd
from rich.panel import Panel
from rich import print


def print_csv(path: str):
    # path = os.path.join(os.getcwd(), "logs", "123.csv")
    df = pd.read_csv(path)
    print(df)


# TODO: Verify that the value for invalid_frame_index is the correct row index
def dump_invalid_time_frame(data: pd.DataFrame, invalid_frame_index: int):
    print(Panel(str(data.iloc[[invalid_frame_index]])))
    pass

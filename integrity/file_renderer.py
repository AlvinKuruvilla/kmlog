import os
import pandas as pd
import argparse

path = os.path.join(os.getcwd(), "logs", "123.csv")
df = pd.read_csv(path)
print(df)
# df.style

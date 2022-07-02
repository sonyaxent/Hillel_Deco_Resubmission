from os import truncate

import pandas as pd
import csv
import numpy

col_names = [
    'Id',
    'Height',
    'Weight'
]


df = pd.read_csv('hw.csv', names=col_names, skiprows=[0])

average_height = round(numpy.mean(df.Height), 2)
average_weight = round(numpy.mean(df.Weight), 2)

# Index, Height(Inches), Weight(Pounds)
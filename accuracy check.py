#import dask.dataframe as dd
from os import listdir

path = 'C:/Users/PRAVEEN/Desktop/New folder'


def find_csv_filenames(path, suffix=".csv"):
    filenames = listdir(path)
    return [filename for filename in filenames if filename.endswith(suffix)]


filenames = find_csv_filenames(path)
for name in filenames:
    print(name)

import pandas as pd
import os


def CsvToDataFrame(filePath,columns):
    if os.path.exists(filePath):
        df = pd.read_csv(filePath)
    else:
        df = pd.DataFrame(columns=columns)
    return df
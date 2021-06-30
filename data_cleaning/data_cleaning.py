import pandas as pd
import numpy as np

if __name__ == "__main__":
    df = pd.read_csv("../data_files/gdp.csv")

    # drop last row because its empty
    df = df.iloc[: , :-1]

    # drop column "Indicator Code" because its always the same (needed?)
    df = df.drop(df.columns[2:4], axis=1)

    # drop all rows (countries) that have less than 30 (half) values for the years
    df = df.dropna(axis=0, thresh=30)

    # fill empty values with 0 (needed for type casting to int)
    # assuming that no "valid" value is really 0, so 0 stands for "no value"
    df = df.fillna(0)

    # cast datatype of all the values of the years to int because float is not needed
    type_dict = {}
    for i in range(1960, 2021):
        type_dict[str(i)] = np.int64
    df = df.astype(type_dict)

    #print(df.describe())
    #print(df.info())

    # export cleaned data to new .csv file
    df.to_csv("../data_files/gdp_clean.csv", index=False)

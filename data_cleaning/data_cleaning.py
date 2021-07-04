import pandas as pd
import numpy as np

if __name__ == "__main__":



    # read and clean gdp.csv
    df_gdp = pd.read_csv("../data_files/gdp.csv")

    # drop last row because its empty and columns after 2016 because we dont need them
    df_gdp = df_gdp.iloc[: , :-5]

    # drop column "Indicator Code" because its always the same (needed?)
    df_gdp = df_gdp.drop(df_gdp.columns[2:4], axis=1)

    # drop all rows (countries) that have less than 27 (half) values for the years
    # 57 years total => at least 26 null values to drop the row
    df_gdp = df_gdp.dropna(axis=0, thresh=26)

    # fill empty values with 0 (needed for type casting to int)
    # assuming that no "valid" value is really 0, so 0 stands for "no value"
    df_gdp = df_gdp.fillna(0)

    # cast datatype of all the values of the years to int because float is not needed
    type_dict = {}
    for i in range(1960, 2017):
        type_dict[str(i)] = np.int64
    df_gdp = df_gdp.astype(type_dict)



    # read and clean life_expectancy.csv
    df_le = pd.read_csv("../data_files/life_expectancy.csv")

    # drop column "Indicator Code" and "Indicator Name" because they're always the same (needed?)
    df_le = df_le.drop(df_le.columns[2:4], axis=1)

    # drop all rows (countries) that have less than 27 (half) values for the years
    # 57 years total => at least 26 null values to drop the row
    df_le = df_le.dropna(axis=0, thresh=26)

    # fill empty values with 0 (needed for type casting to int)
    # assuming that no "valid" value is really 0, so 0 stands for "no value"
    df_le = df_le.fillna(0)

    # round all numbers to 3 decimals
    df_le = df_le.round(decimals=3)



    # drop all rows in the other dataset that are dropped in the other one
    # find all countries that are still in the data
    count_dict_gdp = []
    for index, row in df_gdp.iterrows():
        count_dict_gdp.append(row["Country Code"])

    # find all countries that are still in the data
    count_dict_le = []
    for index, row in df_le.iterrows():
        count_dict_le.append(row["Country Code"])

    # find all rows (countries) that are still in both datasets
    countries = [x for x in count_dict_gdp if x in count_dict_le]

    # find indices of rows that are not in both datasets and delete them from df_gdp
    index_list = []
    for index, row in df_gdp.iterrows():
        if row["Country Code"] not in countries: 
            index_list.append(index)
    df_gdp = df_gdp.drop(index_list)

    # find indices of rows that are not in both datasets and delete them from df_le
    index_list = []
    for index, row in df_le.iterrows():
        if row["Country Code"] not in countries: 
            index_list.append(index)
    df_le = df_le.drop(index_list)

    #print(df_le.info(), df_gdp.info())

    # export cleaned data to new .csv files
    df_gdp.to_csv("../data_files/gdp_clean.csv", index=False)
    df_le.to_csv("../data_files/life_expectancy_clean.csv", index=False)



    # Clean other datasets
    df_co = pd.read_csv("../data_files/co2_emission.csv")

    # drop rows (countries) without country code
    df_co = df_co.dropna()

    # drop rows that are not between 1960 and 2016
    df_co = df_co.drop(df_co[df_co.Year > 2016].index)
    df_co = df_co.drop(df_co[df_co.Year < 1960].index)

    # convert CO2 emissions to integer
    df_co = df_co.astype({"Annual CO₂ emissions (tonnes )": np.int64})

    df_co.to_csv("../data_files/co2_emission_clean.csv", index=False)



    df_pg = pd.read_csv("../data_files/population_growth.csv")

    # drop column "Indicator Code" and "Indicator Name" because they're always the same (needed?)
    df_pg = df_pg.drop(df_pg.columns[2:4], axis=1)

    # drop last 4 columns (after 2016)
    df_pg = df_pg.iloc[: , :-4]

    # fill missing values with 0
    df_pg = df_pg.fillna(0)

    # round all numbers to 5 decimals
    df_pg = df_pg.round(decimals=5)

    # find indices of rows that are not in both datasets and delete them from df_pg
    index_list = []
    for index, row in df_pg.iterrows():
        if row["Country Code"] not in countries: 
            index_list.append(index)
    df_pg = df_pg.drop(index_list)

    df_pg.to_csv("../data_files/population_growth_clean.csv", index=False)



    df_pt = pd.read_csv("../data_files/population_total.csv")

    # drop all rows with year greater than 2016
    df_pt = df_pt.drop(df_pt[df_pt.Year > 2016].index)

    df_pt.to_csv("../data_files/population_total_clean.csv", index=False)

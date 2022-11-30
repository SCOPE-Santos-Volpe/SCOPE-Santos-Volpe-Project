"""This file is to hold a bunch of useful helper functions so that they can be imported into any file
"""

import pandas as pd
import glob
import os

def get_all_csv_filenames(path: str) -> list[str]:
    """Finds and returns the filenames (including the folder) of every CSV in the folder specified at `path`.

    Args:
        path: A string containing the path to the folder containing the .csv files

    Returns:
        A list of strings containing the file path to every csv in the folder at `path`
    """
    all_filenames = glob.glob(os.path.join(path, "*.CSV"))
    return all_filenames

def load_df_from_csv(path:str, **kwargs) -> pd.DataFrame:
    """Loads a dataframe from the csv at `path`.

    Convenience wrapper for `pd.read_csv` because Mira likes wrapping everything in their own helper function

    Args:
        path: A string containing the path to a .csv file
        **kwargs: Pass through other arguments to pd.read_csv

    Returns:
        A `pd.DataFrame` loaded from the .csv
    """
    df=pd.read_csv(path, **kwargs)
    return df

def get_all_dfs_from_csv(filenames: list[str], required_columns: list[str] = [], **kwargs) -> list[pd.DataFrame]:
    """Returns a list of dataframes loaded from the list of files `filename`.

    If `required_columns` is set then will only load .csvs with every item in `required_columns` in their column names.


    Args:
        filenames: A list of strings containing the filename for each file to load
        required_columns: A list of strings that must be present in the .csv column headers for the csv to be loaded. Default is an empty list

    Returns:
        A list of dataframes containing the dataframe from every csv in the folder at `path`
    """
    all_files = filenames

    dfs=[]

    for filename in all_files:
        df=load_df_from_csv(filename, **kwargs)
        if(all(elem in df.columns for elem in required_columns)):
            dfs.append(df)

    return dfs


def concat_pandas_dfs(dfs: list[pd.DataFrame]) -> pd.DataFrame:
    """Wrapper for pd.concat to make maintennance easier

    Args:
        dfs: A list of `pd.DataFrame`
    Returns:
        A single `pd.DataFrame`
    """
    
    return pd.concat(dfs, axis=0, ignore_index=True)


def write_dataframe_to_file(df: pd.DataFrame, filename: str):
    """Writes a `pd.DataFrame` to a CSV file at `filename`.

    Args:
        df: a `pd.DataFrame` to be written.
        filename: a string specifying where to save the file

    Returns:
        Returns the output of `df.to_csv(filename)`
    """
    
    return df.to_csv(filename)
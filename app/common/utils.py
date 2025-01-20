"""Module consists of utility functions."""
import os

import pandas as pd


def save_to_csv(data: pd.DataFrame, filename: str = "trending.csv"):
    """Save data as csv in the given datadir.

    Create the directory (and intermediate dirs) if it
    doesn't exist yet. If the file has been created,
    then append it.

    Args:
        data (pd.DataFrame): data to be saved.
        filename (str): directory and the name of the file.
            Default is to save as `trending.csv` in current dir.

    Return:
        None
    """
    if not os.path.isdir(filename.split("/")[-2]):
        os.makedirs(filename.split("/")[-2])

    if not os.path.exists(filename):
        data.to_csv(filename, index=False)
        return

    data.to_csv(filename, index=False, header=False, mode="a")
    return

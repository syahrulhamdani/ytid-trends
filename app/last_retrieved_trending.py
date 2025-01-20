"""Script to check last retrieval trendings in trending.csv"""
import os
import logging

import pandas as pd

from ytid import config as c
from ytid.exceptions import ReadError
from ytid.logger import setup_logging


_LOGGER = logging.getLogger(__name__)


def main():
    filename = os.path.join(c.DATADIR, "trending.csv")
    if not os.path.exists(filename):
        raise ReadError("File not found: %s" % filename)

    df = pd.read_csv(filename, parse_dates=[-1])
    _LOGGER.info("Loaded data: %s", filename)

    last_5_dates = df.trending_time.dt.date.unique()[-5:]
    last_5_dates = [
        date.strftime("%Y%m%d")
        for date in last_5_dates
    ]
    _LOGGER.info("Last 5 retrieval dates: %s", ", ".join(last_5_dates))


if __name__ == "__main__":
    setup_logging()
    main()

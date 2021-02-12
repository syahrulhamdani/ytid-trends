"""Worker to extract Indonesia Trending YouTube Video Statistics."""
import os
import logging
from datetime import datetime
from time import time

import pandas as pd

from ytid import config, YouTube
from ytid.logger import setup_logging


_LOGGER = logging.getLogger(__name__)


def save_to_csv(data, filename="trending.csv"):
    """Save data as csv in the given datadir."""
    if not os.path.isdir(filename.split("/")[-2]):
        os.makedirs(filename.split("/")[-2])

    if not os.path.exists(filename):
        data.to_csv(filename, index=False)
        return

    data.to_csv(filename, index=False, header=False, mode="a")
    return


def main():
    _LOGGER.info("Start retrieving indonesia youtube trending videos")
    youtube = YouTube(
        url=config.URL,
        api_key=config.API_KEY
    )
    start = time()
    videos = youtube.get_trendings()
    end = time()
    _LOGGER.debug("Done retrieving raw video data in %.3fs",
                  (end - start))

    df_videos = pd.DataFrame([
        video.to_dict(trending_time=datetime.now())
        for video in videos
    ])
    _LOGGER.info("Got total %d trending videos", df_videos.shape[0])

    filename = os.path.join(config.DATADIR, "trending.csv")
    save_to_csv(df_videos, filename)
    df_saved = pd.read_csv(filename)
    _LOGGER.info("Done saving %d trending videos (%s). Total videos: %d",
                 df_videos.shape[0],
                 os.path.join(config.DATADIR, "trending.csv"),
                 df_saved.shape[0])


if __name__ == "__main__":
    setup_logging(
        "indonesia-youtube-trending",
        config.LOG_LEVEL
    )
    main()
"""Worker to extract Indonesia Trending YouTube Video Statistics."""
import logging
from datetime import datetime
from pathlib import Path
from time import time

import pandas as pd
import pytz

from common.utils import save_to_csv
from ytid import config, YouTube
from ytid.logger import setup_logging


_LOGGER = logging.getLogger("main")


def main():
    _LOGGER.info("Start retrieving indonesia youtube trending videos")
    now = datetime.now(tz=pytz.utc)
    dataset_version = datetime.now(tz=pytz.timezone("Asia/Jakarta"))
    dataset_version = dataset_version.strftime("%Y%m%d.%H%M")

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
        video.to_dict(trending_time=now)
        for video in videos
    ])
    _LOGGER.info("Got total %d trending videos", df_videos.shape[0])

    filename = Path(config.DATADIR) / f"trending_{dataset_version}.csv"
    save_to_csv(df_videos, filename.as_posix())
    df_saved = pd.read_csv(filename)
    _LOGGER.info("Done saving %d trending videos (%s). Total videos: %d",
                 df_videos.shape[0], filename, df_saved.shape[0])


if __name__ == "__main__":
    setup_logging(config.LOG_LEVEL)
    main()

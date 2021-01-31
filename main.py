"""Worker to extract Indonesia Trending YouTube Video Statistics."""
import logging
from time import time

import pandas as pd

from ytid import config, YouTube
from ytid.logger import setup_logging


_LOGGER = logging.getLogger(__name__)


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
        video.to_dict()
        for video in videos
    ])
    _LOGGER.info("Got total %d trending videos", df_videos.shape[0])


if __name__ == "__main__":
    setup_logging(
        "indonesia-youtube-trending",
        config.LOG_LEVEL
    )
    main()

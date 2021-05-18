import logging
from dataclasses import dataclass
from typing import Dict, List

import requests
from requests.exceptions import RequestException

from common.video import Video
from ytid.exceptions import ReadError


_LOGGER = logging.getLogger(__name__)


@dataclass
class YouTube:
    """YouTube Data API.

    Attributes:
        url (str): url for youtube API.
        api_key (str): API key.
    """
    url: str
    api_key: str

    def _get(self, payload: Dict[str, str]):
        try:
            res = requests.get(self.url, params=payload)
            res.raise_for_status()
        except RequestException:
            raise ReadError(
                "Error while retrieving based on payload: {}".format(payload)
            )
        else:
            return res.json()

    def get_trendings(self, region_code: str = "ID",
                      result_per_page: int = 50) -> List[Video]:
        """Retrieves most popular (trending) videos based on
        specified parameters.

        Args:
            region_code (str): region where the trendings will be retrieved.
                The value follows ISO 3166-1 alpha-2 country code. By default
                will retrieve trending from Indonesia.
            result_per_page (int): maximum number of items that should be returned
                in the result. 50 is the default value.

        Returns:
            List[Video]: List of trending videos.
        """
        payload = {
            "key": self.api_key,
            "chart": "mostPopular",
            "part": "snippet,contentDetails,statistics",
            "regionCode": region_code,
            "maxResults": result_per_page,
        }

        response = self._get(payload)
        videos = response.get("items")
        _LOGGER.debug("Got %d videos from youtube", len(videos))

        cursor = response.get("nextPageToken")
        while cursor:
            payload["pageToken"] = cursor
            response = self._get(payload)
            cursor = response.get("nextPageToken")
            videos.extend(response.get("items"))
            _LOGGER.debug("Got %d videos", len(videos))

        videos = [
            Video(
                snippet=video.get("snippet"),
                content_detail=video.get("contentDetails"),
                statistic=video.get("statistics")
            )
            for video in videos
        ]

        return videos

"""Exceptions module."""


class YoutubeError(Exception):
    """Base class for all exceptions occur in the app."""
    pass


class ReadError(YoutubeError):
    """Error while retrieving items from YouTube"""
    pass

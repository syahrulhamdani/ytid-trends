"""Module for logger."""
import logging
import sys


def setup_logging(log_level="INFO", **kwargs):
    """Setup logging.

    Args:
        log_level (str): Logging level.
    """
    log_format = (
        '%(asctime)s '
        '%(name)s '
        '[%(levelname)s] '
        '%(message)s'
    )

    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setLevel(logging.DEBUG)
    stdout_handler.addFilter(lambda record: record.levelno <= logging.INFO)

    stderr_handler = logging.StreamHandler(sys.stderr)
    stderr_handler.setLevel(logging.WARNING)

    logging.basicConfig(format=log_format,
                        level=log_level,
                        handlers=[stdout_handler, stderr_handler])

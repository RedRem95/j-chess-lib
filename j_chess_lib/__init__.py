"""Top-level package for j-chess-lib."""
import logging
import sys

logger = logging.getLogger("j_chess_lib")
logger_handler = logging.StreamHandler(stream=sys.stderr)
logger_formatter = logging.Formatter('{asctime} - {levelname:^8s} - {message}', "%Y-%m-%d %H:%M:%S", "{")
logger_handler.setFormatter(fmt=logger_formatter)
logger.addHandler(logger_handler)
FORMAT = '{asctime} - {levelname:8s} - {message}s'

from .communication import schema_version

__author__ = """RedRem95"""
__version__ = '0.7.2'
__schema_version__ = schema_version

logger.info(f"Loading j-chess-lib v-{__version__} by {__author__}. Using schema-version v-{schema_version}")

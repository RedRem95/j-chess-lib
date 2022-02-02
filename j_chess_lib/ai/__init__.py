import os

from .ai import AI, StoreAI, DumbAI

__all__ = ["AI", "StoreAI", "DumbAI"]

if os.environ.get("IMPORT_SAMPLE_AIS", True):
    from .examples import *

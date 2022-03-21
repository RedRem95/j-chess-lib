import os

from .ai import AI, StoreAI, DumbAI, VerboseAI

__all__ = ["AI", "StoreAI", "DumbAI", "VerboseAI"]

if os.environ.get("IMPORT_SAMPLE_AIS", True):
    from .examples import *

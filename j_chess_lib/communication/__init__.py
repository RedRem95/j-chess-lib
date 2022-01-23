try:
    from .schema import *
except ImportError as e:
    raise ImportError("Failed to import communication classes provided by schema. Did you install them?") from e

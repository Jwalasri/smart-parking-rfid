"""Placeholder for computer‑vision occupancy detection.

This module defines a stub function that you can replace with your
own computer‑vision model to count occupied parking spaces from
camera images.  The default implementation returns ``None`` to
indicate that no vision‑based occupancy estimate is available.
"""

from __future__ import annotations

from pathlib import Path
from typing import Optional


def detect_occupancy(image_path: Path | str) -> Optional[int]:
    """Return the number of occupied parking spots detected in the image.

    This stub always returns ``None``.  Replace the implementation
    with a call to a trained computer‑vision model.
    """
    # Real implementation would load the image and run it through a
    # model such as YOLO or ResNet to detect cars and compute
    # occupancy.  Here we return None to signal that no estimate is
    # available.
    return None